'''
    Created by zxl on 15/7/2.
    Copyright (c) 2015年 zxl. All rights reserved.
'''

import os.path
import json
import subprocess
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.process
from check_answer import * 
import time
from wrap import *

filename = "tmp.txt"            # 可以编辑的文件
editFlag = 0                    # 编辑文件的选项
all_the_text = ""               # 当前渲染的页面
question_num = 0                # 需要解决的题号
path = "\\"                     # Shell所在的路径

'''
    处理文件编辑的接口: edit
    HTTP协议，使用Get方法
    参数：filename = 1.sh
    返回：1.sh的内容
    功能：打开1.sh，并返回其内容
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
    处理文件保存的接口: save
    HTTP协议，使用Post方法
    参数：filename 和 content
    返回：空
    功能：直接将文件保存进所正在编辑的文件
'''

class FileSaveHandler(tornado.web.RequestHandler):

    def get(self):

        pass

    def post(self):

        global filename, editFlag

        content = self.get_argument('file_content','')  #获取content
        fp = open(filename,'w')                         #写文件
        fp.write(content)                               #写入文件内容
        fp.close()
        print(content)
        editFlag = 0                                    #将可编辑选项置为0
        self.render("index.html",tutorial_content = all_the_text)       #重新渲染整个学习网站

        pass

'''
    处理教程显示的接口: tutorial
    HTTP协议，使用Get方法
    参数：教程编号
    返回：空
    功能：将对应的教程载入并渲染出来，此处使用模板
'''
class TutorialEditHandler(tornado.web.RequestHandler):

    def get(self, *d):

        global all_the_text, question_num

        fp = open("tutorial/" + d[0] + ".html")         #打开需要渲染的页面
        question_num = int(d[0])                        #获取题目编号
        try:
            all_the_text = fp.read()                    #读取渲染页面内容
            self.render("index.html",tutorial_content = all_the_text)   #重新渲染整个学习网站
        finally:
            fp.close()

        pass

    def post(self):

        pass


'''
    进行整个页面初始化的接口: init
    HTTP协议，使用Get方法
    参数：无
    返回：空
    功能：初始化整个网站界面
'''
class InitHandler(tornado.web.RequestHandler):

    def get(self, *d):

        global all_the_text

        fp = open("tutorial/0.html")                    #打开需要渲染的页面
        try:
            all_the_text = fp.read()                    #读取渲染页面内容
            self.render("index.html",tutorial_content = all_the_text)   #初始化整个学习网站
        finally:
            fp.close()

        pass

    def post(self):

        pass

'''
    对Shell命令进行管理的接口: Shell
    HTTP协议，使用Get方法
    参数：用户输入的一条Shell指令: line
    返回：该条指令所带来的结果，使用Json，包括:
         file_editor: 是否为启动文件编辑区域
         output: 指令返回内容
         file_content: 文件编辑区域的内容
    功能：执行用户输入的每一条指令，并根据指令产生返回信息，上下文有关
'''
class ShellHandler(tornado.web.RequestHandler):

    def get(self, *d):

        global editFlag, filename, question_num, p, path

        line = self.get_argument('line', '')            #读取网站传递过来的参数line
        print(line)                                     
        file_content = ""                               
        if line.find("myedit") == 0:                    #如果命令是myedit
            editFlag = 1                                #可编辑区域打开
            filename = line[7:]                         #获取可编辑文件名
            filename = path + '/' + filename            #对应到本地文件上
            retStr = ""
            fp = open(filename, 'a')                    #新建本地文件
            fp.close()          
            fp = open(filename)                         #打开本地文件
            try:
                file_content = fp.read()                #获取文件内容
            finally:
                fp.close()
        elif line.find("sudo") != -1:                   #是否是sudo命令，本网站不允许使用sudo
            retStr = "禁止使用sudo"
        else:
            send_all(p, line + '\n')                    #执行命令
            time.sleep(0.02)                            #命令执行
            try:
                ret = recv_some(p)                      #接收命令返回的结果
            except Exception:       
                p = Popen('bash', stdin=PIPE, stdout=PIPE)          #如果出现异常，则重新运行一个bash
                ret = recv_some(p)                      
            retStr = ret.decode()                       #将返回结果进行解码，变成string
            print(ret)

        check_ans_var = CheckAnswer(question_num)       #判断结果思考题question_num是否正确
        if check_ans_var.check_ans(line, retStr):       #根据输入、输出进行判断
            retStr += "\nChallenge Pass\n"              #如果正确则提示Challenge Pass

        self.write(json.dumps({                         #返回结果使用Json格式
            'file_editor': editFlag,
            'output': retStr,
            'file_content': file_content,
        }))

    def post(self):

        pass

    def on_finish(self):

        pass

'''
    显示当前路径的接口: symbol
    HTTP协议，使用Get方法
    参数：无
    返回：当前所处的路径
    功能：返回用户当前使用Shell时所处于的目录
'''
class PwdHandler(tornado.web.RequestHandler):

    def get(self, *d):

        global p, path

        try:
            send_all(p, 'pwd\n')                        #使用pwd命令获取命令
        except Exception:
            p = Popen('bash', stdin=PIPE, stdout=PIPE)
            send_all(p, 'pwd\n')

        time.sleep(0.02)
        ret = recv_some(p)                              #获取路径
        path = ret.decode()[:-1]
        retStr = ret.decode()[:-1] + "$ "               #将路径加上标记并返回
        self.write(retStr)

        pass

    def post(self):

        pass

'''
    配置URL映射关系
    /shell : shell的接口
    /edit : edit的接口
    /save : save的接口
    /symbol : 显示当前路径的接口
    /tutorial : 显示当前教程编号的接口
    此处采用正则表达式进行匹配
'''

application = tornado.web.Application([
    ("/symbol", PwdHandler),
    ("/tutorial/([0-9]+)", TutorialEditHandler),
    ("/shell", ShellHandler),    
    ("/save", FileSaveHandler),
    ("/edit", FileEditHandler),
    ("/()", InitHandler),
    ("/(.*)", tornado.web.StaticFileHandler, {
        "path": os.path.dirname(os.path.realpath(__file__)),
        "default_filename": "index.html",
    }),
], debug=True)

if __name__ == "__main__":

    application.listen(3000)                            #监听3000端口
    p = Popen('bash', stdin=PIPE, stdout=PIPE)          #打开Bash
    tornado.ioloop.IOLoop.current().start()   
    

