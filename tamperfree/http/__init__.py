import logging
import string
from bitstring import ConstBitStream, BitStream, Bits
from tamperfree.http.content_type import _handle_content_type
from tamperfree.http.content_encoding import _handle_content_encoding
from tamperfree.http.transfer_encoding import _handle_transfer_encoding
import sys

logger = logging.getLogger(__name__)

class HttpRequest(object):
    def __init__(self, headers, body):
        self.headers = headers
        self.body = body

class HttpResponse(object):
    def __init__(self, status_line, headers, body):
        self.status_line = status_line
        self.headers = headers
        self.body = body

def _parse_response(stream):
    # headers followed by two \r\n
    pos = stream.find(Bits(bytes=b'\r\n\r\n'), bytealigned=True)[0]
    header_bytes, body = stream[:pos], stream[pos+32:]
    headers = dict()
    header_lines = header_bytes.bytes.decode("ascii").split('\r\n')
    status_line = header_lines[0]
    for h in header_lines[1:]:
        splits = h.split(":")
        headers[splits[0]] = splits[1].strip()

    # logger.debug(header_lines[0])
    logger.debug(headers)
    # logger.debug(body)

    body = _handle_transfer_encoding(headers, body)
    # logger.debug(body)
    body = _handle_content_encoding(headers, body)
    # logger.debug(body)
    body = _handle_content_type(headers, body)
    # logger.debug(body)
    if len(body) == 0:
        body = "" #just making sure that body is a string after all this.

    return HttpResponse(status_line, headers, body)

def _parse_request(stream):
    pos = stream.find(Bits(bytes=b'\r\n\r\n'), bytealigned=True)[0]
    # For now I don't care about the request body.
    header_bytes, _ = stream[:pos], stream[pos+32:]
    headers = dict()
    header_lines = header_bytes.bytes.decode("ascii").split('\r\n')
    for h in header_lines[1:]:
        splits = h.split(":")
        headers[splits[0]] = splits[1].strip()

    return HttpRequest(headers, None)


def extract_from_raw(bytes):
    stream = ConstBitStream(bytes=bytes)
    # Find responses. Needs to be improved. Currently putting HTTP/1.1 in the body or headers could trick this.
    # Also HTTP/2.0 is probably a thing soon.
    header_positions = [p for p in stream.findall(Bits(bytes=b'HTTP'), bytealigned=True)]

    logger.debug(str(header_positions))
    header_positions.append(len(stream))
    responses = []

    for i in range(len(header_positions) - 1):
        pos = header_positions[i]
        next_pos = header_positions[i+1]
        request = stream[pos:next_pos]
        response  = _parse_response(request)
        responses.append(response)

    return responses



def extract_from_capturefile(capturefile):
    with open(capturefile, 'rb') as cf:
        bytes = cf.read()
        return extract_from_raw(bytes)


def _main(file):
    extract_from_capturefile(file)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    _main(sys.argv[1])
