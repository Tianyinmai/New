"""
随机密码生成器 - 主程序入口

这是一个功能完善的密码生成工具，支持：
- 自定义密码长度（6-32位）
- 多种字符类型选择
- 批量生成密码
- 密码强度检测
- 历史记录保存
- 剪贴板复制功能

使用方法：
    python main.py

作者：Password Generator
版本：1.0.0
"""

import sys

# 确保可以导入本地模块
sys.path.insert(0, '.')

from cli.menu import Menu


def main():
    """
    程序主入口函数
    
    初始化并启动密码生成器的交互菜单
    """
    try:
        # 创建菜单实例并运行
        menu = Menu()
        menu.run()
    except KeyboardInterrupt:
        # 处理Ctrl+C中断
        print("\n\n程序被用户中断，再见！")
        sys.exit(0)
    except Exception as e:
        # 处理其他异常
        print(f"\n程序发生错误：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
