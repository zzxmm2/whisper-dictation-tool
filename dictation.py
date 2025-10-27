#!/usr/bin/env python3
"""
Speech-to-Text Dictation Tool
Press Alt+D to start recording, speak, then press Alt+D again to stop and transcribe.
The transcribed text will be automatically typed into the active window.
"""

import pyaudio
import wave
import threading
import time
import whisper
from pynput import keyboard
import pyautogui
from datetime import datetime
import os
import warnings
import pyperclip

# Suppress Whisper warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

class DictationTool:
    def __init__(self):
        # Configuration: Choose your preferred model
        # Options: "base" (fastest), "small" (balanced), "medium" (most accurate), "large" (best but slowest)
        self.MODEL_SIZE = "small"  # Change this to balance accuracy vs. speed
        
        self.recording = False
        self.audio = None
        self.frames = []
        self.stream = None
        self.model = None
        self.hotkey = {keyboard.Key.alt, keyboard.KeyCode.from_char('d')}
        self.current_keys = set()
        self.record_thread = None
        self.last_hotkey_time = 0  # Prevent rapid hotkey triggers
        self.hotkey_debounce = 1.0  # Minimum seconds between hotkey triggers
        self.processing = False  # Prevent multiple transcription processes
        
        # Chinese conversion dictionary (common traditional to simplified mappings)
        self._chinese_map = {
            # Common characters
            '現': '现', '說': '说', '聽': '听', '嗎': '吗', '學': '学', '記': '记',
            '這': '这', '個': '个', '裡': '里', '邊': '边', '為': '为', '麼': '么',
            '會': '会', '來': '来', '從': '从', '對': '对', '錯': '错',
            '時': '时', '間': '间', '鐘': '钟', '請': '请', '謝': '谢',
            # Additional characters from your test
            '話': '话', '試': '试', '檢': '检', '體': '体', '還': '还', '是': '是',
            '你': '你', '我': '我', '在': '在', '中': '中', '文': '文', '能': '能',
            '懂': '懂', '到': '到', '去': '去', '來': '来', '到': '到', '得': '得',
            '一': '一', '二': '二', '三': '三', '四': '四', '五': '五', '六': '六',
            '七': '七', '八': '八', '九': '九', '十': '十', '百': '百', '千': '千',
            '萬': '万', '億': '亿', '第': '第', '次': '次', '回': '回', '遍': '遍',
            '種': '种', '類': '类', '樣': '样', '種': '种', '類': '类', '樣': '样',
            '東': '东', '西': '西', '南': '南', '北': '北', '上': '上', '下': '下',
            '左': '左', '右': '右', '前': '前', '後': '后', '內': '内', '外': '外',
            '大': '大', '小': '小', '高': '高', '低': '低', '長': '长', '短': '短',
            '寬': '宽', '窄': '窄', '厚': '厚', '薄': '薄', '重': '重', '輕': '轻',
            '快': '快', '慢': '慢', '新': '新', '舊': '旧', '好': '好', '壞': '坏',
            '美': '美', '醜': '丑', '熱': '热', '冷': '冷', '暖': '暖', '涼': '凉',
            '乾': '干', '濕': '湿', '亮': '亮', '暗': '暗', '強': '强', '弱': '弱',
            '多': '多', '少': '少', '全': '全', '半': '半', '整': '整', '零': '零',
            '單': '单', '雙': '双', '幾': '几', '些': '些', '每': '每', '各': '各',
            '別': '别', '另': '另', '其': '其', '他': '他', '她': '她', '它': '它',
            '們': '们', '的': '的', '地': '地', '得': '得', '了': '了', '着': '着',
            '過': '过', '來': '来', '去': '去', '到': '到', '在': '在', '有': '有',
            '沒': '没', '不': '不', '很': '很', '太': '太', '更': '更', '最': '最',
            '比': '比', '和': '和', '與': '与', '或': '或', '但': '但', '而': '而',
            '因': '因', '為': '为', '所': '所', '以': '以', '把': '把', '被': '被',
            '給': '给', '讓': '让', '叫': '叫', '使': '使', '要': '要', '想': '想',
            '覺': '觉', '知': '知', '道': '道', '看': '看', '見': '见', '聞': '闻',
            '聽': '听', '說': '说', '講': '讲', '談': '谈', '問': '问', '答': '答',
            '寫': '写', '讀': '读', '教': '教', '學': '学', '習': '习', '練': '练',
            '工': '工', '作': '作', '做': '做', '辦': '办', '理': '理', '管': '管',
            '幫': '帮', '助': '助', '支': '支', '持': '持', '保': '保', '護': '护',
            '愛': '爱', '喜': '喜', '歡': '欢', '討': '讨', '厭': '厌', '恨': '恨',
            '怕': '怕', '擔': '担', '心': '心', '擔': '担', '憂': '忧', '愁': '愁',
            '樂': '乐', '笑': '笑', '哭': '哭', '怒': '怒', '氣': '气', '急': '急',
            '忙': '忙', '閒': '闲', '累': '累', '困': '困', '睡': '睡', '醒': '醒',
            '吃': '吃', '喝': '喝', '穿': '穿', '戴': '戴', '住': '住', '行': '行',
            '走': '走', '跑': '跑', '跳': '跳', '坐': '坐', '站': '站', '躺': '躺',
            '買': '买', '賣': '卖', '送': '送', '收': '收', '借': '借', '還': '还',
            '開': '开', '關': '关', '進': '进', '出': '出', '入': '入', '離': '离',
            '回': '回', '來': '来', '去': '去', '到': '到', '從': '从', '向': '向',
            '往': '往', '朝': '朝', '對': '对', '面': '面', '背': '背', '側': '侧',
            '正': '正', '反': '反', '直': '直', '彎': '弯', '平': '平', '斜': '斜',
            '圓': '圆', '方': '方', '尖': '尖', '鈍': '钝', '軟': '软', '硬': '硬',
            '滑': '滑', '粗': '粗', '細': '细', '光': '光', '亮': '亮', '暗': '暗',
            '清': '清', '濁': '浊', '香': '香', '臭': '臭', '甜': '甜', '苦': '苦',
            '酸': '酸', '辣': '辣', '鹹': '咸', '淡': '淡', '濃': '浓', '稀': '稀',
            '深': '深', '淺': '浅', '遠': '远', '近': '近', '早': '早', '晚': '晚',
            '遲': '迟', '快': '快', '慢': '慢', '久': '久', '短': '短', '長': '长',
            '新': '新', '舊': '旧', '老': '老', '少': '少', '年': '年', '月': '月',
            '日': '日', '時': '时', '分': '分', '秒': '秒', '週': '周', '期': '期',
            '季': '季', '節': '节', '春': '春', '夏': '夏', '秋': '秋', '冬': '冬',
            '今': '今', '昨': '昨', '明': '明', '後': '后', '前': '前', '當': '当',
            '現': '现', '過': '过', '將': '将', '要': '要', '會': '会', '能': '能',
            '可': '可', '應': '应', '該': '该', '必': '必', '須': '须', '需': '需',
            '要': '要', '想': '想', '願': '愿', '希': '希', '望': '望', '期': '期',
            '待': '待', '等': '等', '候': '候', '等': '等', '待': '待', '候': '候'
        }
        
        # Audio settings
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024
        
        # Initialize Chinese converter
        self.chinese_converter = self._init_chinese_converter()
        if self.chinese_converter:
            print("Chinese converter initialized (Traditional → Simplified)")
        else:
            print("Chinese converter not available")
        
        # Initialize audio system
        try:
            self.audio = pyaudio.PyAudio()
        except Exception as e:
            print(f"Error initializing audio: {e}")
            return
        
        # Initialize Whisper model
        print("Loading Whisper model... (this may take a moment on first run)")
        try:
            # Model options for better mixed language accuracy:
            # - "base": Good balance of speed/accuracy
            # - "small": Better accuracy, slightly slower
            # - "medium": Best accuracy, slower (RECOMMENDED for mixed languages)
            # - "large": Best accuracy, slowest
            # 
            # Using configurable model size for best balance of accuracy vs. speed
            self.model = whisper.load_model(self.MODEL_SIZE)
            print(f"Whisper model loaded successfully! (Model: {self.MODEL_SIZE})")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            return
        
        # Set up hotkey listener
        try:
            self.listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )
            print("🎤 Dictation tool ready! Press Alt+D to start/stop recording.")
        except Exception as e:
            print(f"Error setting up hotkey listener: {e}")
            return
    
    def _init_chinese_converter(self):
        """Initialize Chinese character converter"""
        return True  # Simple flag to indicate converter is available
    
    def _convert_to_simplified(self, text):
        """Convert traditional Chinese characters to simplified"""
        if not self.chinese_converter:
            return text
        
        converted_text = text
        for traditional, simplified in self._chinese_map.items():
            converted_text = converted_text.replace(traditional, simplified)
        
        return converted_text
    

        
    def on_press(self, key):
        try:
            self.current_keys.add(key)
            if self.hotkey.issubset(self.current_keys):
                current_time = time.time()
                if current_time - self.last_hotkey_time >= self.hotkey_debounce:
                    self.last_hotkey_time = current_time
                    print(f"🔑 Hotkey triggered at {current_time}")
                    self.toggle_recording()
                else:
                    print(f"⏸️  Hotkey ignored (debounced)")
        except AttributeError:
            pass
    
    def on_release(self, key):
        try:
            self.current_keys.discard(key)
        except AttributeError:
            pass
    
    def toggle_recording(self):
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        if self.recording:
            return
            
        self.recording = True
        self.frames = []
        
        # Start recording in a separate thread
        self.record_thread = threading.Thread(target=self._record_audio)
        self.record_thread.daemon = True  # Make thread daemon so it doesn't block exit
        self.record_thread.start()
        
        print("🎤 Recording started... (Press Alt+D again to stop)")
        
    def _record_audio(self):
        try:
            if not self.audio:
                print("Audio system not initialized")
                return
                
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            while self.recording:
                try:
                    data = self.stream.read(self.chunk, exception_on_overflow=False)
                    self.frames.append(data)
                except Exception as e:
                    print(f"Error reading audio: {e}")
                    break
                    
        except Exception as e:
            print(f"Error recording audio: {e}")
            self.recording = False
        finally:
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                except:
                    pass
                self.stream = None
    
    def stop_recording(self):
        if not self.recording:
            return
        
        if self.processing:
            print("⏸️  Already processing, ignoring duplicate request")
            return
            
        self.recording = False
        self.processing = True
        print("⏹️  Recording stopped. Transcribing...")
        
        # Wait for recording thread to finish
        if self.record_thread and self.record_thread.is_alive():
            self.record_thread.join(timeout=2.0)
        
        if self.frames:
            # Save audio to temporary file
            temp_file = f"/tmp/dictation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            if self._save_audio(temp_file):
                # Transcribe with Whisper
                try:
                    print("🔍 Transcribing with Whisper...")
                    
                    # Use better settings for mixed language input
                    result = self.model.transcribe(
                        temp_file,
                        task="transcribe",
                        language=None,  # Let Whisper auto-detect
                        initial_prompt="This is a mixed language conversation in Chinese and English. Please transcribe accurately in both languages.",
                        condition_on_previous_text=False,
                        temperature=0.0  # More deterministic output
                    )
                    
                    transcribed_text = result["text"].strip()
                    
                    if transcribed_text:
                        print(f"📝 Transcribed: {transcribed_text}")
                        
                        # Always convert traditional Chinese characters to simplified
                        simplified_text = self._convert_to_simplified(transcribed_text)
                        
                        # Show conversion if any changes were made
                        if simplified_text != transcribed_text:
                            print(f"🔄 Converted to simplified: {simplified_text}")
                        
                        # Type the text into the active window
                        self._type_text(simplified_text)
                    else:
                        print("❌ No speech detected")
                        
                except Exception as e:
                    print(f"Error transcribing: {e}")
                finally:
                    # Reset processing flag
                    self.processing = False
                
                # Clean up temporary file
                try:
                    os.remove(temp_file)
                except:
                    pass
            else:
                print("❌ Failed to save audio file")
                self.processing = False
    
    def _save_audio(self, filename):
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))
            return True
        except Exception as e:
            print(f"Error saving audio: {e}")
            return False
    
    def _type_text(self, text):
        try:
            print(f"🎯 Attempting to type: '{text}'")
            
            # Small delay to ensure focus is on the target window
            time.sleep(0.2)
            
            # Use clipboard method for better Unicode support
            original_clipboard = pyperclip.paste()
            print(f"📋 Original clipboard content: '{original_clipboard}'")
            
            # Copy text to clipboard
            pyperclip.copy(text)
            
            # Verify clipboard content
            clipboard_content = pyperclip.paste()
            if clipboard_content != text:
                print(f"⚠️  Clipboard verification failed! Expected: '{text}', Got: '{clipboard_content}'")
                # Try direct typing instead
                raise Exception("Clipboard content mismatch")
            
            print(f"📋 Clipboard content verified: '{clipboard_content}'")
            
            # Paste using Ctrl+V
            pyautogui.hotkey('ctrl', 'v')
            
            # Wait a bit longer for paste to complete
            time.sleep(0.3)
            
            # Restore original clipboard content
            pyperclip.copy(original_clipboard)
            
            print("✅ Text typed successfully via clipboard!")
        except Exception as e:
            print(f"❌ Clipboard method failed: {e}")
            print("🔄 Trying direct typing method...")
            
            # Fallback to direct typing if clipboard method fails
            try:
                # Clear any existing text selection first
                pyautogui.hotkey('ctrl', 'a')  # Select all
                time.sleep(0.1)
                pyautogui.press('delete')      # Delete selected text
                time.sleep(0.1)
                
                # Type the text directly
                pyautogui.write(text)
                print("✅ Text typed successfully (direct method)!")
            except Exception as e2:
                print(f"❌ Direct typing also failed: {e2}")
                print("💡 Please manually copy and paste the text from the terminal output")
    
    def run(self):
        """Main loop to keep the program running"""
        try:
            print("Dictation tool is running. Press Ctrl+C to exit.")
            if hasattr(self, 'listener') and self.listener:
                self.listener.start()
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n👋 Exiting dictation tool...")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            # Stop recording if active
            if self.recording:
                self.recording = False
                if self.record_thread and self.record_thread.is_alive():
                    self.record_thread.join(timeout=1.0)
            
            # Close audio stream
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                except:
                    pass
                self.stream = None
            
            # Terminate audio system
            if self.audio:
                try:
                    self.audio.terminate()
                except:
                    pass
                self.audio = None
            
            # Stop listener
            if hasattr(self, 'listener') and self.listener:
                try:
                    self.listener.stop()
                except:
                    pass
        except Exception as e:
            print(f"Error during cleanup: {e}")

def main():
    # Set pyautogui safety settings
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    
    # Create and run dictation tool
    try:
        dictation = DictationTool()
        dictation.run()
    except Exception as e:
        print(f"Failed to start dictation tool: {e}")
        print("Please check your audio setup and try again.")

if __name__ == "__main__":
    main()
