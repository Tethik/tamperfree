import logging

logger = logging.getLogger(__name__)

def _handle_content_type(headers, body):
    if not 'Content-Type' in headers:
        return body

    charset_def = "charset="
    charset = None

    h = headers['Content-Type']

    i = h.find(charset_def)
    if i >= 0:
        e = h.find(";", i)
        if e < 0:
            e = len(h)
        charset = h[i+len(charset_def):e].replace(";", "").strip()

    if charset == "utf-8" or i == -1:
        body = body.decode("utf-8")
    elif charset == "ascii":
        body = body.decode("ascii")
    else:
        raise NotImplementedError("{charset} charset is not implemented".format(charset=charset))
    return body
