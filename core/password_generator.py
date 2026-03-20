import random
import string
from datetime import datetime
import json
import os

class PasswordGenerator:
    """
    随机密码生成器核心类
    
    负责生成随机密码、保存密码记录、管理历史记录等功能。
    """
    
    CHAR_SETS = {
        'digits': string.digits,
        'lowercase': string.ascii_lowercase,
        'uppercase': string.ascii_uppercase,
        'special': '!@#$%^&*()_+-=[]{}|;:,.<>?'
    }
    
    CONFUSABLE_CHARS = {
        '0': 'O',
        'O': '0',
        '1': 'l',
        'l': '1',
        'I': '1',
        '1': 'I'
    }
    
    CONFUSABLE_SET = {'0', 'O', '1', 'l', 'I'}
    
    def __init__(self, history_file='passwords.json'):
        """
        初始化密码生成器
        
        Args:
            history_file (str): 历史记录文件路径，默认为'passwords.json'
        """
        self.history_file = history_file
    
    def generate_password(self, length=16, char_types=None, exclude_confusable=False):
        """
        生成单个随机密码
        
        Args:
            length (int): 密码长度，范围6-32，默认16
            char_types (list): 字符类型列表，可选值：'digits', 'lowercase', 'uppercase', 'special'
            exclude_confusable (bool): 是否排除易混淆字符，默认False
        
        Returns:
            str: 生成的随机密码
        
        Raises:
            ValueError: 当密码长度不在有效范围内或未选择任何字符类型时
        """
        if length < 6 or length > 32:
            raise ValueError("密码长度必须在6-32位之间")
        
        if not char_types:
            char_types = ['digits', 'lowercase', 'uppercase', 'special']
        
        all_chars = ''
        for char_type in char_types:
            if char_type in self.CHAR_SETS:
                all_chars += self.CHAR_SETS[char_type]
        
        if not all_chars:
            raise ValueError("必须至少选择一种字符类型")
        
        if exclude_confusable:
            all_chars = ''.join(c for c in all_chars if c not in self.CONFUSABLE_SET)
            if not all_chars:
                raise ValueError("排除易混淆字符后无可用的字符类型，请选择其他字符类型")
        
        password = ''.join(random.choice(all_chars) for _ in range(length))
        return password
    
    def generate_batch(self, count=1, length=16, char_types=None, exclude_confusable=False):
        """
        批量生成随机密码
        
        Args:
            count (int): 生成数量，范围1-100，默认1
            length (int): 密码长度，范围6-32，默认16
            char_types (list): 字符类型列表
            exclude_confusable (bool): 是否排除易混淆字符，默认False
        
        Returns:
            list: 生成的密码列表
        
        Raises:
            ValueError: 当生成数量不在有效范围内时
        """
        if count < 1 or count > 100:
            raise ValueError("批量生成数量必须在1-100之间")
        
        passwords = []
        for _ in range(count):
            password = self.generate_password(length, char_types, exclude_confusable)
            passwords.append(password)
        
        return passwords
    
    def save_to_history(self, passwords, strengths):
        """
        保存密码到历史记录文件
        
        Args:
            passwords (list): 密码列表
            strengths (list): 对应的强度列表
        
        Returns:
            bool: 保存成功返回True，失败返回False
        """
        record = {
            "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "密码列表": passwords,
            "强度": strengths
        }
        
        history = []
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    if not isinstance(history, list):
                        history = []
            except (json.JSONDecodeError, IOError):
                history = []
        
        history.append(record)
        
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def get_history(self):
        """
        获取历史生成记录
        
        Returns:
            list: 历史记录列表，每条记录包含生成时间、密码列表和强度信息
        """
        if not os.path.exists(self.history_file):
            return []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
                return history if isinstance(history, list) else []
        except (json.JSONDecodeError, IOError):
            return []
    
    def clear_history(self):
        """
        清空历史生成记录
        
        Returns:
            bool: 清空成功返回True，失败返回False
        """
        try:
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
            return True
        except IOError:
            return False
