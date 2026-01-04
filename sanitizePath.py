import re
import os
from pathlib import Path

def sanitize_path(input_path: str) -> str:
    """
    将输入路径中不符合 Windows/Linux 规范的部分替换为 '_'
    """
    path_obj = Path(input_path)
    parts = list(path_obj.parts)
    
    # 1. 定义 Windows 禁用的字符正则 (Linux 仅禁用 / 和 \0，Windows 包含更多)
    # < > : " / \ | ? *
    invalid_chars_re = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
    
    # 2. Windows 保留的文件名
    reserved_names = {
        "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", 
        "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", 
        "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    sanitized_parts = []
    
    for i, part in enumerate(parts):
        # 跳过根目录标识符 (如 Windows 的 C:\ 或 Linux 的 /)
        if i == 0 and (part.endswith('\\') or part == '/'):
            sanitized_parts.append(part)
            continue
            
        # 替换禁用字符为 '_'
        new_part = invalid_chars_re.sub('_', part)
        
        # 处理 Windows 特有的末尾限制：文件名末尾不能是空格或点
        new_part = new_part.strip(' .')
        if not new_part: # 如果清理后变为空字符串
            new_part = "_"
            
        # 检查是否为保留名称 (不区分大小写)
        base_name = new_part.split('.')[0].upper()
        if base_name in reserved_names:
            new_part = "_" + new_part

        sanitized_parts.append(new_part)

    # 重新组合路径
    # 注意：这里使用 os.path.join 保证生成的路径符合当前运行环境的斜杠习惯
    return str(Path(*sanitized_parts))