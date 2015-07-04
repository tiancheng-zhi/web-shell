#!/usr/bin/python3
import os.path
import json
import subprocess
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.process

class ShellWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")
        self.shell = tornado.process.Subprocess(["bash", "-i"],
            stdin=tornado.process.Subprocess.STREAM,
            stdout=tornado.process.Subprocess.STREAM,
            stderr=subprocess.STDOUT
        )
        def read_callback(data):
            self.write_message(data)
            self.shell.stdout.read_bytes(4096, read_callback, partial=True)
        self.shell.set_exit_callback(lambda p: self.close())
        self.shell.stdout.read_bytes(4096, read_callback, partial=True)

    def on_message(self, message):
        if len(message) == 1:
            self.shell.stdin.write(message.encode())

    def on_close(self):
        print("WebSocket closed")
        if self.shell.proc.poll() == None:
            self.shell.proc.kill()
        self.shell.proc.wait()

application = tornado.web.Application([
    ("/shell", ShellWebSocket),
    ("/(.*)", tornado.web.StaticFileHandler, {
        "path": os.path.dirname(os.path.realpath(__file__)),
        "default_filename": "index.html",
    }),
], debug=True)

if __name__ == "__main__":
    application.listen(3000)
    tornado.ioloop.IOLoop.current().start()
