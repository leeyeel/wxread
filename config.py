# config.py 自定义配置,包括阅读次数、推送token的填写
import os
import re

"""
可修改区域
默认使用本地值如果不存在从环境变量中获取值
"""

# 阅读次数 默认40次/20分钟
READ_NUM = int(os.getenv('READ_NUM') or 40)
# 需要推送时可选，可选pushplus、wxpusher、telegram
PUSH_METHOD = "" or os.getenv('PUSH_METHOD')
# pushplus推送时需填
PUSHPLUS_TOKEN = "" or os.getenv("PUSHPLUS_TOKEN")
# telegram推送时需填
TELEGRAM_BOT_TOKEN = "" or os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "" or os.getenv("TELEGRAM_CHAT_ID")
# wxpusher推送时需填
WXPUSHER_SPT = "" or os.getenv("WXPUSHER_SPT")
# read接口的bash命令，本地部署时可对应替换headers、cookies
curl_str = os.getenv('WXREAD_CURL_BASH')

# headers、cookies是一个省略模版，本地或者docker部署时对应替换
cookies = {
    'RK': 'oxEY1bTnXf',
    'ptcz': '53e3b35a9486dd63c4d06430b05aa169402117fc407dc5cc9329b41e59f62e2b',
    'pac_uid': '0_e63870bcecc18',
    'iip': '0',
    '_qimei_uuid42': '183070d3135100ee797b08bc922054dc3062834291',
    'wr_avatar': 'https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FeEOpSbFh2Mb1bUxMW9Y3FRPfXwWvOLaNlsjWIkcKeeNg6vlVS5kOVuhNKGQ1M8zaggLqMPmpE5qIUdqEXlQgYg%2F132',
    'wr_gender': '0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ko;q=0.5',
    'baggage': 'sentry-environment=production,sentry-release=dev-1730698697208,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=1ff5a0725f8841088b42f97109c45862',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
}


# 书籍
book = [
    "24a320007191987a24a4603","ce032b305a9bc1ce0b0dd2a","43f3229071984b9343f04a4","d7732ea0813ab7d58g0184b8",
    "3d03298058a9443d052d409","4fc328a0729350754fc56d4","a743220058a92aa746632c0","140329d0716ce81f140468e",
    "1d9321c0718ff5e11d9afe8","ff132750727dc0f6ff1f7b5","e8532a40719c4eb7e851cbe","9b13257072562b5c9b1c8d6"
]

# 章节
chapter = [
    "1d7328e029a1d7f7abc1af1","37a32ae029837a749d80032","47d328e029447d1e9905d2b","e96328f02dae96ed478dde6",
    "63d32d402d963dc7ed1006e","9fc324302859fc3d71522e0","65d3230028465ded535348f","65d3230028465ded535348f",
    "3de32dd027d3def184ad06e","4c5327a02794c56ff4ce24c","ca4326502d6ca46c1b957c7","7f632b502707f6ffaa6bf2e",
    "153323102d41534b76d32fa","f09320f026af0935e4cd23d","eb1327402d3eb1637279cc9","7e7327a02a67e7757b1e50a"
]

"""
建议保留区域|默认读三体，其它书籍自行测试时间是否增加
"""
data = {
    "appId": "wb182564874663h45195495",
    "b": "24a320007191987a24a4603",
    "c": "37a32ae029837a749d80032",
    "ci": 51,
    "co": 338,
    "sm": "第一部前往拜访公爵夫妇的那天（盖尔芒特亲",
    "pr": 0,
    "rt": 16,
    "ts": 1752257861106,
    "rn": 232,
    "sg": "132dfeb3cdc96c0d0a3442a1cc9cef1904b6d1ba8f011e2f6556ea15391cc0e1",
    "ct": 1752257861,
    "ps": "15e320507a71bba2g013f19",
    "pc": "f2c326a07a71bba2g015374",
    "s": "36cc0815"
}


def convert(curl_command):
    """提取bash接口中的headers与cookies
    支持 -H 'Cookie: xxx' 和 -b 'xxx' 两种方式的cookie提取
    """
    # 提取 headers
    headers_temp = {}
    for match in re.findall(r"-H '([^:]+): ([^']+)'", curl_command):
        headers_temp[match[0]] = match[1]

    # 提取 cookies
    cookies = {}
    
    # 从 -H 'Cookie: xxx' 提取
    cookie_header = next((v for k, v in headers_temp.items() 
                         if k.lower() == 'cookie'), '')
    
    # 从 -b 'xxx' 提取
    cookie_b = re.search(r"-b '([^']+)'", curl_command)
    cookie_string = cookie_b.group(1) if cookie_b else cookie_header
    
    # 解析 cookie 字符串
    if cookie_string:
        for cookie in cookie_string.split('; '):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
    
    # 移除 headers 中的 Cookie/cookie
    headers = {k: v for k, v in headers_temp.items() 
              if k.lower() != 'cookie'}

    return headers, cookies


headers, cookies = convert(curl_str) if curl_str else (headers, cookies)
