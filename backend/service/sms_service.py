import json
import time
from typing import List
import requests
import hashlib
from typing import Dict, Any


class Encryptor:
    def __init__(self, appid: str, appSecret: str):
        self.appid = appid
        self.appSecret = appSecret

    def _sort_params(self, parammap: Dict[str, Any]) -> str:
        """将参数字典按照键的ASCII码升序排列，并转换为字符串"""
        sorted_params = parammap.items()
        param_str = "&".join(f"{key}={value}" for key, value in sorted_params)
        return param_str

    def _create_sign_source(self, parammap: Dict[str, Any], timestamp: int) -> str:
        """创建签名源字符串"""
        param_str1 = f"appid={self.appid}"+f"&appSecret={self.appSecret}"+f"&timestamp={timestamp}"
        param_str = self._sort_params(parammap)
        sign_source = param_str1 +'&' + param_str
        print(sign_source.replace("'",'"').replace(' ',''))
        return sign_source.replace("'",'"').replace(' ','')

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


class CommonPlatformShortMessageService:
    def __init__(self, config: Dict[str, Any]):
        """
        初始化短信服务
        :param config: 配置字典，包含以下字段：
            - openEnable: 是否启用短信服务
            - messageUrl: 短信接口地址
            - messageAppId: 应用ID
            - messageAppKey: 应用密钥
            - templateMapping: 模板ID映射字典（数字ID到字符串ID）
        """
        self.config = config

    def send_short_message(self, mobile: str, template_id: int, content: List[str]) -> bool:
        """
        发送短信
        :param mobile: 手机号
        :param template_id: 模板ID（数字）
        :param content: 模板变量列表
        :return: 是否发送成功
        """
        if not self.config.get("openEnable", True):
            return True

        param_map = {
            "targetPhoneList":[mobile],
            "templateId": self._get_template_id(template_id),
            "templateVariableList": content,
        }

        timestamp = int(time.time() * 1000)
        sign = self._generate_sign(param_map, timestamp)
        headers = self._build_headers(sign, timestamp)
        post_url = self.config["messageUrl"]
        response = requests.post(
            post_url,
            headers=headers,
            data=json.dumps(param_map, ensure_ascii=False).encode("utf-8"),
            timeout=10
        )

        print(f"发送短信结果：{response.json()}")
        if response.json().get('msg') == '发送完成':
            return True
        return False

    def _generate_sign(self, param_map: Dict[str, Any], timestamp: int) -> str:
        """
        生成签名
        :param param_map: 请求参数
        :param timestamp: 时间戳
        :return: 签名字符串
        """
        encryptor = Encryptor(self.config.get('messageAppId'), self.config.get('messageAppKey'))
        signature = encryptor.encrypt(param_map, timestamp, method='SHA512')

        return signature

    def _build_headers(self, sign: str, timestamp: int) -> Dict[str, str]:
        """
        构建请求头
        :param sign: 签名
        :param timestamp: 时间戳
        :return: 请求头字典
        """
        return {
            "appid": self.config["messageAppId"],
            "signType": "SHA512",
            "sign": sign,
            "timestamp": str(timestamp),
            "Content-Type": "application/json;charset=UTF-8"
        }

    def _get_template_id(self, template_id: int) -> str:
        """
        获取模板主键
        :param template_id: 模板数字ID
        :return: 字符串类型的模板ID
        """
        return self.config["templateMapping"].get(template_id, "")

    def verify_sign(self, mobile,template_id,content,original_sign: str) -> bool:
        """
        验证签名
        :param param_map: 请求参数
        :param timestamp: 时间戳
        :param original_sign: 原始签名字符串
        :return: 如果签名匹配，则返回 True，否则返回 False
        """
        # 重新生成签名
        param_map = {
            "templateVariableList": content,
            "templateId": self._get_template_id(template_id),
            "phone": mobile
        }
        timestamp = 1758179881041
        new_sign = self._generate_sign(param_map, timestamp)

        # 比较新生成的签名与原始签名
        return new_sign == original_sign

# 示例用法
if __name__ == "__main__":
    config = {
        "openEnable": True,
        "messageUrl": "http://182.129.202.234:20083/pr-api/system/sendMsg/batch",
        "messageAppId": "f17806f3bdee4df9ab2ef1025192ea66",
        "messageAppKey": "qfR0wpiQLMecIMp2S9mEJffQ1wTQFmeJ",
        "templateMapping": {
            1: "de93769423184975b5de3c94c0e9bfc9",
            2: "cafb0e0dd1af47de8981b5ee65562795"
        }
    }

    service = CommonPlatformShortMessageService(config)
    service.send_short_message("18560853934", 1, ["测试","23","13","2","52","系统","123"])
