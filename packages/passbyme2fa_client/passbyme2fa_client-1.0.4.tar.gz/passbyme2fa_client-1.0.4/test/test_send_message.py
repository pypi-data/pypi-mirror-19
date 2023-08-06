from passbyme2fa_client import *
import unittest
import os
import httpretty
from pprint import pprint
import arrow

class TestSendMessage(unittest.TestCase):

    def setUp(self):
        pem_file = os.path.join(os.path.dirname(__file__), "auth.pem")
        self.pbm = PassByME2FAClient(
            key = pem_file, cert = pem_file, password = "123456"
        )
        httpretty.enable()

    def test_missing_recipients(self):
        with self.assertRaises(ValueError):
            self.pbm.send_message(
            )
        with self.assertRaises(ValueError):
            self.pbm.send_message(
                recipients = []
            )

    def test_invalid_availability(self):
        with self.assertRaises(ValueError):
            self.pbm.send_message(
                recipients = ["somebody@somewhe.re"],
                availability = "hey"
            )

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            self.pbm.send_message(
                recipients = ["somebody@somewhe.re"],
                availability = 300,
                type = "whoa"
            )

    def test_non_420_error_code(self):
        httpretty.register_uri(httpretty.POST, "https://auth-sp.passbyme.com/frontend/messages",
                           status = 500)
        with self.assertRaises(HTTPError):
            self.pbm.send_message(
                recipients = ["somebody@somewhe.re"],
                availability = 300,
                type = PassByME2FAClient.MessageType.MESSAGE
            )

    def test_420_error_code_no_resp_body(self):
        httpretty.register_uri(httpretty.POST, "https://auth-sp.passbyme.com/frontend/messages",
                           status = 420, body = None)
        with self.assertRaises(HTTPError):
            self.pbm.send_message(
                recipients = ["somebody@somewhe.re"],
                availability = 300,
                type = PassByME2FAClient.MessageType.MESSAGE
            )

    def test_420_error_code_invalid_resp_body(self):
        httpretty.register_uri(httpretty.POST, "https://auth-sp.passbyme.com/frontend/messages",
                           status = 420, body = "No JSON, sorry.")
        with self.assertRaises(ValueError):
            self.pbm.send_message(
                recipients = ["somebody@somewhe.re"],
                availability = 300,
                type = PassByME2FAClient.MessageType.MESSAGE
            )

    def test_420_error_code(self):
        httpretty.register_uri(httpretty.POST, "https://auth-sp.passbyme.com/frontend/messages",
                           status = 420,
                           body = "{\"code\": 421}")
        with self.assertRaises(PassByMEError) as context:
            self.pbm.send_message(
                recipients = ["somebody@somewhe.re"],
                availability = 300,
                type = PassByME2FAClient.MessageType.MESSAGE
            )
        self.assertEqual(421, context.exception.response["code"])

    def test_no_response_body(self):
        httpretty.register_uri(httpretty.POST, "https://auth-sp.passbyme.com/frontend/messages",
                           status = 200, body = None)
        with self.assertRaises(HTTPError):
            self.pbm.send_message(
                recipients = ["somebody@somewhe.re"],
                availability = 300,
                type = PassByME2FAClient.MessageType.MESSAGE
            )

    def test_response_body(self):
        httpretty.register_uri(httpretty.POST, "https://auth-sp.passbyme.com/frontend/messages",
           status = 200,
           body = "{\"messageId\": \"YzX95zUA1et2ijQ\", \"expirationDate\" : \"2015-06-11T13:06:12.658+02:00\"," +
                     "\"recipients\" : [{ \"userId\": \"pbmId1\", \"status\": \"PENDING\" }," +
                       "{\"userId\": \"pbmId2\", \"status\": \"NOTIFIED\" },"+
                       "{\"userId\": \"pbmId3\", \"status\": \"SEEN\" }]}")
        session_info = self.pbm.send_message(
                recipients = ["somebody@somewhe.re"],
                availability = 300,
                type = PassByME2FAClient.MessageType.MESSAGE
            )
        self.assertEqual("YzX95zUA1et2ijQ", session_info.message_id)
        self.assertEqual(arrow.get("2015-06-11T13:06:12.658+02:00"), session_info.expiration_date)
        self.assertEqual(3, len(session_info.recipient_statuses))
        self.assertEqual("pbmId1", session_info.recipient_statuses[0].user_id)
        self.assertEqual(PassByME2FAClient.MessageStatus.PENDING, session_info.recipient_statuses[0].status)
        self.assertEqual("pbmId2", session_info.recipient_statuses[1].user_id)
        self.assertEqual(PassByME2FAClient.MessageStatus.NOTIFIED, session_info.recipient_statuses[1].status)
        self.assertEqual("pbmId3", session_info.recipient_statuses[2].user_id)
        self.assertEqual(PassByME2FAClient.MessageStatus.SEEN, session_info.recipient_statuses[2].status)
