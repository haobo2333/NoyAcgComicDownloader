import requests
import re
import os

def getImg(bid: str, page: int):
    '''
    getImg 的 Docstring
    
    :param bid: 漫画编号
    :type bid: str
    :param page: 漫画页码
    :type page: int
    '''
    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'Referer': 'https://noy1.top/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'DNT': '1',
    }
    
    try:
        response = requests.get(f'https://img.noy.asia/{bid}/{page}.webp', headers=headers, timeout=15)
        response.raise_for_status()
            
        return response.content
        
    except Exception as e:
        return str(e)