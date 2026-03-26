import sys
from pathlib import Path

# Add the collector package to Python path for imports
collector_path = Path(__file__).parent.parent
sys.path.insert(0, str(collector_path))

def pytest_configure(config):
    """Register custom pytest markers"""
    config.addinivalue_line("markers", "integration: Integration tests that require external dependencies (e.g., GEEKTIME_COOKIE)")
