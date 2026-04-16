import argparse
import sys
from pathlib import Path
from .core import process_chat_data

def main():
    parser = argparse.ArgumentParser(
        description="QQ 聊天记录脱敏清洗工具",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # 核心修改 1：移除 required=True，设定默认值为同目录下的 export.json
    parser.add_argument("-i", "--input", default="export.json", help="输入的原始聊天记录文件")
    parser.add_argument("-o", "--output", default="desensitized_chat.txt", help="输出路径")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    try:
        # 核心修改 2：加入通俗的错误提示，并使用 input() 阻塞窗口关闭
        if not input_path.exists() or not input_path.is_file():
            print(f"❌ 找不到文件: {input_path.absolute()}")
            print("💡 请确保你已经将导出的聊天记录命名为 'export.json'，并与本程序放在同一个文件夹内！")
            input("\n[按回车键退出程序...]")
            sys.exit(1)

        print(f"⚙️ 开始读取并分析: {input_path.name}")
        
        stats = process_chat_data(input_path, output_path)
        
        print(f"✅ 脱敏完成！安全文件已保存至: {output_path.absolute()}")
        print(f"📊 统计摘要:")
        print(f"   - 共处理有效消息: {stats['processed_count']} 条")
        print(f"   - 识别并隐匿用户: {stats['unique_users']} 个")
        
        # 核心修改 3：成功后阻塞窗口，让用户有时间看清输出结果
        input("\n[处理完毕，请按回车键退出...]")

    except Exception as e:
        print(f"❌ 处理发生意外中断: {e}", file=sys.stderr)
        input("\n[按回车键退出程序...]")
        sys.exit(1)

if __name__ == "__main__":
    main()