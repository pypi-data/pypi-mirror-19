from .json_helper import get_json_field

class RecipientStatus:

    def __init__(self, json):
        self.user_id = get_json_field(json, "userId")
        self.status = get_json_field(json, "status")        
