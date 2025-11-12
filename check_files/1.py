import hashlib
from typing import Dict, Any

class Encryptor:
    def __init__(self, appid: str, appSecret: str):
        self.appid = appid
        self.appSecret = appSecret

    def _sort_params(self, parammap: Dict[str, Any]) -> str:
        """将参数字典按照键的ASCII码升序排列，并转换为字符串"""
        sorted_params = sorted(parammap.items())
        param_str = "&".join(f"{key}={value}" for key, value in sorted_params)
        return param_str

    def _create_sign_source(self, parammap: Dict[str, Any], timestamp: int) -> str:
        """创建签名源字符串"""
        param_str = self._sort_params(parammap)
        sign_source = f"{self.appid}{self.appSecret}{timestamp}{param_str}"
        return sign_source

    def encrypt(self, parammap: Dict[str, Any], timestamp: int, method: str = 'SHA256') -> str:
        """根据选择的加密方式对签名源字符串进行加密"""
        sign_source = self._create_sign_source(parammap, timestamp)
        if method.upper() == 'MD5':
            hasher = hashlib.md5()
        elif method.upper() == 'SHA256':
            hasher = hashlib.sha256()
        elif method.upper() == 'SHA512':
            hasher = hashlib.sha512()
        else:
            raise ValueError("Unsupported encryption method. Choose from 'MD5', 'SHA256', 'SHA512'.")

        hasher.update(sign_source.encode('utf-8'))
        return hasher.hexdigest()

# 使用示例
appid = "your_appid"
appSecret = "your_appSecret"
parammap = {"param1": "value1", "param2": "value2"}
timestamp = 1633036800

encryptor = Encryptor(appid, appSecret)
signature = encryptor.encrypt(parammap, timestamp, method='SHA256')
print("Signature:", signature)
