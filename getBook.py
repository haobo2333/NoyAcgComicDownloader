import getBookInfo
import getImg
import sanitizePath
from pathlib import Path

def getBook(bid:int,cookies:str,path:str,bookinfo:dict):
    info = getBookInfo.getBookInfo(cookies=cookies,bid=bid)
    for i in range(1,info['Len']+1):
        bookinfo['page'] = i
        fullpath = path.format_map(bookinfo)
        sanitize_fullpath = sanitizePath.sanitize_path(fullpath)
        objpath = Path(sanitize_fullpath)
        objpath.parent.mkdir(parents=True,exist_ok=True)
        content = getImg.getImg(bid=bid,page=i)
        with open(sanitize_fullpath,"wb")as f:
            f.write(content)