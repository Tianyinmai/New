"""
密码强度检测模块
提供密码强度评估功能
"""

import re
from enum import Enum


class StrengthLevel(Enum):
    """密码强度等级枚举"""
    WEAK = "弱"
    MEDIUM = "中"
    STRONG = "强"


class StrengthChecker:
    """密码强度检测器类"""
    
    def __init__(self):
        """初始化强度检测器"""
        pass
    
    def check(self, password: str) -> str:
        """
        检测密码强度
        
        评分标准：
        - 基础分：密码长度
        - 字符类型加分：数字、小写字母、大写字母、特殊符号各+1分
        - 长度加分：12位以上+1分，16位以上+2分
        - 强度等级：
          * 弱：0-3分
          * 中：4-6分
          * 强：7分以上
        
        Args:
            password: 待检测的密码
            
        Returns:
            str: 强度等级（"弱"/"中"/"强"）
            
        Raises:
            ValueError: 当密码为空时抛出异常
        """
        if not password:
            raise ValueError("密码不能为空")
        
        score = 0
        
        # 基础分：根据长度给分
        length = len(password)
        if length >= 6:
            score += 1
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1
        
        # 字符类型加分
        char_types = 0
        
        # 检查数字
        if re.search(r'\d', password):
            char_types += 1
            score += 1
        
        # 检查小写字母
        if re.search(r'[a-z]', password):
            char_types += 1
            score += 1
        
        # 检查大写字母
        if re.search(r'[A-Z]', password):
            char_types += 1
            score += 1
        
        # 检查特殊符号
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            char_types += 1
            score += 1
        
        # 如果只有一种字符类型，即使长度较长也降低分数
        if char_types == 1:
            score = min(score, 3)
        
        # 如果只有两种字符类型，最高只能到中等
        if char_types == 2:
            score = min(score, 5)
        
        # 根据分数判断强度等级
        if score <= 3:
            return StrengthLevel.WEAK.value
        elif score <= 5:
            return StrengthLevel.MEDIUM.value
        else:
            return StrengthLevel.STRONG.value
    
    def check_batch(self, passwords: list) -> list:
        """
        批量检测密码强度
        
        Args:
            passwords: 密码列表
            
        Returns:
            list: 对应的强度等级列表
        """
        return [self.check(pwd) for pwd in passwords]
    
    def get_strength_details(self, password: str) -> dict:
        """
        获取密码强度的详细信息
        
        Args:
            password: 待检测的密码
            
        Returns:
            dict: 包含详细信息的字典，包括：
                - strength: 强度等级
                - length: 密码长度
                - has_digits: 是否包含数字
                - has_lowercase: 是否包含小写字母
                - has_uppercase: 是否包含大写字母
                - has_special: 是否包含特殊符号
                - char_types_count: 字符类型数量
        """
        if not password:
            raise ValueError("密码不能为空")
        
        details = {
            "strength": self.check(password),
            "length": len(password),
            "has_digits": bool(re.search(r'\d', password)),
            "has_lowercase": bool(re.search(r'[a-z]', password)),
            "has_uppercase": bool(re.search(r'[A-Z]', password)),
            "has_special": bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password)),
            "char_types_count": 0
        }
        
        details["char_types_count"] = sum([
            details["has_digits"],
            details["has_lowercase"],
            details["has_uppercase"],
            details["has_special"]
        ])
        
        return details
    
    def get_suggestions(self, password: str) -> list:
        """
        获取密码改进建议
        
        Args:
            password: 待检测的密码
            
        Returns:
            list: 改进建议列表
        """
        suggestions = []
        details = self.get_strength_details(password)
        
        if details["length"] < 12:
            suggestions.append("建议密码长度至少为12位")
        
        if not details["has_digits"]:
            suggestions.append("建议添加数字")
        
        if not details["has_lowercase"]:
            suggestions.append("建议添加小写字母")
        
        if not details["has_uppercase"]:
            suggestions.append("建议添加大写字母")
        
        if not details["has_special"]:
            suggestions.append("建议添加特殊符号（如!@#$%^&*等）")
        
        if details["char_types_count"] < 3:
            suggestions.append("建议使用至少3种不同类型的字符")
        
        return suggestions
