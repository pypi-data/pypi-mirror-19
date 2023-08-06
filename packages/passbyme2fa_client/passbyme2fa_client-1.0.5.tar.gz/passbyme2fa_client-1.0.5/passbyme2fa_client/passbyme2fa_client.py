
try:
    from httplib import HTTPSConnection
except:
    from http.client import HTTPSConnection
import ssl
import os
from pprint import pprint
import json
from .http_error import HTTPError
from .passbyme_error import PassByMEError
from .session_info import SessionInfo

class PassByME2FAClient:

    class MessageType:
        AUTHORIZATION = "authorization"
        MESSAGE       = "message"
        ESIGN         = "esign"

    class MessageStatus:
        PENDING        = "PENDING"
        NOTIFIED       = "NOTIFIED"
        DOWNLOADED     = "DOWNLOADED"
        SEEN           = "SEEN"
        NOT_SEEN       = "NOT_SEEN"
        NOT_NOTIFIED   = "NOT_NOTIFIED"
        NOT_DOWNLOADED = "NOT_DOWNLOADED"
        NO_DEVICE      = "NO_DEVICE"
        FAILED         = "FAILED"
        DISABLED       = "DISABLED"
        CANCELLED      = "CANCELLED"
        APPROVED       = "APPROVED"
        DENIED         = "DENIED"

    def __init__(self,
                address = "auth-sp.passbyme.com",
                key = None, cert = None, password = None
            ):
        if key is None or cert is None or len(key) == 0 or len(cert) == 0:
            raise ValueError("SSL key or certificate is missing!")
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_verify_locations(
            os.path.join(os.path.dirname(__file__), "truststore.pem"))
        context.load_cert_chain(certfile = cert,
            keyfile = key, password = password)
        self.http = HTTPSConnection(address,
                context = context
            )

    def send_message(self,
                recipients = None,
                subject = None,
                body = None,
                availability = None,
                type = None,
                callbackUrl = None):
        if recipients is None or len(recipients) == 0:
            raise ValueError("Recipients are not given!")

        availability = int(availability)
        if availability < 1:
            raise ValueError("Invalid availability!")

        if type not in [getattr(self.MessageType, attr)
                for attr in dir(self.MessageType) if not attr.startswith("__")]:
            raise ValueError("Invalid type: " + type)

        body = json.dumps({
          "recipients": recipients,
          "subject": subject,
          "body": body,
          "availability": availability,
          "type": type,
          "callbackUrl": callbackUrl
        })
        headers = {
            "Content-type": "application/json",
        }
        return SessionInfo(
            self.__do_https("POST", "/frontend/messages", headers, body),
            self
        )

    def track_message(self, message_id = None, session_info = None):
        return self.__handle_existing_message("GET",
            message_id, session_info)

    def cancel_message(self, message_id = None, session_info = None):
        return self.__handle_existing_message("DELETE",
            message_id, session_info)

    def __handle_existing_message(self, http_method,
                message_id = None, session_info = None
            ):
        if session_info is not None:
            message_id = session_info.message_id
        if message_id is None or len(message_id) == 0:
            raise ValueError("Message id is missing!")

        json = self.__do_https(http_method, "/frontend/messages/" + message_id)

        if session_info is not None:
            session_info.re_init(json)
            return session_info

        return SessionInfo(json, self)

    def __do_https(self, method, path, additional_headers = None, body = None):
        headers = {
            "X-PBM-API-VERSION": "1"
        }
        if additional_headers is not None:
            headers.update(additional_headers)

        self.http.request(method, path, body, headers)
        response = self.http.getresponse()

        resp_body = response.read()
        if len(resp_body) == 0:
            raise HTTPError(response)

        if response.status < 200 or response.status > 299:
            if response.status == 420:
                raise PassByMEError(json.loads(resp_body.decode("utf-8")))
            else:
                raise HTTPError(response)

        return json.loads(resp_body.decode("utf-8"))
