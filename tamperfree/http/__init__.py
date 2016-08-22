import logging
import string
from bitstring import ConstBitStream, BitStream
from tamperfree.http.content_type import _handle_content_type
from tamperfree.http.content_encoding import _handle_content_encoding
from tamperfree.http.transfer_encoding import _handle_transfer_encoding
import sys

logger = logging.getLogger(__name__)

def _parse_request(stream):
    # headers followed by two \r\n
    pos = stream.find(b'\r\n\r\n', bytealigned=True)[0]
    header_bytes, body = stream[:pos], stream[pos+32:]
    headers = dict()
    header_lines = header_bytes.bytes.decode("ascii").split('\r\n')
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

    return headers, body


def extract_from_capture(capturefile):
    with open(capturefile, 'rb') as cf:
        bytes = cf.read()
        stream = ConstBitStream(bytes=bytes)
        header_positions = [p for p in stream.findall(b'HTTP/1.1', bytealigned=True)]


        logger.debug(str(header_positions))
        header_positions.append(len(stream))

        for i in range(len(header_positions) - 1):
            pos = header_positions[i]
            next_pos = header_positions[i+1]
            request = stream[pos:next_pos]
            headers, body = _parse_request(request)
            print(body)

def _main(file):
    extract_from_capture(file)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    _main(sys.argv[1])
