import logging
from bitstring import BitStream

logger = logging.getLogger(__name__)

def _handle_transfer_encoding(headers, body):
    if not "Transfer-Encoding" in headers:
        return BitStream(body)


    if not headers["Transfer-Encoding"].strip().lower() == "chunked":
        return BitStream(body)

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
