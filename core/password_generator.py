"""
密码生成器核心模块
提供密码生成功能，支持自定义长度、字符类型、批量生成等
"""

import random
import string
from datetime import datetime
from typing import List, Dict, Any


class PasswordGenerator:
    """密码生成器类"""
    
    # 字符集定义
    DIGITS = string.digits  # 数字: 0-9
    LOWERCASE = string.ascii_lowercase  # 小写字母: a-z
    UPPERCASE = string.ascii_uppercase  # 大写字母: A-Z
    SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"  # 特殊符号
    
    # 易混淆字符映射
    CONFUSING_CHARS = {
        '0': '', 'O': '', 'o': '',  # 0 和 O 混淆
        '1': '', 'l': '', 'I': '',  # 1、l 和 I 混淆
    }
    
    def __init__(self):
        """初始化密码生成器"""
        self.history_file = "passwords.json"
    
    def generate(self, 
                 length: int = 16, 
                 use_digits: bool = True,
                 use_lowercase: bool = True, 
                 use_uppercase: bool = True,
                 use_special: bool = False,
                 exclude_confusing: bool = False) -> str:
        """
        生成单个密码
        
        Args:
            length: 密码长度，范围6-32，默认16
            use_digits: 是否使用数字
            use_lowercase: 是否使用小写字母
            use_uppercase: 是否使用大写字母
            use_special: 是否使用特殊符号
            exclude_confusing: 是否排除易混淆字符
            
        Returns:
            str: 生成的密码
            
        Raises:
            ValueError: 当参数不合法时抛出异常
        """
        # 参数验证
        if not isinstance(length, int) or length < 6 or length > 32:
            raise ValueError(f"密码长度必须在6-32之间，当前值: {length}")
        
        # 构建字符集
        charset = self._build_charset(
            use_digits, use_lowercase, use_uppercase, use_special
        )
        
        if not charset:
            raise ValueError("至少选择一种字符类型")
        
        # 排除易混淆字符
        if exclude_confusing:
            charset = self._exclude_confusing_chars(charset)
        
        # 确保每种选中的字符类型至少出现一次
        password_chars = []
        required_chars = []
        
        if use_digits:
            digits_set = self.DIGITS
            if exclude_confusing:
                digits_set = self._exclude_confusing_chars(digits_set)
            if digits_set:
                required_chars.append(random.choice(digits_set))
        
        if use_lowercase:
            lowercase_set = self.LOWERCASE
            if exclude_confusing:
                lowercase_set = self._exclude_confusing_chars(lowercase_set)
            if lowercase_set:
                required_chars.append(random.choice(lowercase_set))
        
        if use_uppercase:
            uppercase_set = self.UPPERCASE
            if exclude_confusing:
                uppercase_set = self._exclude_confusing_chars(uppercase_set)
            if uppercase_set:
                required_chars.append(random.choice(uppercase_set))
        
        if use_special:
            if self.SPECIAL:
                required_chars.append(random.choice(self.SPECIAL))
        
        # 填充剩余长度
        remaining_length = length - len(required_chars)
        if remaining_length < 0:
            raise ValueError("密码长度不足以包含所有必需的字符类型")
        
        password_chars = required_chars + [random.choice(charset) for _ in range(remaining_length)]
        
        # 打乱字符顺序
        random.shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def generate_batch(self,
                       count: int = 1,
                       length: int = 16,
                       use_digits: bool = True,
                       use_lowercase: bool = True,
                       use_uppercase: bool = True,
                       use_special: bool = False,
                       exclude_confusing: bool = False) -> List[str]:
        """
        批量生成密码
        
        Args:
            count: 生成数量，范围1-100，默认1
            length: 密码长度，范围6-32，默认16
            use_digits: 是否使用数字
            use_lowercase: 是否使用小写字母
            use_uppercase: 是否使用大写字母
            use_special: 是否使用特殊符号
            exclude_confusing: 是否排除易混淆字符
            
        Returns:
            List[str]: 生成的密码列表
            
        Raises:
            ValueError: 当参数不合法时抛出异常
        """
        if not isinstance(count, int) or count < 1 or count > 100:
            raise ValueError(f"批量生成数量必须在1-100之间，当前值: {count}")
        
        passwords = []
        for _ in range(count):
            password = self.generate(
                length=length,
                use_digits=use_digits,
                use_lowercase=use_lowercase,
                use_uppercase=use_uppercase,
                use_special=use_special,
                exclude_confusing=exclude_confusing
            )
            passwords.append(password)
        
        return passwords
    
    def _build_charset(self, 
                       use_digits: bool, 
                       use_lowercase: bool,
                       use_uppercase: bool, 
                       use_special: bool) -> str:
        """
        构建字符集
        
        Args:
            use_digits: 是否使用数字
            use_lowercase: 是否使用小写字母
            use_uppercase: 是否使用大写字母
            use_special: 是否使用特殊符号
            
        Returns:
            str: 构建的字符集
        """
        charset = ""
        if use_digits:
            charset += self.DIGITS
        if use_lowercase:
            charset += self.LOWERCASE
        if use_uppercase:
            charset += self.UPPERCASE
        if use_special:
            charset += self.SPECIAL
        return charset
    
    def _exclude_confusing_chars(self, charset: str) -> str:
        """
        从字符集中排除易混淆字符
        
        Args:
            charset: 原始字符集
            
        Returns:
            str: 排除易混淆字符后的字符集
        """
        return ''.join(c for c in charset if c not in self.CONFUSING_CHARS)
    
    def save_to_history(self, passwords: List[str], strengths: List[str]) -> bool:
        """
        保存生成的密码到历史记录文件
        
        Args:
            passwords: 密码列表
            strengths: 对应的强度列表
            
        Returns:
            bool: 保存是否成功
        """
        import json
        import os
        
        try:
            # 读取现有历史记录
            history = []
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    try:
                        history = json.load(f)
                    except json.JSONDecodeError:
                        history = []
            
            # 添加新记录
            record = {
                "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "密码列表": passwords,
                "强度": strengths
            }
            history.append(record)
            
            # 保存到文件
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存历史记录失败: {e}")
            return False
    
    def load_history(self) -> List[Dict[str, Any]]:
        """
        加载历史记录
        
        Returns:
            List[Dict[str, Any]]: 历史记录列表
        """
        import json
        import os
        
        if not os.path.exists(self.history_file):
            return []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"读取历史记录失败: {e}")
            return []
    
    def clear_history(self) -> bool:
        """
        清空历史记录
        
        Returns:
            bool: 清空是否成功
        """
        import os
        
        try:
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
            return True
        except Exception as e:
            print(f"清空历史记录失败: {e}")
            return False
