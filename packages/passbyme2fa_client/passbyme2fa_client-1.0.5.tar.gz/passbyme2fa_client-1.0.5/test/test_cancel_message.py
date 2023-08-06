from passbyme2fa_client import *
import unittest
import os
import httpretty
from pprint import pprint
import arrow

class TestCancelMessage(unittest.TestCase):

    def setUp(self):
        pem_file = os.path.join(os.path.dirname(__file__), "auth.pem")
        self.pbm = PassByME2FAClient(
            key = pem_file, cert = pem_file, password = "123456"
        )
        httpretty.enable()

    def test_response_body(self):
        httpretty.register_uri(httpretty.DELETE, "https://auth-sp.passbyme.com/frontend/messages/YzX95zUA1et2ijQ",
           status = 200,
           body = "{\"messageId\": \"YzX95zUA1et2ijQ\", \"expirationDate\" : \"2015-06-11T13:06:12.658+02:00\"," +
                     "\"recipients\" : [{ \"userId\": \"pbmId1\", \"status\": \"CANCELLED\" }]}")
        session_info = self.pbm.cancel_message(
                "YzX95zUA1et2ijQ"
            )
        self.assertEqual("YzX95zUA1et2ijQ", session_info.message_id)
        self.assertEqual(arrow.get("2015-06-11T13:06:12.658+02:00"), session_info.expiration_date)
        self.assertEqual(1, len(session_info.recipient_statuses))
        self.assertEqual("pbmId1", session_info.recipient_statuses[0].user_id)
        self.assertEqual(PassByME2FAClient.MessageStatus.CANCELLED, session_info.recipient_statuses[0].status)

    def test_session_info_cancel(self):
        httpretty.register_uri(httpretty.POST, "https://auth-sp.passbyme.com/frontend/messages",
           status = 200,
           body = "{\"messageId\": \"YzX95zUA1et2ijQ\", \"expirationDate\" : \"2015-06-11T13:06:12.658+02:00\"," +
                     "\"recipients\" : [{ \"userId\": \"pbmId1\", \"status\": \"PENDING\" }]}")
        httpretty.register_uri(httpretty.GET, "https://auth-sp.passbyme.com/frontend/messages/YzX95zUA1et2ijQ",
           status = 200,
           body = "{\"messageId\": \"YzX95zUA1et2ijQ\", \"expirationDate\" : \"2015-06-11T13:06:12.658+02:00\"," +
                     "\"recipients\" : [{ \"userId\": \"pbmId1\", \"status\": \"CANCELLED\" }]}")

        session_info = self.pbm.send_message(
                recipients = ["somebody@somewhe.re"],
                availability = 300,
                type = PassByME2FAClient.MessageType.MESSAGE
            )
        self.assertEqual("YzX95zUA1et2ijQ", session_info.message_id)
        self.assertEqual(arrow.get("2015-06-11T13:06:12.658+02:00"), session_info.expiration_date)
        self.assertEqual(1, len(session_info.recipient_statuses))
        self.assertEqual("pbmId1", session_info.recipient_statuses[0].user_id)
        self.assertEqual(PassByME2FAClient.MessageStatus.PENDING, session_info.recipient_statuses[0].status)

        session_info.cancel()

        self.assertEqual(PassByME2FAClient.MessageStatus.CANCELLED, session_info.recipient_statuses[0].status)
