import datetime
import arrow
from .json_helper import get_json_field
from .recipient_status import RecipientStatus

class SessionInfo:

    def __init__(self, json, pbm_client):
        self.re_init(json)
        self.pbm_client = pbm_client

    def refresh(self):
        self.pbm_client.track_message(session_info = self)

    def cancel(self):
        self.pbm_client.cancel_message(session_info = self)

    def re_init(self, json):
        self.message_id = get_json_field(json, "messageId")
        self.expiration_date = arrow.get(
            get_json_field(json, "expirationDate")
        )
        self.recipient_statuses = [
            RecipientStatus(json)
                for json in get_json_field(json, "recipients")
        ]
