import re
from views import view_register, chat, view_main, view_cats, view_dogs, view_static, view_404

urlpattern = [
    ("^/register$", view_register),
    ("^/chat$", chat),
    ("^/$", view_main),
    ("^/cats", view_cats),
    ("^/dogs", view_dogs),
    ("^/static/(?P<image_name>[a-zA-Z\.]+)$", view_static),
]


def get_view(raw_uri, request_method, http_cookie, body):
    for regex_pattern, view_fun in urlpattern:
        if pattern := re.match(regex_pattern, raw_uri):
            return view_fun(request_method, http_cookie, body, **pattern.groupdict())
    return view_404(request_method, http_cookie, body)


