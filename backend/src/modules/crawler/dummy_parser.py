# dummy_parser.py
import re

class DummyParser:
    def parse(self, raw_content):
        # Simulate extracting URLs from raw HTML or JSON text
        urls = re.findall(r'https?://[^\s"\'>]+', str(raw_content))
        return {"urls": urls}