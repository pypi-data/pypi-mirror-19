def get_json_field(json, field):
    if field not in json:
        raise IOError("Missing JSON field: %s" % field)
    return json[field]
