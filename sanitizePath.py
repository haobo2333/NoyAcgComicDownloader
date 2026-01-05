import re
import os
from pathlib import Path

def sanitize_path(input_path: str) -> str:
    """
    将输入路径中不符合命名规范的部分替换为 '_'
    """
    path_obj = Path(input_path)
    parts = list(path_obj.parts)
    invalid_chars_re = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
    
    reserved_names = {
        "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", 
        "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", 
        "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    sanitized_parts = []
    
    for i, part in enumerate(parts):
        if i == 0 and (part.endswith('\\') or part == '/'):
            sanitized_parts.append(part)
            continue
        new_part = invalid_chars_re.sub('_', part)
        new_part = new_part.strip(' .')
        if not new_part:
            new_part = "_"
        base_name = new_part.split('.')[0].upper()
        if base_name in reserved_names:
            new_part = "_" + new_part

        sanitized_parts.append(new_part)
    return str(Path(*sanitized_parts))