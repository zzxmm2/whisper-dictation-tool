#!/usr/bin/env python3
"""
Test script for Chinese character conversion
"""

class TestChineseConverter:
    def __init__(self):
        # Chinese conversion dictionary (same as in dictation.py)
        self._chinese_map = {
            '現': '现', '說': '说', '聽': '听', '嗎': '吗', '學': '学', '記': '记',
            '這': '这', '個': '个', '裡': '里', '邊': '边', '為': '为', '麼': '么',
            '會': '会', '來': '来', '從': '从', '對': '对', '錯': '错',
            '時': '时', '間': '间', '鐘': '钟', '請': '请', '謝': '谢',
            '話': '话', '試': '试', '檢': '检', '體': '体', '還': '还'
        }
    
    def convert_to_simplified(self, text):
        """Convert traditional Chinese characters to simplified"""
        converted_text = text
        for traditional, simplified in self._chinese_map.items():
            converted_text = converted_text.replace(traditional, simplified)
        return converted_text

def main():
    converter = TestChineseConverter()
    
    # Test cases
    test_cases = [
        "你好，這是繁體中文測試。",
        "Hello, this is English text.",
        "混合語言測試：Hello 世界！",
        "繁體字：現說聽嗎學記這個裡邊為麼會來從對錯時間鐘請謝",
        "簡體字：现说听吗学记这个里边为么会来从对错时间钟请谢"
    ]
    
    print("🧪 Testing Chinese Character Conversion")
    print("=" * 50)
    
    for i, test_text in enumerate(test_cases, 1):
        converted = converter.convert_to_simplified(test_text)
        print(f"Test {i}:")
        print(f"  Original: {test_text}")
        print(f"  Converted: {converted}")
        print(f"  Changed: {'Yes' if converted != test_text else 'No'}")
        print()

if __name__ == "__main__":
    main()
