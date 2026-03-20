import sys

class ClipboardManager:
    """
    剪贴板管理器
    
    提供复制文本到系统剪贴板的功能。
    """
    
    @staticmethod
    def copy_to_clipboard(text):
        """
        将文本复制到系统剪贴板
        
        Args:
            text (str): 要复制的文本内容
        
        Returns:
            bool: 复制成功返回True，失败返回False
        """
        try:
            import pyperclip
            pyperclip.copy(text)
            return True
        except ImportError:
            try:
                if sys.platform == 'win32':
                    import subprocess
                    subprocess.run(['clip'], input=text.encode('utf-16'), check=True)
                    return True
                elif sys.platform == 'darwin':
                    import subprocess
                    subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=True)
                    return True
                elif sys.platform.startswith('linux'):
                    import subprocess
                    subprocess.run(['xclip', '-selection', 'clipboard'], 
                                   input=text.encode('utf-8'), check=True)
                    return True
            except Exception:
                return False
        except Exception:
            return False
        
        return False
    
    @staticmethod
    def check_pyperclip_installed():
        """
        检查pyperclip库是否已安装
        
        Returns:
            bool: 已安装返回True，否则返回False
        """
        try:
            import pyperclip
            return True
        except ImportError:
            return False
