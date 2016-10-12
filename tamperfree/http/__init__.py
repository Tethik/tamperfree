import logging
import string
from bitstring import ConstBitStream, BitStream, Bits
from tamperfree.http.content_type import _handle_content_type
from tamperfree.http.content_encoding import _handle_content_encoding
from tamperfree.http.transfer_encoding import _handle_transfer_encoding
import sys
import re

logger = logging.getLogger(__name__)

class HttpRequest(object):
    def __init__(self, headers, path, body):
        self.headers = headers
        self.path = path
        self.body = body

class HttpResponse(object):
    def __init__(self, status_line, headers, body):
        self.status_line = status_line
        self.headers = headers
        self.body = body

def _parse_response(bytes):
    stream = ConstBitStream(bytes=bytes)
    pos = stream.find(Bits(bytes=b'\r\n\r\n'), bytealigned=True)[0]
    header_bytes, body = stream[:pos], stream[pos+32:]
    headers = dict()
    header_lines = header_bytes.bytes.decode("ascii").split('\r\n')
    status_line = header_lines[0]
    for h in header_lines[1:]:
        splits = h.split(":")
        headers[splits[0]] = splits[1].strip()

    return HttpResponse(status_line, headers, body.tobytes())

def _parse_request(bytes, path):
    stream = ConstBitStream(bytes=bytes)
    pos = stream.find(Bits(bytes=b'\r\n\r\n'), bytealigned=True)[0]
    # For now I don't care about the request body.
    header_bytes, _ = stream[:pos], stream[pos+32:]
    headers = dict()
    header_lines = header_bytes.bytes.decode("ascii").split('\r\n')
    for h in header_lines[1:]:
        splits = h.split(":")
        headers[splits[0]] = splits[1].strip()

    return HttpRequest(headers, path, None)


def extract_from_raw(text):
    # Find responses. Needs to be improved. Currently putting HTTP/1.1 in the body or headers could trick this.
    request_re = re.compile('(GET|HEAD|POST|PUT|DELETE|TRACE|CONNECT|OPTIONS|PATCH) ([^\n]+) HTTP\/\d\.\d')
    response_re = re.compile('HTTP/\d\.\d (\d+) ([A-Z ]+)')
    lookup = dict()
    request_matches = []
    for m in re.finditer(request_re, text):
        lookup[m.start()] = "request"
        request_matches.append(m)
    response_matches = []
    for m in re.finditer(response_re, text):
        lookup[m.start()] = "response"
        response_matches.append(m)

    matches = sorted(request_matches + response_matches, key=lambda x: x.start())
    logger.info("After sort")
    for m in matches:
        logger.info(m.start(), m.groups())

    logger.info("")
    logger.info("***************")

    requests = [] # assuming fifo. i.e. first response is replying to first request.
    responses = []

    def _parse(requests, responses, match, data):
        logger.info(match.start(), match.groups())
        if lookup[match.start()] == "request":
            request = _parse_request(data, match.group(0))
            requests.append(request)
        elif lookup[match.start()] == "response":
            response = _parse_response(data)
            response.request = requests[0]
            requests.pop(0)
            responses.append(response)

    if len(matches) < 2:
        return []

    previous = matches[0]
    for current in matches[1:]:
        start = previous.start()
        end = current.start()
        data = text[start:end]
        _parse(requests, responses, previous, data)
        previous = current

    # last one
    data = text[previous.start():len(text)]
    _parse(requests, responses, previous, data)

    logger.info("")
    logger.info("***************")

    return responses

def extract_from_capturefile(capturefile):
    with open(capturefile, 'r') as cf:
        raw_text = cf.read()
        return extract_from_raw(raw_text)

def _main(file):
    extract_from_capturefile(file)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    _main(sys.argv[1])
