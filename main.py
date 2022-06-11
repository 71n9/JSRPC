import time
import json
from flask_sockets import Sockets
from gevent import monkey
from flask import Flask
from flask import request

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

monkey.patch_all()
app = Flask(__name__)
sockets = Sockets(app)

browserDic = {}
resultDic = {}


@sockets.route('/ws')
def echoSocket(ws):
    while not ws.closed:

        message = ws.receive()  # 接收消息
        if message is None:
            print("浏览器关闭:", id(ws))
            continue

        msgDate = message.decode("utf-8")

        data = json.loads(msgDate)

        if data["msg"] == "register":
            browserDic[data["browser"]] = ws
            print(f"注册{data['browser']}浏览器成功:{id(browserDic)}")

        if data["msg"] == "result":
            resultDic[data["resultId"]] = data["result"]


@app.route('/get')
def get():
    browser = request.args.get('browser')
    fun = request.args.get('fun')
    arg = request.args.get('arg')

    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    response = {"success": False, "msg": "未注册或已关闭！", "date": nowTime}

    if not (browser and fun and arg):
        print(browser, fun, arg)
        response["msg"] = "错误的请求方式！正确示例: http://127.0.0.1:5000/get?browser=%E7%99%BE%E5%BA%A6&fun=getHostName&arg=[1,2]"
        return response

    if browser in browserDic.keys():
        t = time.time()
        resultId = str(int(t * 10000))
        alreadySend = False

        # 15秒未返回结果自动结束
        while (time.time() - t) < 15:

            if browserDic[browser].closed:
                browserDic.pop(browser)

                return response

            if not alreadySend:
                data = {"exec": fun, "arg": arg, "resultId": resultId}

                browserDic[browser].send(json.dumps(data))
                alreadySend = True

            if resultId in resultDic.keys():
                response["success"] = True
                response["data"] = resultDic[resultId]
                response["msg"] = fun
                print(f"{nowTime} 调用成功:{response}")
                return response

            time.sleep(0.1)

        response["msg"] = "超出指定时间未接收到结果！"

    return response


def run(host, prot):
    server = pywsgi.WSGIServer((host, prot), app, handler_class=WebSocketHandler)
    print(f'server start at {host}:{prot}')
    server.serve_forever()


if __name__ == "__main__":
    host = "127.0.0.1"
    prot = 5000
    run(host, prot)
