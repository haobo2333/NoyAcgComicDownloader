import requests


def getBookInfo(cookies: str, bid: int):
    '''
    getBookInfo 的 Docstring

    :param cookies: 用户Cookie
    :type cookies: str
    :param bid: 漫画编号
    :type bid: int
    '''
    cookies = {
        'NOY_SESSION': cookies
    }

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
        # 'cookie': 'NOY_SESSION=MTc2NzM0NzAxMHxOd3dBTkZWWVRUWXlRa015V0VVM1VrdzJRVE0wTWs5WE56Sk9VVXhJTkUxUk1qUlBRekpITnpWVlZVUlZNa2czVkZOT1RGSTNXVkU9fA1qTj40pDf6HEzOAtBy7vxcq-dBSHxo4uZTkWWr0Rkx; _ga=GA1.1.337070843.1767347085; _ga_8XQD6ESY5R=GS2.1.s1767347084$o1$g0$t1767347084$j60$l0$h0',
    }

    data = {
        'bid': bid
    }

    response = requests.post(
        'https://noy1.top/api/getbookinfo', headers=headers, cookies=cookies, data=data)
    text = response.json()
    return text
