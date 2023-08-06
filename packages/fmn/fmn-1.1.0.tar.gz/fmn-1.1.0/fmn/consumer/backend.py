# FMN worker figuring out for a fedmsg message the list of recipient and
# contexts
from __future__ import print_function


import json
import logging
import smtplib
import time

import pika
import fedmsg
import fedmsg.meta
import fedmsg_meta_fedora_infrastructure

from pika.adapters import twisted_connection
from twisted.internet import defer, reactor, protocol, task

import fmn.lib
import fmn.rules.utils
import fmn.consumer.backends as fmn_backends
import fmn.consumer.producer as fmn_producers

import fmn.consumer.fmn_fasshim
from fedmsg_meta_fedora_infrastructure import fasshim


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("fmn")
log.setLevel('DEBUG')
CONFIG = fedmsg.config.load_config()
fedmsg.meta.make_processors(**CONFIG)

DB_URI = CONFIG.get('fmn.sqlalchemy.uri', None)
session = fmn.lib.models.init(DB_URI)

fmn.consumer.fmn_fasshim.make_fas_cache(**CONFIG)
# Monkey patch fedmsg_meta modules
fasshim.nick2fas = fmn.consumer.fmn_fasshim.nick2fas
fasshim.email2fas = fmn.consumer.fmn_fasshim.email2fas
fedmsg_meta_fedora_infrastructure.supybot.nick2fas = \
    fmn.consumer.fmn_fasshim.nick2fas
fedmsg_meta_fedora_infrastructure.anitya.email2fas = \
    fmn.consumer.fmn_fasshim.email2fas
fedmsg_meta_fedora_infrastructure.bz.email2fas = \
    fmn.consumer.fmn_fasshim.email2fas
fedmsg_meta_fedora_infrastructure.mailman3.email2fas = \
    fmn.consumer.fmn_fasshim.email2fas
fedmsg_meta_fedora_infrastructure.pagure.email2fas = \
    fmn.consumer.fmn_fasshim.email2fas

CNT = 0

log.debug("Instantiating FMN backends")
backend_kwargs = dict(config=CONFIG)

# If debug is enabled, use the debug backend everywhere
if CONFIG.get('fmn.backends.debug', False):
    log.debug(' ** Use the DebugBackend as all backends **')
    backends = {
        'sse': fmn_backends.SSEBackend(**backend_kwargs),
        'email': fmn_backends.DebugBackend(**backend_kwargs),
        'irc': fmn_backends.IRCBackend(**backend_kwargs),
        'android': fmn_backends.DebugBackend(**backend_kwargs),
    }
else:
    backends = {
        'sse': fmn_backends.SSEBackend(**backend_kwargs),
        'email': fmn_backends.EmailBackend(**backend_kwargs),
        'irc': fmn_backends.IRCBackend(**backend_kwargs),
        'android': fmn_backends.GCMBackend(**backend_kwargs),
    }

# But, disable any of those backends that don't appear explicitly in
# our config.
for key, value in backends.items():
    if key not in CONFIG['fmn.backends']:
        del backends[key]

# Also, check that we don't have something enabled that's not explicit
for key in CONFIG['fmn.backends']:
    if key not in backends:
        raise ValueError("%r in fmn.backends (%r) is invalid" % (
            key, CONFIG['fmn.backends']))


def get_preferences():
    print('get_preferences')
    prefs = {}
    for p in session.query(fmn.lib.models.Preference).all():
        prefs['%s__%s' % (p.openid, p.context_name)] = p
    print('prefs retrieved')
    return prefs


PREFS = get_preferences()


def update_preferences(openid, prefs):
    print("Refreshing preferences for %r" % openid)
    for p in fmn.lib.models.Preference.by_user(session, openid):
        prefs['%s__%s' % (p.openid, p.context_name)] = p
    return prefs


@defer.inlineCallbacks
def run(connection):

    channel = yield connection.channel()
    yield channel.basic_qos(prefetch_count=1)

    queue = 'refresh'
    yield channel.exchange_declare(exchange=queue, type='fanout')
    result = yield channel.queue_declare(exclusive=False)
    queue_name = result.method.queue
    yield channel.queue_bind(exchange=queue, queue=queue_name)
    queue_object, consumer_tag = yield channel.basic_consume(queue=queue_name)
    lc = task.LoopingCall(read, queue_object)
    lc.start(0.01)

    queue = 'backends'
    yield channel.exchange_declare(exchange=queue, type='direct')
    yield channel.queue_declare(durable=True)
    yield channel.queue_bind(exchange=queue, queue=queue)
    queue_object2, consumer_tag2 = yield channel.basic_consume(queue=queue)
    lc2 = task.LoopingCall(read, queue_object2)
    lc2.start(0.01)


@defer.inlineCallbacks
def read(queue_object):

    ch, method, properties, body = yield queue_object.get()

    global CNT, PREFS
    CNT += 1

    start = time.time()

    data = json.loads(body)
    topic = data.get('topic', '')
    function = data.get('function', '')

    if '.fmn.' in topic:
        openid = data['body']['msg']['openid']
        PREFS = update_preferences(openid, PREFS)
        if topic == 'consumer.fmn.prefs.update':  # msg from the consumer
            print("Done with refreshing prefs.  %0.2fs %s" % (
                time.time() - start, data['topic']))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

    if function:
        print("Got a function call to %s" % function)
        if function == 'handle':
            backend = backends[data['backend']]
            backend.handle(session,
                           data['recipient'],
                           data['msg'],
                           data['streamline'])
            ch.basic_ack(delivery_tag=method.delivery_tag)
        elif function == 'handle_batch':
            backend = backends[data['backend']]
            backend.handle_batch(session,
                                 data['recipient'],
                                 data['queued_messages'])
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            print("Unknown function")
        return

    recipients, context, raw_msg = \
        data['recipients'], data['context'], data['raw_msg']['body']

    print("  Considering %r with %i recips" % (
        context, len(list(recipients))))

    backend = backends[context]
    for recipient in recipients:
        user = recipient['user']
        t = time.time()
        pref = PREFS.get('%s__%s' % (user, context))
        print("pref retrieved in: %0.2fs" % (time.time() - t))

        try:
            if not pref.should_batch:
                print("    Calling backend %r with %r" % (backend, recipient))
                t = time.time()
                backend.handle(session, recipient, raw_msg)
                print("Handled by backend in: %0.2fs" % (time.time() - t))
            else:
                print("    Queueing msg for digest")
                fmn.lib.models.QueuedMessage.enqueue(
                    session, user, context, raw_msg)
            if ('filter_oneshot' in recipient and recipient['filter_oneshot']):
                print("    Marking one-shot filter as fired")
                idx = recipient['filter_id']
                fltr = session.query(fmn.lib.models.Filter).get(idx)
                fltr.fired(session)
        except RuntimeError:
            yield ch.basic_nack(delivery_tag=method.delivery_tag)
            return
        except smtplib.SMTPSenderRefused:
            yield ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

    session.commit()

    yield ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Done.  %0.2fs %s %s" % (
              time.time() - start, raw_msg['msg_id'], raw_msg['topic']))


parameters = pika.ConnectionParameters()
cc = protocol.ClientCreator(
    reactor, twisted_connection.TwistedProtocolConnection, parameters)
host = CONFIG.get('fmn.pika.host', 'localhost')
port = int(CONFIG.get('fmn.pika.port', 5672))
d = cc.connectTCP(host=host, port=port)
d.addCallback(lambda protocol: protocol.ready)
d.addCallback(run)

# Here we schedule to producers to run periodically (with a default
# frequency of 10 seconds.
# Added value: Everything is nicely tied up with twisted in one app/place
# Cons: if one of the producer suddenly takes a real while to run, it will
# block the entire twisted reactor and thus all the backends with it.
# TODO: move to cron?
frequency = CONFIG.get('fmn.confirmation_frequency', 10)
confirmation_producer = fmn_producers.ConfirmationProducer(
    session, backends)
lc3 = task.LoopingCall(confirmation_producer.work)
lc3.start(frequency)


try:
    print('Starting consuming')
    reactor.run()
except KeyboardInterrupt:
    pass
finally:
    session.close()
    print('%s tasks proceeded' % CNT)
