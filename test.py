import json

# 构造测试文本
dirty_text = """
--- 基础脱敏测试 ---
用户123说：我的手机号是13800138000，你可以发邮件到 my_name.test@domain.com.cn 联系我。
我的身份证号是11010519900101123X，银行卡号是6222021234567890123。
我的QQ是1234567，也可以加我另一个号10001。

--- 媒体占位符与系统标签 ---
[图片: 7B8C9D0E1F2A3B4C5D6E7F8A9B0C1D2E.png]
[语音: /data/user/0/com.tencent.mobileqq/files/audio/v_123456.amr]
[视频: http://v.qpic.cn/1010_abcdefg.mp4]
[回复 u_a1b2c3d4: 刚才那个文件收到了吗？]
@张三 @李四_测试 你们看下这个。

--- 边界与格式测试 ---
手机号在括号里(13912345678)，或者在句末13700000000。
邮箱带特殊符号：first-part.last_name+tag@sub.example.org。
身份证末尾小写：44010619800101123x。
QQ号长度边界：12345（5位）和 12345678901（11位）。

--- 防误杀测试（极重要） ---
时间戳：1712800000（10位）和 1712800000000（13位，不应被误判为手机号）。
纯数字编号：202404010001（12位，不应被误判为银行卡或手机号）。
版本号或坐标：v1.2.3.4，GPS: 116.397, 39.908。
数学公式：1+1=2，或者金额：￥100.00。
日期格式：20240520（8位数字，不应被误判为QQ号）。

--- 昵称与特殊符号 ---
昵称测试： . (点)、 _ (下划线)、 A (单字母)、 1 (单数字) 均应触发 is_risky_name。
"""

# 封装为符合 core.py 解析要求的格式
test_data = [
    {
        "sender": {"uin": "10001", "name": "测试员"},
        "time": "2024-04-15 10:00:00",
        "content": {"text": dirty_text}
    }
]

# 保存文件
with open('test_export.json', 'w', encoding='utf-8') as f:
    json.dump(test_data, f, ensure_ascii=False, indent=2)

print("✅ test_export.json 已生成")