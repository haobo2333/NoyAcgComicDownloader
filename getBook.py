import getImg
import sanitizePath
from pathlib import Path


def getBook(bid: int, path: str, bookinfo: dict):
    try:
        for i in range(1, bookinfo['Len']+1):
            bookinfo['page'] = i
            fullpath = path.format_map(bookinfo)
            sanitize_fullpath = sanitizePath.sanitize_path(fullpath)
            objpath = Path(sanitize_fullpath)
            objpath.parent.mkdir(parents=True, exist_ok=True)
            content = getImg.getImg(bid=bid, page=i)
            with open(sanitize_fullpath, "wb")as f:
                f.write(content)
    except Exception as e:
        return str(e)
