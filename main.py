import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.menu import PasswordMenu

def main():
    """
    程序主入口函数
    
    初始化并启动密码生成器交互界面。
    """
    try:
        menu = PasswordMenu()
        menu.run()
    except KeyboardInterrupt:
        print("\n\n程序已终止")
        sys.exit(0)
    except Exception as e:
        print(f"\n程序发生错误：{e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
