import logging
import sys
import time
import threading
import string
from bitstring import ConstBitStream, BitStream
import zlib
import base64

logger = logging.getLogger(__name__)

def _handle_content_encoding(headers, body):
    if not "Content-Encoding" in headers:
        return body

    encoding = headers["Content-Encoding"].strip()

    if not encoding:
        return body

    if "gzip" in encoding:
        body.pos = 0
        return zlib.decompress(body.bytes, 16+zlib.MAX_WBITS)
    else:
        raise NotImplementedError("%s encoding not implemented" % encoding)




def _handle_content_type(headers, body):
    if not 'Content-Type' in headers:
        return body

    charset_def = "charset="
    charset = None

    h = headers['Content-Type']

    i = h.find(charset_def)
    # logger.debug(h)
    # logger.debug(i)
    if i >= 0:
        e = h.find(";", i)
        if e < 0:
            e = len(h)
        charset = h[i+len(charset_def):e].replace(";", "").strip()

    # logger.debug(charset)
    if charset == "utf-8":
        body = body.decode("utf-8")
    else:
        body = body.decode("ascii")
    return body

def _handle_transfer_encoding(headers, body):
    if not "Transfer-Encoding" in headers:
        return body


    if not headers["Transfer-Encoding"].strip().lower() == "chunked":
        return body

    new_body = BitStream()
    # Chunked responses are encoded by separating the response into chunks.
    # Each chunk begins with a number followed by \r\n.
    # The number is how many bytes the chunk contains.
    # After the \r\n\r\n the chunk bytes go. The chunk ends after the
    # specified number of byes and another \r\n
    start_pos = 0

    while start_pos < len(body):
        body.pos = start_pos
        i = body.find(b'\r\n', start = start_pos, bytealigned = True)
        if not i:
            break
        i = i[0]
        logger.debug(i)
        body.pos = start_pos # rewind
        h = body[start_pos:i].bytes.decode('ascii')
        num_bits = int(h, 16)*8
        logger.debug("Chunk with {num_bytes} bytes at binary pos {start_pos}".\
            format(num_bytes = num_bits//8, start_pos = start_pos))
        if num_bits == 0:
            break
        chunk_data = body[i+16:i+16+num_bits]
        logger.debug("{b} len: {l}".format(b = str(chunk_data), l = len(chunk_data)))
        new_body.insert(chunk_data)
        start_pos += i + num_bits + 32

        # todo: handle chunk extensions.

    body = new_body
    return body


def _parse_request(stream):
    # headers followed by two \r\n
    pos = stream.find(b'\r\n\r\n', bytealigned=True)[0]
    header_bytes, body = stream[:pos], stream[pos+32:]
    headers = dict()
    header_lines = header_bytes.bytes.decode("ascii").split('\r\n')
    for h in header_lines[1:]:
        splits = h.split(":")
        headers[splits[0]] = splits[1].strip()

    logger.debug(header_lines[0])
    logger.debug(headers)
    logger.debug(body)

    body = _handle_transfer_encoding(headers, body)
    logger.debug(body)
    body = _handle_content_encoding(headers, body)
    logger.debug(body)
    body = _handle_content_type(headers, body)
    logger.debug(body)

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




def _main():
    extract_from_capture("caps/1.cap")

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    _main()
