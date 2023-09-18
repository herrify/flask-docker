from flask import Flask, request,jsonify,json
from flask_cors import CORS, cross_origin
from openchat import OpenChatProxy, HostAgents
import time
import json
import socket
socket.setdefaulttimeout(8)

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
Cors = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/unionChat", methods=["POST","GET"])
def submitData():
    timeStart = time.time()
    try:
        code = HostAgents.API_REQUEST_CODE_SUCCESS.value
        data = ""
        msg = ""
        useTime = 0
        requestJson = request.get_json()
        requestContent = requestJson["content"]
        requestType = requestJson["type"]
        if requestType == "chatGPT":
            data = chatAnyWhere(requestContent)
        elif requestType == "ai360":
            data = ai360Chat(requestContent)
        elif requestType == "baiduIce":
            requestRes = baiduIceChat(requestContent)
            contentDict = json.loads(requestRes)
            data = contentDict["result"]
        else:
            data = chatAnyWhere(requestContent)
        if data == HostAgents.API_REQUEST_CODE_FAIL.value:
            code = HostAgents.API_REQUEST_CODE_FAIL.value
            msg = "Api Request Failed"
    except socket.timeout:
        code = HostAgents.API_REQUEST_CODE_TIMEOUT.value
        msg = "Api Request Timeout"
    except Exception as e:
        code = HostAgents.API_REQUEST_CODE_FAIL.value
        msg = "Api Request Failed"
    timeEnd = time.time()
    useTime = timeEnd - timeStart
    try:
        return jsonify({"code": code, "data": {"reply": data}, "msg": msg, "useTime": useTime})
    except Exception as e:
        return jsonify({"code": 201, "data": "", "msg": "", "useTime": useTime})

@app.route("/baiduIce", methods=["POST","GET"])
def baiduIce():
    requestJson = request.get_json()
    requestContent = requestJson['content']
    if not requestContent:
        requestContent = "hello ,self introduce in Chinese please"
    content = baiduIceChat(requestContent)
    return content.text


def chatAnyWhere(content):
    return OpenChatProxy.chatAnyWhere(content)

def chatOpenAI(content):
    return OpenChatProxy.chatOpenAiProxy(content)

def baiduIceChat(content):
    return OpenChatProxy.baiduIceChat(content)

def ai360Chat(content):
    return OpenChatProxy.ai360Chat(content)


if __name__ == '__main__':
    app.run(debug=True)