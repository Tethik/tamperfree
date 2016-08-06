import socket
import logging
import sys
import time
import threading

logger = logging.getLogger(__name__)

class TcpChannel(threading.Thread):
    def __init__(self, conn, outfile):
        threading.Thread.__init__(self)
        self.conn = conn
        self.outfile = outfile

    def run(self):
        with open(self.outfile, "wb") as fd:
            try:
                remote_conn = socket.create_connection(("127.0.0.1", "9150"))
                self._proxy(remote_conn, fd)
            except Exception as ex:
                logger.error(ex)
            finally:
                remote_conn.close()
                logger.info('Closing remote socket')
                self.conn.close()
                logger.info('Closing client socket')

    def _proxy(self, remote_conn, fd):
        self.conn.setblocking(0)
        remote_conn.setblocking(0)
        lst_msg_received = time.clock()
        while lst_msg_received + 2 > time.clock():
            p1 = self._read_and_send_all(self.conn, remote_conn)
            p2 = self._read_and_send_all(remote_conn, self.conn, fd)
            if p1 or p2:
                lst_msg_received = time.clock()



    def _read_and_send_all(self, _from, to, fd = None):
        try:
            data = _from.recv(4096)
            if fd:
                fd.write(data)
                fd.flush()
            to.sendall(data)
            return True
        except:
            return False




class TCP(threading.Thread):
    """
    Copied/Modified from proxy.py github
    """

    def __init__(self, hostname='127.0.0.1', port=8899, backlog=5):
        threading.Thread.__init__(self)
        self.hostname = hostname
        self.port = port
        self.counter = 1
        self.started = False
        self.backlog = backlog

    def run(self):
        try:
            logger.info('Starting server on port %d' % self.port)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.hostname, self.port))
            self.socket.listen(self.backlog)
            self.started = True
            self.threads = []

            while self.started:
                conn, addr = self.socket.accept()
                logger.debug('Accepted connection %r at address %r' % (conn, addr))
                tor = TcpChannel(conn, 'caps/%s.cap' % self.counter)
                self.threads.append(tor)
                self.counter += 1
                tor.start()
        except KeyboardInterrupt as e:
            logger.info('Interrupt exception caught.')
            for thread in self.threads:
                if thread.is_alive():
                    thread.join(2)
                if thread.is_alive():
                    raise RuntimeError("Proxy-Thread wont stop.")
        except Exception as e:
            logger.exception('Exception while running the server %r' % e)
        finally:
            logger.info('Closing server socket')
            self.socket.close()

    def close(self):
        self.started = False

    def finished(self):
        return all(not thread.is_alive() for thread in self.threads)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    proxy = TCP()
    proxy.run()
    assert proxy.finished()
