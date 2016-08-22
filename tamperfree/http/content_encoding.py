import zlib
import logging

logger = logging.getLogger(__name__)

def _handle_content_encoding(headers, body):
    if not "Content-Encoding" in headers:
        return body.bytes

    encoding = headers["Content-Encoding"].strip()

    if not encoding:
        return body.bytes

    # This needs to be updated for all the different types of encoding. Add as needed.
    if "gzip" in encoding:
        body.pos = 0
        return zlib.decompress(body.bytes, 16+zlib.MAX_WBITS)
    else:
        raise NotImplementedError("%s encoding not implemented" % encoding)
