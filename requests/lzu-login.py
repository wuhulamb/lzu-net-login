#!/usr/bin/env python3
import os
import math
import json
import hmac
import socket
import base64
import hashlib
import requests
from dotenv import load_dotenv
from urllib.parse import quote

def get_local_ip():
    try:
        # 使用UDP协议创建一个套接字
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个外部地址（如Google DNS服务器）
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]  # 获取本地套接字的IP
    except Exception as e:
        ip = "127.0.0.1"  # 失败则返回回环地址
    finally:
        s.close()
    return ip

def json_response(response):
    res = response.text
    # 提取JSON部分：找到第一个'('和最后一个')'的位置
    start = res.find('(') + 1
    end = res.rfind(')')
    json_str = res[start:end]

    # 将JSON字符串转为字典
    try:
        data_dict = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"解析JSON失败: {e}")
        data_dict = None
    return data_dict

def base64_encode(input_str: str) -> str:
    input_bytes = input_str.encode('utf-8')
    encoded_bytes = base64.b64encode(input_bytes)
    return encoded_bytes.decode('utf-8')

def encode_uri_component(s: str) -> str:
    return quote(
        s,
        safe="!'()*-._~",  # 保留的字符（注意单引号需转义）
        encoding='utf-8',   # 强制使用UTF-8编码
        errors='strict'     # 遇到无法编码的字符抛出异常
    )


def info(d, k):

    def xEncode(s_str, key):
        def s(a, b):
            v = []
            for i in range(0, len(a), 4):
                chunk = a[i:i+4]
                val = 0
                for j in range(len(chunk)):
                    val |= ord(chunk[j]) << (8 * j)
                v.append(val)
            if b:
                v.append(len(a))
            return v

        def l(a, b):
            res = []
            for val in a:
                byte0 = val & 0xFF
                byte1 = (val >> 8) & 0xFF
                byte2 = (val >> 16) & 0xFF
                byte3 = (val >> 24) & 0xFF
                res.append(chr(byte0))
                res.append(chr(byte1))
                res.append(chr(byte2))
                res.append(chr(byte3))
            res_str = ''.join(res)
            if b:
                if not a:
                    return ''
                m = a[-1]
                res_str = res_str[:m]
            return res_str

        if not s_str:
            return ""
        
        v = s(s_str, True)
        k = s(key, False)
        
        # 扩展k到长度4，不足补0
        if len(k) < 4:
            k += [0] * (4 - len(k))
        
        n = len(v) - 1
        if n < 0:
            return []
        
        z = v[n] & 0xFFFFFFFF
        y = v[0] & 0xFFFFFFFF
        c = 0x9E3779B9
        q = int(math.floor(6 + 52 / (n + 1)))
        d = 0
        
        for _ in range(q):
            d = (d + c) & 0xFFFFFFFF
            e = (d >> 2) & 3
            
            for p in range(n):
                y_val = v[p + 1] & 0xFFFFFFFF
                z_val = z
                
                # 计算m
                m_term1 = ((z_val >> 5) ^ (y_val << 2)) & 0xFFFFFFFF
                term2_part1 = ((y_val >> 3) ^ (z_val << 4)) & 0xFFFFFFFF
                term2 = (term2_part1 ^ ((d ^ y_val) & 0xFFFFFFFF)) & 0xFFFFFFFF
                m = (m_term1 + term2) & 0xFFFFFFFF
                
                key_index = ((p & 3) ^ e)
                key_val = k[key_index] & 0xFFFFFFFF
                term3 = (key_val ^ z_val) & 0xFFFFFFFF
                m = (m + term3) & 0xFFFFFFFF
                
                new_val = (v[p] + m) & 0xFFFFFFFF
                v[p] = new_val
                z = new_val
            
            # 处理最后一个元素v[n]
            y_val = v[0] & 0xFFFFFFFF
            z_val = z
            
            m_term1 = ((z_val >> 5) ^ (y_val << 2)) & 0xFFFFFFFF
            term2_part1 = ((y_val >> 3) ^ (z_val << 4)) & 0xFFFFFFFF
            term2 = (term2_part1 ^ ((d ^ y_val) & 0xFFFFFFFF)) & 0xFFFFFFFF
            m = (m_term1 + term2) & 0xFFFFFFFF
            
            p_val = n
            key_index = ((p_val & 3) ^ e)
            key_val = k[key_index] & 0xFFFFFFFF
            term3 = (key_val ^ z_val) & 0xFFFFFFFF
            m = (m + term3) & 0xFFFFFFFF
            
            new_val = (v[n] + m) & 0xFFFFFFFF
            v[n] = new_val
            z = new_val
        
        # 返回处理后的v数组，假设l函数处理此处结果
        return l(v, False)

    CUSTOM_ALPHABET = 'LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA'
    # 生成JSON字符串，紧凑模式无空格
    json_str = json.dumps(d, separators=(',', ':'))
    # 转换为UTF-8字节并处理为字符序列
    json_bytes = json_str.encode('utf-8')
    str_processed = ''.join(chr(b) for b in json_bytes)
    # 处理密钥
    key_bytes = k.encode('utf-8')
    key_processed = ''.join(chr(b) for b in key_bytes)
    # 执行xEncode加密
    x_encoded = xEncode(str_processed, key_processed)
    # 转换为字节序列进行Base64编码
    x_bytes = bytes(ord(c) for c in x_encoded)
    # 标准Base64编码并去除填充
    encoded_standard = base64.b64encode(x_bytes).decode('ascii')
    # 转换为自定义字母表
    custom_trans = str.maketrans(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',
        CUSTOM_ALPHABET
    )
    encoded_custom = encoded_standard.translate(custom_trans)
    # 添加前缀并返回
    return "{SRBX1}" + encoded_custom

def hmac_md5(key, token):
    return hmac.new(key.encode('utf-8'), token.encode('utf-8'), hashlib.md5).hexdigest()

def sha1(key):
    message = key.encode('utf-8')
    hash_object = hashlib.sha1(message)  # 注意要传入 bytes 类型
    return hash_object.hexdigest()    # 输出 16 进制字符串

# ================================================= #

# 获取当前脚本的绝对路径（如果是符号链接，解析真实路径）
script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)

# 拼接 .env 文件的路径
env_path = os.path.join(script_dir, ".env")

# 显式加载指定路径的 .env
load_dotenv(dotenv_path=env_path)

username = os.getenv("username") + "@study"
password = os.getenv("password")
password = base64_encode(encode_uri_component(password))
my_ip = get_local_ip()

# ================================================= #

f_url = "http://10.10.0.166/cgi-bin/get_challenge"

f_params = {
    "callback": "jQuery",
    "username": username,  # @符号会自动编码为 %40
    "ip": my_ip,
}

f_headers = {
    "Host": "10.10.0.166",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Referer": "http://10.10.0.166/srun_portal_pc?ac_id=2&theme=lzu&srun_domain=&srun_domain=@study&srun_domain=",
    "Cookie": "lang=zh-CN",
    "Priority": "u=0"
}

f_response = requests.get(
    f_url,
    params=f_params,
    headers=f_headers,
    verify=False  # 如果服务器使用自签名证书需要加这个参数
)

#print(f_response.status_code)
#print(response.text)

f_data_dict = json_response(f_response)
challenge = f_data_dict["challenge"]
# ================================================= #

data = {
    "username": username,
    "password": password,
    "ip": my_ip,
    "acid": "2",
    "enc_ver": "srun_bx1",
}
p_info = info(data, challenge)

url = "http://10.10.0.166/cgi-bin/srun_portal"
hmd5 = hmac_md5(password, challenge)
md5_password = "{MD5}" + hmd5

chkstr = challenge + username
chkstr += challenge + hmd5
chkstr += challenge + "2"
chkstr += challenge + my_ip
chkstr += challenge + "200"
chkstr += challenge + "1"
chkstr += challenge + p_info
chksum = sha1(chkstr)

params = {
    "callback": "jQuery",
    "action": "login",
    "username": username,
    "password": md5_password,
    "ac_id": "2",
    "ip": my_ip,
    "chksum": chksum,
    "info": p_info,
    "n": "200",
    "type": "1",
    "os": "Linux",
    "name": "Linux",
    "double_stack": "0",
    #"_": "1745847589381"
}

headers = {
    "Host": "10.10.0.166",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Referer": "http://10.10.0.166/srun_portal_pc?ac_id=2&theme=lzu&srun_domain=&srun_domain=@study&srun_domain=",
    "Cookie": "lang=zh-CN"
}

response = requests.get(
    url,
    params=params,
    headers=headers,
    verify=False  # 跳过 SSL 验证（如果是 HTTPS）
)

#print(f"Status Code: {response.status_code}")
#print(f"Response Text: {response.text}")

login_res = json_response(response)
if login_res["res"] == "ok":
    print("Connect lzu net successfully!")
else:
    print("Connect lzu net fail ...")
