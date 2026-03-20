"""
交互菜单模块
提供命令行交互界面
"""

import sys
from typing import List, Tuple

# 导入核心模块
sys.path.insert(0, '..')
from core.password_generator import PasswordGenerator
from utils.strength_checker import StrengthChecker
from utils.clipboard import clipboard


class Menu:
    """交互菜单类"""
    
    def __init__(self):
        """初始化菜单"""
        self.generator = PasswordGenerator()
        self.checker = StrengthChecker()
        self.running = True
    
    def display_main_menu(self):
        """显示主菜单"""
        print("\n===== 随机密码生成器 =====")
        print("1. 生成单个密码")
        print("2. 批量生成密码")
        print("3. 查看历史生成记录")
        print("4. 清空历史记录")
        print("0. 退出程序")
        print("=" * 25)
    
    def get_choice(self, prompt: str = "请选择功能（0-4）：") -> str:
        """
        获取用户选择
        
        Args:
            prompt: 提示信息
            
        Returns:
            str: 用户输入
        """
        return input(prompt).strip()
    
    def get_password_length(self) -> int:
        """
        获取密码长度输入
        
        Returns:
            int: 密码长度
        """
        while True:
            user_input = input("请设置密码长度（6-32，默认16）：").strip()
            
            # 使用默认值
            if not user_input:
                return 16
            
            try:
                length = int(user_input)
                if length < 6 or length > 32:
                    print("❌ 错误：密码长度必须在6-32之间！")
                    continue
                return length
            except ValueError:
                print("❌ 错误：请输入有效的数字！")
    
    def get_char_types(self) -> Tuple[bool, bool, bool, bool]:
        """
        获取字符类型选择
        
        Returns:
            Tuple[bool, bool, bool, bool]: (数字, 小写字母, 大写字母, 特殊符号)
        """
        print("\n字符类型选项：")
        print("  1. 数字")
        print("  2. 小写字母")
        print("  3. 大写字母")
        print("  4. 特殊符号")
        
        while True:
            user_input = input("请选择字符类型（可多选，用逗号分隔，如1,2,3）：").strip()
            
            if not user_input:
                print("❌ 错误：至少选择一种字符类型！")
                continue
            
            try:
                # 解析选择
                choices = [int(x.strip()) for x in user_input.split(',')]
                
                # 验证选择
                if not all(1 <= c <= 4 for c in choices):
                    print("❌ 错误：选项必须在1-4之间！")
                    continue
                
                use_digits = 1 in choices
                use_lowercase = 2 in choices
                use_uppercase = 3 in choices
                use_special = 4 in choices
                
                if not any([use_digits, use_lowercase, use_uppercase, use_special]):
                    print("❌ 错误：至少选择一种字符类型！")
                    continue
                
                return use_digits, use_lowercase, use_uppercase, use_special
                
            except ValueError:
                print("❌ 错误：请输入有效的数字，用逗号分隔！")
    
    def get_exclude_confusing(self) -> bool:
        """
        获取是否排除易混淆字符的选择
        
        Returns:
            bool: 是否排除易混淆字符
        """
        while True:
            user_input = input("是否排除易混淆字符（y/n，默认n）：").strip().lower()
            
            if not user_input or user_input == 'n':
                return False
            elif user_input == 'y':
                return True
            else:
                print("❌ 错误：请输入 y 或 n！")
    
    def get_batch_count(self) -> int:
        """
        获取批量生成数量
        
        Returns:
            int: 生成数量
        """
        while True:
            user_input = input("请输入生成数量（1-100，默认1）：").strip()
            
            if not user_input:
                return 1
            
            try:
                count = int(user_input)
                if count < 1 or count > 100:
                    print("❌ 错误：生成数量必须在1-100之间！")
                    continue
                return count
            except ValueError:
                print("❌ 错误：请输入有效的数字！")
    
    def ask_copy_to_clipboard(self, text: str) -> bool:
        """
        询问是否复制到剪贴板
        
        Args:
            text: 要复制的文本
            
        Returns:
            bool: 是否复制成功
        """
        while True:
            user_input = input("是否复制到剪贴板（y/n）：").strip().lower()
            
            if user_input == 'y':
                if clipboard.copy(text):
                    print("✅ 密码已复制到剪贴板！")
                    return True
                else:
                    print("❌ 复制到剪贴板失败！")
                    return False
            elif user_input == 'n' or not user_input:
                return False
            else:
                print("❌ 错误：请输入 y 或 n！")
    
    def generate_single_password(self):
        """生成单个密码"""
        try:
            # 获取参数
            length = self.get_password_length()
            use_digits, use_lowercase, use_uppercase, use_special = self.get_char_types()
            exclude_confusing = self.get_exclude_confusing()
            
            # 生成密码
            password = self.generator.generate(
                length=length,
                use_digits=use_digits,
                use_lowercase=use_lowercase,
                use_uppercase=use_uppercase,
                use_special=use_special,
                exclude_confusing=exclude_confusing
            )
            
            # 检测强度
            strength = self.checker.check(password)
            
            # 显示结果
            print(f"\n生成的密码：{password}")
            print(f"密码强度：{strength}")
            
            # 保存到历史记录
            self.generator.save_to_history([password], [strength])
            
            # 询问是否复制
            self.ask_copy_to_clipboard(password)
            
        except ValueError as e:
            print(f"❌ 错误：{e}")
        except Exception as e:
            print(f"❌ 发生未知错误：{e}")
    
    def generate_batch_passwords(self):
        """批量生成密码"""
        try:
            # 获取参数
            count = self.get_batch_count()
            length = self.get_password_length()
            use_digits, use_lowercase, use_uppercase, use_special = self.get_char_types()
            exclude_confusing = self.get_exclude_confusing()
            
            # 生成密码
            passwords = self.generator.generate_batch(
                count=count,
                length=length,
                use_digits=use_digits,
                use_lowercase=use_lowercase,
                use_uppercase=use_uppercase,
                use_special=use_special,
                exclude_confusing=exclude_confusing
            )
            
            # 检测强度
            strengths = self.checker.check_batch(passwords)
            
            # 显示结果
            print(f"\n===== 生成的密码列表 =====")
            for i, (password, strength) in enumerate(zip(passwords, strengths), 1):
                print(f"{i}. {password}  [强度：{strength}]")
            print("=" * 30)
            
            # 保存到历史记录
            self.generator.save_to_history(passwords, strengths)
            
            # 询问是否复制所有密码
            all_passwords = "\n".join(passwords)
            print(f"\n已生成 {count} 个密码并保存到历史记录。")
            
            while True:
                copy_choice = input("是否复制所有密码到剪贴板（y/n）：").strip().lower()
                if copy_choice == 'y':
                    if clipboard.copy(all_passwords):
                        print("✅ 所有密码已复制到剪贴板！")
                    else:
                        print("❌ 复制到剪贴板失败！")
                    break
                elif copy_choice == 'n' or not copy_choice:
                    break
                else:
                    print("❌ 错误：请输入 y 或 n！")
            
        except ValueError as e:
            print(f"❌ 错误：{e}")
        except Exception as e:
            print(f"❌ 发生未知错误：{e}")
    
    def view_history(self):
        """查看历史记录"""
        history = self.generator.load_history()
        
        if not history:
            print("\n暂无历史记录。")
            return
        
        print(f"\n===== 历史生成记录 =====")
        print(f"共 {len(history)} 条记录\n")
        
        for i, record in enumerate(history, 1):
            print(f"【记录 {i}】")
            print(f"  生成时间：{record.get('生成时间', '未知')}")
            passwords = record.get('密码列表', [])
            strengths = record.get('强度', [])
            
            for j, (pwd, strength) in enumerate(zip(passwords, strengths), 1):
                print(f"  {j}. {pwd}  [强度：{strength}]")
            print()
        
        print("=" * 30)
    
    def clear_history(self):
        """清空历史记录"""
        while True:
            confirm = input("确定要清空所有历史记录吗？此操作不可恢复（y/n）：").strip().lower()
            
            if confirm == 'y':
                if self.generator.clear_history():
                    print("✅ 历史记录已清空！")
                else:
                    print("❌ 清空历史记录失败！")
                break
            elif confirm == 'n' or not confirm:
                print("已取消清空操作。")
                break
            else:
                print("❌ 错误：请输入 y 或 n！")
    
    def run(self):
        """运行菜单循环"""
        print("欢迎使用随机密码生成器！")
        print(clipboard.get_status_message())
        
        while self.running:
            self.display_main_menu()
            choice = self.get_choice()
            
            if choice == '1':
                self.generate_single_password()
            elif choice == '2':
                self.generate_batch_passwords()
            elif choice == '3':
                self.view_history()
            elif choice == '4':
                self.clear_history()
            elif choice == '0':
                print("\n感谢使用，再见！")
                self.running = False
            else:
                print("❌ 错误：请输入0-4之间的数字！")


def main():
    """菜单模块入口函数"""
    menu = Menu()
    menu.run()


if __name__ == "__main__":
    main()
