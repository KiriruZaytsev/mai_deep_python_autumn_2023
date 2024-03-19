
import socket
import threading
import queue
import re
import json
import sys
import argparse
from collections import Counter
import requests


class Server:
    def __init__(self, w_count=1, com_count=1, host=socket.gethostname(), port=5000):
        print(f'Server ip:{host}, port:{port}')
        self.w_count = w_count
        self.com_count = com_count
        self.lock = threading.Lock()
        self.url_count = 0
        self.que = queue.Queue(self.w_count * 2)
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ser.bind((host, port))
        self.ser.listen(self.w_count + 1)

    def sender(self, json_str, url):
        user = self.ser.accept()[0]
        msg = url + '~' + json_str
        user.send('Worker'.encode('utf-8'))
        if user.recv(1024).decode('utf-8') == "Ready":
            user.send(msg.encode('utf-8'))
            self.url_count += 1
        user.close()

    def start_server(self):
        user = self.ser.accept()[0]
        user.send("User has been connected".encode('utf-8'))
        user.close()

        master_tr = threading.Thread(
                target=self.master,
            )
        master_tr.start()
        master_tr.join()
        self.ser.close()
        print("End")

    def worker(self):
        while True:
            try:
                url = self.que.get(timeout=1)
            except queue.Empty:
                continue
            if url is None:
                print("Worker has stopped")
                break
            try:
                request = requests.get(url, timeout=10)
                if request.status_code != 200:
                    continue
            except requests.exceptions.RequestException:
                print(f'Exception: {str(requests.exceptions.RequestException)}')
                continue
            http = request.text
            word_list = re.findall('[a]+', http, flags=re.IGNORECASE)
            freq = Counter(word_list).most_common(self.com_count)
            js_freq = json.dumps(dict(freq))
            self.sender(js_freq, url)
            with self.lock:
                print(f"Number of processed urls is: {self.url_count}")

    def master(self):
        worker_tr = [
            threading.Thread(
                target=self.worker,
            )
            for _ in range(self.w_count)
        ]

        for thread in worker_tr:
            thread.start()

        while True:
            user = self.ser.accept()[0]
            user.send("Master".encode('utf-8'))

            try:
                data = user.recv(1024)
            except ConnectionError:
                print("ConnectionError")
                break

            if data.decode('utf-8') == 'Stop':
                print("Server has stopped")
                for _ in range(self.w_count):
                    self.que.put(None)
                break
            if len(data) > 0:
                url = data.decode('utf-8')[:-1]
                self.que.put(url)
            else:
                for _ in range(self.w_count):
                    self.que.put(None)
                break

            user.close()
        user.close()

        for thread in worker_tr:
            thread.join()

    def close_server(self):
        self.ser.shutdown(socket.SHUT_RDWR)
        self.ser.close()


class User:
    def __init__(self, thread_count, file: str, host=socket.gethostname(), port=5000):
        self.file = file
        self.thread_count = thread_count
        self.host = host
        self.port = port
        self.que = queue.Queue(self.thread_count * 2)

    def connection(self):
        ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ser.connect((self.host, self.port))
        try:
            msg = ser.recv(1024).decode('utf-8')
        except ConnectionResetError:
            print('ConnectionResetError')
            msg = 'Exit'
        if msg == 'CLinet is connected!':
            print(msg)
            threads = [
                threading.Thread(
                    target=self.listen,
                )
                for _ in range(self.thread_count)
            ]

            for thread in threads:
                thread.start()

            self.queue_generate()

            for thread in threads:
                thread.join()
        else:
            print("Wrong connection message from Server")
        ser.close()

    def queue_generate(self):
        with open(self.file, 'r', encoding='utf-8') as text:
            for line in text:
                self.que.put(line)
        for _ in range(self.thread_count):
            self.que.put(None)

    def listen(self):
        while True:
            try:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.connect((self.host, self.port))
                msg = server.recv(1024).decode('utf-8')
            except (ConnectionResetError, ConnectionRefusedError):
                server.close()
                break
            if msg == 'Master':
                url = self.que.get(timeout=1)
                if url is None:
                    break
                server.send(url.encode('utf-8'))
            elif msg == 'Worker':
                server.send('Ready'.encode('utf-8'))
                url, json_str = server.recv(1024).decode('utf-8').split('~', 1)
                print(f'{url}: {json_str}')
            server.close()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=int, default=1)
    parser.add_argument('-k', type=int, default=1)
    return parser


if __name__ == '__main__':
    namespace = create_parser().parse_args(sys.argv[1:])
    w = namespace.w
    k = namespace.k
    Server(w, k).start_server()
    try:
        data_to_connect = int(sys.argv[1])
        file_name = sys.argv[2]
    except IndexError:
        raise IndexError
    User(data_to_connect, file_name).connection()