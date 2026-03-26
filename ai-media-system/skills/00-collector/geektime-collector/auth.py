import os
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class AuthHandler:
    def __init__(self):
        self.cookie = os.getenv("GEEKTIME_COOKIE", "")
        self.user_agent = os.getenv(
            "GEEKTIME_USER_AGENT",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        self.proxy_url = os.getenv("PROXY_URL", "")

    def get_headers(self) -> Dict[str, str]:
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        if self.cookie:
            headers["Cookie"] = self.cookie
        return headers

    def get_proxy_config(self) -> Optional[Dict[str, str]]:
        if not self.proxy_url:
            return None
        return {"server": self.proxy_url}

    def is_authenticated(self) -> bool:
        return bool(self.cookie)
