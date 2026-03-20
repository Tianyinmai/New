"""
剪贴板操作模块
提供复制到剪贴板的功能
"""

import sys


class ClipboardManager:
    """剪贴板管理器类"""
    
    def __init__(self):
        """初始化剪贴板管理器，尝试导入pyperclip"""
        self.pyperclip_available = False
        self._try_import_pyperclip()
    
    def _try_import_pyperclip(self):
        """尝试导入pyperclip库"""
        try:
            import pyperclip
            self.pyperclip = pyperclip
            self.pyperclip_available = True
        except ImportError:
            self.pyperclip_available = False
    
    def copy(self, text: str) -> bool:
        """
        复制文本到剪贴板
        
        Args:
            text: 要复制的文本
            
        Returns:
            bool: 复制是否成功
        """
        if not text:
            return False
        
        # 优先使用pyperclip
        if self.pyperclip_available:
            try:
                self.pyperclip.copy(text)
                return True
            except Exception as e:
                print(f"pyperclip复制失败: {e}")
                return self._fallback_copy(text)
        else:
            return self._fallback_copy(text)
    
    def _fallback_copy(self, text: str) -> bool:
        """
        备用复制方法（当pyperclip不可用时使用）
        
        Args:
            text: 要复制的文本
            
        Returns:
            bool: 复制是否成功
        """
        try:
            if sys.platform == "win32":
                # Windows: 使用clip命令
                import subprocess
                subprocess.run(
                    ["clip"], 
                    input=text.encode('utf-16le'), 
                    check=True,
                    shell=True
                )
                return True
            elif sys.platform == "darwin":
                # macOS: 使用pbcopy命令
                import subprocess
                subprocess.run(
                    ["pbcopy"], 
                    input=text.encode('utf-8'), 
                    check=True
                )
                return True
            elif sys.platform.startswith("linux"):
                # Linux: 尝试使用xclip或xsel
                import subprocess
                # 尝试xclip
                try:
                    subprocess.run(
                        ["xclip", "-selection", "clipboard"], 
                        input=text.encode('utf-8'), 
                        check=True
                    )
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass
                
                # 尝试xsel
                try:
                    subprocess.run(
                        ["xsel", "--clipboard", "--input"], 
                        input=text.encode('utf-8'), 
                        check=True
                    )
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass
            
            # 如果所有方法都失败
            return False
        except Exception as e:
            print(f"备用复制方法失败: {e}")
            return False
    
    def paste(self) -> str:
        """
        从剪贴板粘贴文本
        
        Returns:
            str: 剪贴板内容，失败返回空字符串
        """
        if self.pyperclip_available:
            try:
                return self.pyperclip.paste()
            except Exception as e:
                print(f"pyperclip粘贴失败: {e}")
                return self._fallback_paste()
        else:
            return self._fallback_paste()
    
    def _fallback_paste(self) -> str:
        """
        备用粘贴方法（当pyperclip不可用时使用）
        
        Returns:
            str: 剪贴板内容，失败返回空字符串
        """
        try:
            if sys.platform == "win32":
                # Windows: 使用PowerShell获取剪贴板
                import subprocess
                result = subprocess.run(
                    ["powershell", "-command", "Get-Clipboard"],
                    capture_output=True,
                    text=True,
                    check=True,
                    shell=True
                )
                return result.stdout.strip()
            elif sys.platform == "darwin":
                # macOS: 使用pbpaste命令
                import subprocess
                result = subprocess.run(
                    ["pbpaste"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout
            elif sys.platform.startswith("linux"):
                # Linux: 尝试使用xclip或xsel
                import subprocess
                # 尝试xclip
                try:
                    result = subprocess.run(
                        ["xclip", "-selection", "clipboard", "-o"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    return result.stdout
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass
                
                # 尝试xsel
                try:
                    result = subprocess.run(
                        ["xsel", "--clipboard", "--output"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    return result.stdout
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass
            
            return ""
        except Exception as e:
            print(f"备用粘贴方法失败: {e}")
            return ""
    
    def is_available(self) -> bool:
        """
        检查剪贴板功能是否可用
        
        Returns:
            bool: 剪贴板功能是否可用
        """
        # 测试复制功能
        test_text = "test"
        return self.copy(test_text)
    
    def get_status_message(self) -> str:
        """
        获取剪贴板功能状态信息
        
        Returns:
            str: 状态信息
        """
        if self.pyperclip_available:
            return "剪贴板功能可用（使用pyperclip）"
        else:
            return "剪贴板功能可用（使用系统命令）" if self.is_available() else "剪贴板功能不可用"


# 创建全局剪贴板管理器实例
clipboard = ClipboardManager()


def copy_to_clipboard(text: str) -> bool:
    """
    复制文本到剪贴板的便捷函数
    
    Args:
        text: 要复制的文本
        
    Returns:
        bool: 复制是否成功
    """
    return clipboard.copy(text)


def paste_from_clipboard() -> str:
    """
    从剪贴板粘贴文本的便捷函数
    
    Returns:
        str: 剪贴板内容
    """
    return clipboard.paste()
