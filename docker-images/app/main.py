from flask import Flask, request,jsonify,json
from flask_cors import CORS, cross_origin
from openchat import OpenChatProxy

app = Flask(__name__)
Cors = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/gptChat", methods=["POST","GET"])
def submitData():
    requestJson = request.get_json()
    requestContent = requestJson['content']
    if not requestContent:
        requestContent = "hello ,how to say 'I am not happy' in Chinese?"
    content = chatAnyWhere(requestContent)
    return content

@app.route("/baiduIce", methods=["POST","GET"])
def baiduIce():
    requestJson = request.get_json()
    requestContent = requestJson['content']
    if not requestContent:
        requestContent = "hello ,how to say 'I am not happy' in Chinese?"
    content = baiduIceChat(requestContent)
    return content.text


def chatAnyWhere(content):
    return OpenChatProxy.chatAnyWhere(content)

def baiduIceChat(content):
    return OpenChatProxy.baiduIceChat(content)


if __name__ == '__main__':
    app.run(debug=True)