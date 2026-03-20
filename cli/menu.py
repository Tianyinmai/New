import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.password_generator import PasswordGenerator
from utils.strength_checker import StrengthChecker
from utils.clipboard import ClipboardManager

class PasswordMenu:
    """
    密码生成器交互菜单类
    
    提供命令行交互界面，处理用户输入和输出显示。
    """
    
    CHAR_TYPE_MAP = {
        '1': 'digits',
        '2': 'lowercase',
        '3': 'uppercase',
        '4': 'special'
    }
    
    CHAR_TYPE_NAMES = {
        'digits': '数字',
        'lowercase': '小写字母',
        'uppercase': '大写字母',
        'special': '特殊符号'
    }
    
    def __init__(self):
        """初始化菜单系统"""
        self.generator = PasswordGenerator()
        self.checker = StrengthChecker()
        self.clipboard = ClipboardManager()
        self.running = True
    
    def display_header(self):
        """显示程序标题"""
        print("\n" + "=" * 30)
        print("    随机密码生成器")
        print("=" * 30)
    
    def display_menu(self):
        """显示主菜单"""
        self.display_header()
        print("1. 生成单个密码")
        print("2. 批量生成密码")
        print("3. 查看历史生成记录")
        print("4. 清空历史记录")
        print("0. 退出程序")
        print("-" * 30)
    
    def get_input_with_default(self, prompt, default_value, input_type=str):
        """
        获取用户输入，支持默认值
        
        Args:
            prompt (str): 提示信息
            default_value: 默认值
            input_type: 输入类型转换函数
        
        Returns:
            转换后的用户输入值或默认值
        """
        user_input = input(prompt).strip()
        if not user_input:
            return default_value
        try:
            return input_type(user_input)
        except ValueError:
            return default_value
    
    def get_char_types(self):
        """
        获取用户选择的字符类型
        
        Returns:
            list: 字符类型列表
        """
        print("请选择字符类型（可多选，用逗号分隔）：")
        print("1. 数字  2. 小写字母  3. 大写字母  4. 特殊符号")
        
        while True:
            choice = input("请选择（默认全部，如：1,2,3）：").strip()
            
            if not choice:
                return ['digits', 'lowercase', 'uppercase', 'special']
            
            try:
                selected = [c.strip() for c in choice.split(',')]
                char_types = []
                for s in selected:
                    if s in self.CHAR_TYPE_MAP:
                        char_types.append(self.CHAR_TYPE_MAP[s])
                
                if char_types:
                    return char_types
                else:
                    print("⚠️ 输入无效，请重新选择（如：1,2,3）")
            except Exception:
                print("⚠️ 输入格式错误，请重新选择")
    
    def get_exclude_confusable(self):
        """
        获取是否排除易混淆字符
        
        Returns:
            bool: True表示排除，False表示不排除
        """
        choice = input("是否排除易混淆字符（y/n，默认n）：").strip().lower()
        return choice == 'y'
    
    def ask_copy_to_clipboard(self, password):
        """
        询问是否复制到剪贴板
        
        Args:
            password (str): 要复制的密码
        """
        choice = input("是否复制到剪贴板（y/n）：").strip().lower()
        if choice == 'y':
            if self.clipboard.copy_to_clipboard(password):
                print("✅ 密码已复制到剪贴板！")
            else:
                print("⚠️ 复制失败，请确保已安装pyperclip库（pip install pyperclip）")
    
    def generate_single_password(self):
        """生成单个密码的交互流程"""
        print("\n--- 生成单个密码 ---")
        
        length = self.get_input_with_default(
            "请设置密码长度（6-32，默认16）：", 
            16, 
            int
        )
        
        char_types = self.get_char_types()
        exclude_confusable = self.get_exclude_confusable()
        
        try:
            password = self.generator.generate_password(
                length=length,
                char_types=char_types,
                exclude_confusable=exclude_confusable
            )
            strength = self.checker.check_strength(password)
            
            print(f"\n生成的密码：{password}")
            print(f"密码强度：{strength}")
            
            self.ask_copy_to_clipboard(password)
            
            self.generator.save_to_history([password], [strength])
            print("✅ 密码已保存到历史记录")
            
        except ValueError as e:
            print(f"⚠️ 错误：{e}")
    
    def generate_batch_passwords(self):
        """批量生成密码的交互流程"""
        print("\n--- 批量生成密码 ---")
        
        count = self.get_input_with_default(
            "请输入生成数量（1-100，默认10）：",
            10,
            int
        )
        
        length = self.get_input_with_default(
            "请设置密码长度（6-32，默认16）：",
            16,
            int
        )
        
        char_types = self.get_char_types()
        exclude_confusable = self.get_exclude_confusable()
        
        try:
            passwords = self.generator.generate_batch(
                count=count,
                length=length,
                char_types=char_types,
                exclude_confusable=exclude_confusable
            )
            
            strengths = [self.checker.check_strength(p) for p in passwords]
            
            print(f"\n成功生成 {len(passwords)} 个密码：")
            print("-" * 40)
            for i, (pwd, strength) in enumerate(zip(passwords, strengths), 1):
                print(f"{i:3d}. {pwd}  [{strength}]")
            print("-" * 40)
            
            strength_counts = {'弱': 0, '中': 0, '强': 0}
            for s in strengths:
                strength_counts[s] += 1
            print(f"强度统计：弱 {strength_counts['弱']}个，中 {strength_counts['中']}个，强 {strength_counts['强']}个")
            
            choice = input("\n是否复制所有密码到剪贴板（y/n）：").strip().lower()
            if choice == 'y':
                all_passwords = '\n'.join(passwords)
                if self.clipboard.copy_to_clipboard(all_passwords):
                    print("✅ 所有密码已复制到剪贴板！")
                else:
                    print("⚠️ 复制失败")
            
            self.generator.save_to_history(passwords, strengths)
            print("✅ 密码已保存到历史记录")
            
        except ValueError as e:
            print(f"⚠️ 错误：{e}")
    
    def view_history(self):
        """查看历史生成记录"""
        print("\n--- 历史生成记录 ---")
        
        history = self.generator.get_history()
        
        if not history:
            print("暂无历史记录")
            return
        
        print(f"共 {len(history)} 条记录：")
        print("=" * 50)
        
        for i, record in enumerate(history, 1):
            print(f"\n【记录 {i}】")
            print(f"生成时间：{record.get('生成时间', '未知')}")
            passwords = record.get('密码列表', [])
            strengths = record.get('强度', [])
            
            for j, (pwd, strength) in enumerate(zip(passwords, strengths), 1):
                if len(passwords) > 1:
                    print(f"  {j}. {pwd}  [{strength}]")
                else:
                    print(f"密码：{pwd}  [{strength}]")
        
        print("\n" + "=" * 50)
    
    def clear_history(self):
        """清空历史记录"""
        print("\n--- 清空历史记录 ---")
        
        choice = input("确定要清空所有历史记录吗？（y/n）：").strip().lower()
        if choice == 'y':
            if self.generator.clear_history():
                print("✅ 历史记录已清空")
            else:
                print("⚠️ 清空失败")
        else:
            print("已取消操作")
    
    def run(self):
        """运行主菜单循环"""
        while self.running:
            self.display_menu()
            
            choice = input("请选择功能（0-4）：").strip()
            
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
                print("⚠️ 无效选择，请输入0-4")
            
            if self.running:
                input("\n按回车键继续...")
