from json import dumps

import json
import time
from hyper import HTTP20Connection
from hyper.tls import init_context
from hyper.http20.connection import StreamResetError
from errors import exception_class_for_reason


IMMEDIATE_NOTIFICATION_PRIORITY = 10
DELAYED_NOTIFICATION_PRIORITY = 5


class APNsClient(object):
    def __init__(self, cert_file, log, use_sandbox=False, use_alternative_port=False, proto=None):
        self.log = log
        self.server = 'api.development.push.apple.com' if use_sandbox else 'api.push.apple.com'
        self.port = 2197 if use_alternative_port else 443
        self.ssl_context = init_context()
        self.ssl_context.load_cert_chain(cert_file)
        self.proto = proto
        self.__connection = None
        self.connect_to_apn_if_needed()

    def connect_to_apn_if_needed(self):
        if self.__connection is None:
            self.__connection = HTTP20Connection(self.server, self.port, ssl_context=self.ssl_context,
                                                 force_proto=self.proto or 'h2')

    def send_notification(self, token_hex, notification, priority=IMMEDIATE_NOTIFICATION_PRIORITY, topic=None, expiration=None):
        json_payload = dumps(notification.dict(), ensure_ascii=False, separators=(',', ':')).encode('utf-8')

        headers = {
            'apns-priority': str(priority)
        }
        if topic is not None:
            headers['apns-topic'] = topic

        if expiration is not None:
            headers['apns-expiration'] = "%d" % expiration

        url = '/3/device/{}'.format(token_hex)
        sent = False
        while not sent:
            try:
                self.connect_to_apn_if_needed()
                stream_id = self.__connection.request('POST', url, json_payload, headers)
                resp = self.__connection.get_response(stream_id)
                with resp:
                    if resp.status != 200:
                        raw_data = resp.read().decode('utf-8')
                        data = json.loads(raw_data)
                        raise exception_class_for_reason(data['reason'])
                sent = True
            except StreamResetError:
                # Connection to APN closed, reconnect
                self.log.exception("Connection to APN lost, reconnecting and trying again")
                self.__connection = None
                time.sleep(5)
