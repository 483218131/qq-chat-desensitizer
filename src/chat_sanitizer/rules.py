import re

# 1. 媒体标签（最先执行，防止干扰后续正则）
REGEX_MEDIA = re.compile(r'\[(图片|语音|视频|文件):.*?\]\n?')

# 2. 邮箱
REGEX_EMAIL = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

# 3. 身份证号（18位）
REGEX_ID_CARD = re.compile(r'(?<!\d)([1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx])(?!\d)')

# 4. 银行卡号（16-19位）
REGEX_BANK_CARD = re.compile(r'(?<!\d)([1-9]\d{15,18})(?!\d)')

# 5. 手机号（11位，1开头）
REGEX_PHONE = re.compile(r'(?<!\d)(1[3-9]\d{9})(?!\d)')

# 6. QQ号（5-11位）
REGEX_QQ = re.compile(r'(?<!\d)(?!(?:17\d{8}|20\d{6})(?!\d))([1-9][0-9]{4,10})(?!\d)')

def is_risky_name(name: str) -> bool:
    """检测是否为极易引发全局替换灾难的“毒性昵称”"""
    name = name.strip()
    if not name: 
        return True 
    if re.fullmatch(r'[^\w\u4e00-\u9fa5]+|_+', name): 
        return True 
    if len(name) == 1 and re.fullmatch(r'[A-Za-z0-9]', name):
        return True
    return False

def mask_sensitive_data(text: str) -> str:
    """通用的文本层脱敏管道"""
    if not text:
        return text
    
    # 严格执行流水线顺序
    text = REGEX_MEDIA.sub('', text)
    text = REGEX_EMAIL.sub('[隐藏邮箱]', text)
    text = REGEX_ID_CARD.sub('[隐藏身份证]', text)
    text = REGEX_BANK_CARD.sub('[隐藏银行卡]', text)
    text = REGEX_PHONE.sub(lambda m: m.group(1)[:3] + '****' + m.group(1)[7:], text)
    text = REGEX_QQ.sub('[隐藏QQ号]', text)
    
    return text.strip()