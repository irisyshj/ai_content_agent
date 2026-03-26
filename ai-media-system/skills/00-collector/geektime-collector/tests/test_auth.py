# Import from parent package using relative import
import sys
from pathlib import Path

# Ensure we can import from parent package
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from auth import AuthHandler
import os

def test_auth_handler_loads_from_env():
    os.environ["GEEKTIME_COOKIE"] = "test_cookie_value"
    auth = AuthHandler()
    assert auth.cookie == "test_cookie_value"

def test_auth_handler_get_headers():
    os.environ["GEEKTIME_COOKIE"] = "test_cookie"
    os.environ["GEEKTIME_USER_AGENT"] = "TestAgent/1.0"
    auth = AuthHandler()
    headers = auth.get_headers()
    assert "Cookie" in headers
    assert headers["Cookie"] == "test_cookie"
    assert headers["User-Agent"] == "TestAgent/1.0"
