def parse_body(body):
    data = {}
    if body is None:
        return data
    for input_ in body.decode().split("&"):
        key, value = input_.split("=")
        data[key] = value
    return data

def parse_cookie(http_cookie):
    data = {}
    if http_cookie is None:
        return data
    for input_ in http_cookie.split("; "):
        if "=" not in input_:
            continue
        key, *value = input_.split("=")
        data[key] = "=".join(value)
    return data
