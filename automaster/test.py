import http.client
import json
import datetime
import hashlib
import uuid
import time
import urllib3
import urllib.request
import urllib.error
import urllib.parse
import threading
import queue
import threading, time

fileq = queue.Queue()

appid_default = 'HR-PROD-GEN000'
secret_default = '81755146-5f01-44a5-b2ae-5fdf7cedbae9'
url_token = 'token.speech.horizon.ai'
url_pack = 'speech.pack.horizon.ai'
deviceID = '9990000000000031'

audio_list = ''
filename_list = []
# audio_file = 'D:develop/201902/交接/测试/packs.pcm'
audio_file = './packs.pcm'


# audio_file = './test1.pcm'


# fileq = queue.LifoQueue()

def get_token(deviceid, url=url_token, appid=appid_default, secret=secret_default):
    """使用http.client模块发送post请求获取token"""
    headers = {'Content-Type': 'application/json'}  # 定义headers
    timestamp = int(time.mktime(datetime.datetime.now().timetuple()))  # 获取当前时间戳
    hl = hashlib.md5()
    hl.update((appid + secret + deviceid + str(timestamp)).encode(encoding='utf-8'))
    signature = str(hl.hexdigest())  # signature为md5加密字符串
    body = {
        'appID': appid,
        'deviceID': deviceid,
        'timestamp': timestamp,
        'signature': signature
    }
    print(body)
    try:
        conn = http.client.HTTPConnection(url, port=80)
        conn.request(method='POST', url='/token', body=json.dumps(body), headers=headers)
        response = conn.getresponse()
        if not response.isclosed():
            resp_str = response.read().decode('utf-8')
            print(resp_str)
            resp_json = json.loads(resp_str)
            token = resp_json['result']['token']
            print(token)
            response.close()
            conn.close()
            return token
    except Exception as err:
        print(str(err))


def urllib3_post(deviceid, token, appid=appid_default, url=url_pack):
    '''使用urllib3模块发送post请求'''
    identify, idx, data = fileq.get()
    print(idx)
    headers = {'appID': appid,
               'deviceID': deviceid,
               'token': token,
               'Content-Type': 'audio/pcm;bit=16;rate=16000',
               'identify': identify,
               # 'horRealFlag': 0,
               'index': idx,
               # 'uniqueID': 'tangchen-test',
               }
    http = urllib3.PoolManager(num_pools=10, timeout=urllib3.Timeout(connect=3.0, read=10.0),
                               retries=3)
    response = http.request(method='POST', url=url, body=data, headers=headers)
    print(str(idx) + ' ' + response.data.decode('utf-8'))


# def urllib_post(deviceid, token, appid=appid_default, url=url_pack):
#     '''使用urllib模块发送post请求'''
#     identify, idx, data = fileq.get()
#     headers = {'appID': appid,
#                'deviceID': deviceid,
#                'token': token,
#                'Content-Type': 'audio/pcm;bit=16;rate=16000',
#                'identify': identify,
#                'index': idx
#                }
#     try:
#         req = urllib.request.Request(url=url, data=data, headers=headers)
#         resp = urllib.request.urlopen(req)
#         resp_str = str(resp.read(), encoding='utf-8')
#         resp_json = json.loads(resp_str)
#         print(str(idx) + ' ' + resp_str)
#         if idx < 0:
#             return resp_json
#     except (urllib.error.HTTPError, urllib.error.URLError) as err:
#         print(str(err))
#         return 0


def get_filename(listfile):
    '''从目录文件中读取子文件名
     for i in range(10):
        filename = get_filename('list_file').__next__()
        print(filename)
    '''
    if not filename_list:
        with open(listfile, 'r') as f:
            for line in f.readlines():
                if line not in ('', '\n', '\r\n'):
                    filename_list.append(line.split('\n')[0])
    try:
        yield filename_list.pop(0)
    except StopIteration:
        pass


def read_file(file):
    '''读文件，并将该文件对应的uuid、文件块index、文件块data保存至queue队列'''
    with open(file, 'rb') as f:
        ID = str(uuid.uuid4())
        idx = 0
        while idx >= 0:
            pack = f.read(2048)
            idx += 1
            if len(pack) == 0:
                idx = -idx
            fileq.put([ID, idx, pack])


if __name__ == '__main__':
    token = get_token(deviceID)
    read_file(audio_file)
    while fileq.qsize():
        t = threading.Thread(target=urllib3_post, args=(deviceID,token))
        t.start()
        # urllib3_post(deviceID, token)
