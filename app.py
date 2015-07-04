import os.path
import json
import subprocess
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.process
from check_answer import *

'''
    处理shell的接口
    WebSocket协议
'''
class ShellWebSocket(tornado.websocket.WebSocketHandler):
    def open(self,*d):
        print(d);
        if len(d) == 2:
            userid = d[0]
            challenge_num = d[1]
        checkAnswer = CheckAnswer(challenge_num);

        print("WebSocket opened")

        self.shell = tornado.process.Subprocess(["bash", "-i"],
            stdin=tornado.process.Subprocess.STREAM,
            stdout=tornado.process.Subprocess.STREAM,
            stderr=subprocess.STDOUT
        )
        def read_callback(data):
            #self.write_message(json.dumps({
            #    'type': 'output',
            #    'data': data,
            #    }))
            self.write_message(data)
            self.shell.stdout.read_bytes(4096, read_callback, partial=True)

        self.shell.set_exit_callback(lambda p: self.close())
        self.shell.stdout.read_bytes(4096, read_callback, partial=True)

    def on_message(self, message):
        if len(message) == 1:
            self.shell.stdin.write(message.encode())
        if True:
            pass

    def on_close(self):
        print("WebSocket closed")
        if self.shell.proc.poll() == None:
            self.shell.proc.kill()
        self.shell.proc.wait()

'''
    处理文件编辑的接口:edit
    HTTP协议，使用Get方法
    参数：filename = 1.sh
    返回：1.sh的内容
'''

class FileEditHandler(tornado.web.RequestHandler):
    def get(self):
        filename = self.get_argument('filename','')     #获取参数的值
        fp = open(filename)                             #本地打开文件
        try:
            all_the_text = fp.read()                    #读取文件内容
            self.write(all_the_text)                    #返回文件内容
        finally:
            fp.close()                                  #关闭文件

    def post(self):
        pass

'''
    处理文件保存的接口:save
    HTTP协议，使用Post方法
    参数：filename 和 content
    返回：空
'''

class FileSaveHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        filename = self.get_argument('filename','')     #获取filename
        content = self.get_argument('content','')       #获取content
        fp = open(filename,'w')                         #写文件
        fp.write(content)
        fp.close()
        pass

class TutorialEditHandler(tornado.web.RequestHandler):
    def get(self, *d):
        fp = open("tutorial/" + d[0] + ".html")                                 #本地打开文件
        try:
            all_the_text = fp.read()                    #读取文件内容
            self.render("index.html",tutorial_content = all_the_text, file_edit = true)
        finally:
            fp.close()
        pass

    def post(self):
        pass

class InitHandler(tornado.web.RequestHandler):
    def get(self, *d):
        fp = open("tutorial/0.html")                    #本地打开文件
        try:
            all_the_text = fp.read()                    #读取文件内容
            self.render("index.html",tutorial_content = all_the_text, file_edit = true)
        finally:
            fp.close()
        pass

    def post(self):
        pass
        
'''
    配置URL映射关系
    /shell/[^/]*/[^/]* : shell的接口
    /edit : edit的接口
    /save : save的接口
'''

application = tornado.web.Application([
    ("/tutorial/([0-9]+)", TutorialEditHandler),
    ("/shell/([^/]*)/([^/]*)", ShellWebSocket),             
    ("/edit", FileEditHandler),
    ("/save", FileSaveHandler),
    ("/()", InitHandler),
    ("/(.*)", tornado.web.StaticFileHandler, {
        "path": os.path.dirname(os.path.realpath(__file__)),
        "default_filename": "index.html",
    }),
], debug=True)

if __name__ == "__main__":
    application.listen(3000)                            #监听3000端口
    tornado.ioloop.IOLoop.current().start()             
