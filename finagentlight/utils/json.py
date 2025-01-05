import json


def dumps(obj, **kwargs):
    """Serialize an object to str format"""
    return json.dumps(obj, default=str, **kwargs)


def loads(json_str, **kwargs):
    """Deserialize a str to an object"""
    return json.loads(json_str, **kwargs)


def load(file_path):
    with open(file_path) as f:
        return loads(f.read())


def save(obj, file_path):
    with open(file_path, 'w') as f:
        f.write(dumps(obj))
