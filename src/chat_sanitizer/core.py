import json
import re
from pathlib import Path
from .rules import is_risky_name, mask_sensitive_data

def process_chat_data(input_file: Path, output_file: Path) -> dict:
    """执行核心脱敏流，返回执行统计数据供上层调用"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except Exception as e:
        raise RuntimeError(f"读取或解析 JSON 失败: {e}")

    # 兼容直接列表和嵌套字典格式
    data = raw_data if isinstance(raw_data, list) else next((v for v in raw_data.values() if isinstance(v, list)), [])
    if not data:
        raise ValueError("未能找到有效的消息列表。")

    uid_to_userX = {}
    name_to_userX = {}
    user_counter = 1

    # 第一轮遍历：建立高危昵称过滤与用户映射
    for msg in data:
        sender = msg.get('sender', {})
        if not isinstance(sender, dict): continue
            
        uid = str(sender.get('uin', sender.get('uid', '')))
        name = str(sender.get('name', ''))

        if not uid: continue

        if uid not in uid_to_userX:
            uid_to_userX[uid] = f"用户{user_counter}"
            user_counter += 1

        if name and name not in ["None", ""]:
            if not is_risky_name(name):
                name_to_userX[name] = uid_to_userX[uid]

    # 按长度降序，防止长昵称被短昵称截断替换
    sorted_names = sorted(name_to_userX.keys(), key=len, reverse=True)
    processed_count = 0

    with open(output_file, 'w', encoding='utf-8') as out_f:
        # 第二轮遍历：执行严格顺序的清洗流水线
        for msg in data:
            sender = msg.get('sender', {})
            uid = str(sender.get('uin', sender.get('uid', '')))
            time_str = msg.get('time', msg.get('timestamp', ''))

            content_obj = msg.get('content', {})
            
            # --- 之前丢失的就是下面这一行提取逻辑 ---
            content_text = str(content_obj.get('text', '')) if isinstance(content_obj, dict) else str(content_obj)

            if not content_text or not uid or content_text == "None":
                continue

            current_user = uid_to_userX.get(uid, "未知用户")

            # 步骤 1：清理系统级硬编码回复标签
            content_text = re.sub(r'\[回复 u_[a-zA-Z0-9_-]+:', '[回复]:', content_text)

            # 步骤 2：执行高精度的强特征脱敏（媒体、邮箱、身份证、手机、QQ）
            # 在此阶段，所有带有 @ 的邮箱会被保护性替换为 [隐藏邮箱]
            content_text = mask_sensitive_data(content_text)

            # 步骤 3：执行人名昵称替换
            for real_name in sorted_names:
                if real_name in content_text:
                    content_text = content_text.replace(real_name, name_to_userX[real_name])

            # 步骤 4：执行残存 @ 符号的扫尾（不会再误杀邮箱）
            if '@' in content_text:
                content_text = re.sub(r'@([^\s，。！？\n]+)', r'@未知人员', content_text)

            # 写入结果
            out_f.write(f"[{time_str}] {current_user}:\n{content_text}\n\n")
            processed_count += 1

    return {
        "processed_count": processed_count,
        "unique_users": len(uid_to_userX)
    }