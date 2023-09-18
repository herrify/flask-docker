#!/usr/bin/python3

import http
import json
from enum import Enum
import requests
from retrying import retry

class HostAgents(Enum):
    OPENAI_OFFICIAL_HOST = "chat.openai.com"

    API_REQUEST_CODE_SUCCESS = 200
    API_REQUEST_CODE_FAIL = 201
    API_REQUEST_CODE_TIMEOUT = 408

class OpenChatRequest():
    @staticmethod
    def chatHTTPSRequest(content, apiHost, apiKey):
        payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            { "role" : "user", "content": content }
        ]
        })
        headers = {
        'Authorization': "Bearer {}".format(apiKey),
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
        }
        try:
            conn = http.client.HTTPSConnection(apiHost)
            conn.request("POST", "/v1/chat/completions", payload, headers)
            res = conn.getresponse()
            data = res.read()
            return data.decode("utf-8")
        except http.client.HTTPException as e:
            return HostAgents.API_REQUEST_CODE_FAIL.value
    
    @staticmethod
    def getAccessToken():
        """
        使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
        """
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={HostAgents.BAIDUBCE_API_KEY.value}&client_secret={HostAgents.BAIDUBCE_API_SECRECT.value}"
        payload = json.dumps("")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("access_token")
    
    
class OpenChatProxy(object):

    @staticmethod
    def chatAnyWhere(content):
        chatRes = OpenChatRequest.chatHTTPSRequest(content, HostAgents.CHATANYWHERE_PROXY_HOST.value, HostAgents.CHATANYWHERE_PROXY_KEY.value)
        contentDict = json.loads(chatRes)
        return contentDict['choices'][0]['message']['content']
    
    @staticmethod
    def chatOpenAiProxy(content):
        return OpenChatRequest.chatHTTPSRequest(content, HostAgents.OPENAI_PROXY_HOST.value, HostAgents.OPENAI_OFFICIAL_KEY.value)
    
    @staticmethod
    def baiduIceChat(content):
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + OpenChatRequest.getAccessToken()
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response = response.text
        except Exception as e:
            response = HostAgents.API_REQUEST_CODE_FAIL.value
        return response