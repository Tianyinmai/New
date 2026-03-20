import re

class StrengthChecker:
    """
    密码强度检测器
    
    根据密码的长度、字符类型多样性等因素评估密码强度。
    """
    
    @staticmethod
    def check_strength(password):
        """
        检测密码强度
        
        评估规则：
        - 长度：6-8位（+1分），9-12位（+2分），13-32位（+3分）
        - 包含数字（+1分）
        - 包含小写字母（+1分）
        - 包含大写字母（+1分）
        - 包含特殊符号（+2分）
        
        Args:
            password (str): 待检测的密码
        
        Returns:
            str: 密码强度等级，返回值为'弱'、'中'或'强'
        """
        if not password:
            return '弱'
        
        score = 0
        
        if len(password) >= 13:
            score += 3
        elif len(password) >= 9:
            score += 2
        elif len(password) >= 6:
            score += 1
        
        if re.search(r'[0-9]', password):
            score += 1
        
        if re.search(r'[a-z]', password):
            score += 1
        
        if re.search(r'[A-Z]', password):
            score += 1
        
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 2
        
        if score <= 3:
            return '弱'
        elif score <= 5:
            return '中'
        else:
            return '强'
    
    @staticmethod
    def get_strength_detail(password):
        """
        获取密码强度详细信息
        
        Args:
            password (str): 待检测的密码
        
        Returns:
            dict: 包含强度等级和各项评分详情的字典
        """
        details = {
            '强度': StrengthChecker.check_strength(password),
            '长度得分': 0,
            '包含数字': False,
            '包含小写字母': False,
            '包含大写字母': False,
            '包含特殊符号': False
        }
        
        if len(password) >= 13:
            details['长度得分'] = 3
        elif len(password) >= 9:
            details['长度得分'] = 2
        elif len(password) >= 6:
            details['长度得分'] = 1
        
        details['包含数字'] = bool(re.search(r'[0-9]', password))
        details['包含小写字母'] = bool(re.search(r'[a-z]', password))
        details['包含大写字母'] = bool(re.search(r'[A-Z]', password))
        details['包含特殊符号'] = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        
        return details
