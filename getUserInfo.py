import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,tr;q=0.5',
    'content-type': 'application/x-www-form-urlencoded',
    'dnt': '1',
    'origin': 'https://noy1.top',
    'priority': 'u=1, i',
    'referer': 'https://noy1.top/',
    'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
}


def getUserInfo(cookie: str):
    '''
    getUserInfo 的 Docstring

    :param cookie: 用户Cookie
    :type cookie: str
    '''
    cookie = {
        'NOY_SESSION': cookie
    }

    response = requests.post(
        'https://noy1.top/api/userinfo_v2', headers=headers, cookies=cookie)
    text = response.json()
    return text