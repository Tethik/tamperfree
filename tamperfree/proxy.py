import socket
import logging
import sys
import time
import threading

logger = logging.getLogger(__name__)
CONNECTION_TIMEOUT = 10
TOR_PORT = 9050 #9150

class TcpChannel(threading.Thread):
    def __init__(self, conn, outfile):
        threading.Thread.__init__(self)
        self.conn = conn
        self.outfile = outfile
        self._stop_proxy = False

    def run(self):
        with open(self.outfile, "wb") as fd:
            try:
                self.remote_conn = socket.create_connection(("127.0.0.1", TOR_PORT))
                self._proxy(self.remote_conn, fd)
            except Exception as ex:
                logger.error(ex)
            finally:
                self.close()

    def _proxy(self, remote_conn, fd):
        self.conn.setblocking(0)
        remote_conn.setblocking(0)
        lst_msg_received = time.clock()
        while lst_msg_received + CONNECTION_TIMEOUT > time.clock() and not self._stop_proxy:
            p1 = self._read_and_send_all(self.conn, remote_conn, fd)
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
        except KeyboardInterrupt as ex:
            raise ex
        except:
            return False


    def stop(self):
        self._stop_proxy = True

    def close(self):
        if self.remote_conn:
            self.remote_conn.close()
            logger.info('Closing remote socket')
        self.conn.close()
        logger.info('Closing client socket')


class TCP(threading.Thread):
    """
    Copied/Modified from proxy.py github
    """

    def __init__(self, hostname='127.0.0.1', port=8899, backlog=5):
        threading.Thread.__init__(self)
        self.hostname = hostname
        self.port = port
        self.counter = 1
        self.stop = False
        self.backlog = backlog
        self.running = False
        self.results = []

    def consume_results(self):
        r = self.results
        self.results = []
        return r

    def run(self):
        try:
            logger.info('Starting server on port %d' % self.port)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.settimeout(0.5)
            self.socket.bind((self.hostname, self.port))
            self.socket.listen(self.backlog)
            self.threads = []

            while not self.stop:
                self.running = True
                try:
                    conn, addr = self.socket.accept()
                except KeyboardInterrupt as ex:
                    raise ex
                except:
                    continue
                logger.debug('Accepted connection %r at address %r' % (conn, addr))
                outfile = 'caps/%s.cap' % self.counter
                self.results.append(outfile)
                tor = TcpChannel(conn, outfile)
                self.threads.append(tor)
                self.counter += 1
                tor.start()
        except KeyboardInterrupt as e:
            logger.info('Interrupt exception caught. Attempting to shut down gracefully')
        except Exception as e:
            logger.exception('Exception while running the server %r' % e)
        finally:
            logger.info('Closing server socket')
            self.socket.close()
            logger.info('Closing down any threads that may still be alive.')
            for thread in self.threads:
                if thread.is_alive():
                    thread.join(CONNECTION_TIMEOUT)
                if thread.is_alive():
                    logger.info('Encountered a stubborn thread. Attempting close.')
                    thread.stop()
                    thread.join(CONNECTION_TIMEOUT / 2.0)
                if thread.is_alive():
                    raise RuntimeError("Proxy-Thread wont stop.")

    def close(self):
        self.stop = True

    def finished(self):
        return all(not thread.is_alive() for thread in self.threads)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    proxy = TCP()
    proxy.run()
    assert proxy.finished()
