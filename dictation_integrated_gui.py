#!/usr/bin/env python3
"""
Integrated GUI for Whisper Dictation Tool
Combines the original dictation.py functionality with a modern GUI interface.
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
import os
import sys
import pyaudio
import wave
import whisper
from pynput import keyboard
import pyautogui
from datetime import datetime
import warnings
import pyperclip
import psutil

# Suppress Whisper warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

class IntegratedDictationGUI:
    def __init__(self):
        # Check for existing dictation processes
        if self._check_existing_processes():
            print("❌ Another dictation process is already running!")
            print("💡 Please close the existing process before starting a new one.")
            sys.exit(1)
        
        self.root = tk.Tk()
        self.root.title("whisper")
        self.root.geometry("200x100")
        self.root.resizable(False, False)
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Position window in top-right corner
        self.position_window()
        
        # Initialize variables (same as original dictation.py)
        self.MODEL_SIZE = "small"
        self.recording = False
        self.processing = False
        self.audio = None
        self.frames = []
        self.stream = None
        self.model = None
        # Use F9 to avoid browser address bar focus (Alt+D)
        self.current_keys = set()
        self.record_thread = None
        self.last_hotkey_time = 0
        self.hotkey_debounce = 1.0
        self.flash_thread = None
        self.flash_running = False
        
        # Audio settings (same as original)
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024
        
        # Chinese conversion dictionary (from original dictation.py)
        self._chinese_map = {
            '現': '现', '說': '说', '聽': '听', '嗎': '吗', '學': '学', '記': '记',
            '這': '这', '個': '个', '裡': '里', '邊': '边', '為': '为', '麼': '么',
            '會': '会', '來': '来', '從': '从', '對': '对', '錯': '错',
            '時': '时', '間': '间', '鐘': '钟', '請': '请', '謝': '谢',
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
        
        self.setup_ui()
        self.initialize_audio()
        self.initialize_whisper()
        self.setup_hotkey_listener()
        
    def position_window(self):
        """Position window in top-right corner"""
        screen_width = self.root.winfo_screenwidth()
        # Place about 25% of screen width away from the right edge
        window_width = 200
        right_margin = int(screen_width * 0.25)
        x = max(0, screen_width - right_margin - window_width)
        y = 20
        self.root.geometry(f"200x100+{x}+{y}")
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='lightgray', relief='raised', bd=1)
        main_frame.pack(fill='both', expand=True)
        
        # Instruction text
        instruction_label = tk.Label(
            main_frame, 
            text="Pkease use 'Alt + F9' to start/stop", 
            font=("Arial", 8), 
            bg='lightgray', 
            fg='black'
        )
        instruction_label.pack(pady=(5, 0))
        
        # Microphone icon (non-clickable)
        self.mic_label = tk.Label(
            main_frame, 
            text="●", 
            font=("Arial", 32, "bold"), 
            bg='lightgray', 
            fg='gray'
        )
        self.mic_label.pack(expand=True)
        
        # Status label
        self.status_label = tk.Label(
            main_frame, 
            text="Ready", 
            font=("Arial", 8), 
            bg='lightgray', 
            fg='black'
        )
        self.status_label.pack()
        
        # Make the window draggable (but not on the microphone icon)
        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.drag_window)
        
    def start_drag(self, event):
        """Start dragging the window"""
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def drag_window(self, event):
        """Drag the window"""
        x = self.root.winfo_x() + (event.x - self.drag_start_x)
        y = self.root.winfo_y() + (event.y - self.drag_start_y)
        self.root.geometry(f"+{x}+{y}")
    
    def initialize_audio(self):
        """Initialize audio system (same as original)"""
        try:
            self.audio = pyaudio.PyAudio()
        except Exception as e:
            self.show_error(f"Audio initialization failed: {e}")
    
    def initialize_whisper(self):
        """Initialize Whisper model (same as original)"""
        def load_model():
            try:
                print("Loading Whisper model... (this may take a moment on first run)")
                self.model = whisper.load_model(self.MODEL_SIZE)
                print(f"Whisper model loaded successfully! (Model: {self.MODEL_SIZE})")
                self.root.after(0, lambda: self.status_label.config(text="Ready"))
            except Exception as e:
                print(f"Error loading Whisper model: {e}")
                self.root.after(0, lambda: self.show_error(f"Whisper model failed: {e}"))
        
        # Load model in background thread
        threading.Thread(target=load_model, daemon=True).start()
        self.status_label.config(text="Loading...")
    
    def setup_hotkey_listener(self):
        """Setup global hotkey listener (same as original)"""
        try:
            self.listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )
            self.listener.start()
            print("🎤 Dictation tool ready! Press Alt+F9 to start/stop recording.")
        except Exception as e:
            self.show_error(f"Hotkey listener failed: {e}")
    
    def on_press(self, key):
        """Handle key press events (same as original)"""
        try:
            # Track currently pressed keys
            self.current_keys.add(key)

            # Trigger on Alt+F9 to avoid conflicting browser shortcuts
            is_alt = any(k in self.current_keys for k in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r))
            is_f9_now = (key == keyboard.Key.f9)
            is_f9_held = (keyboard.Key.f9 in self.current_keys)
            if is_alt and (is_f9_now or is_f9_held):
                current_time = time.time()
                if current_time - self.last_hotkey_time >= self.hotkey_debounce:
                    self.last_hotkey_time = current_time
                    self.root.after(0, self.toggle_recording)
        except AttributeError:
            pass
    
    def on_release(self, key):
        """Handle key release events (same as original)"""
        try:
            self.current_keys.discard(key)
        except AttributeError:
            pass
    
    def toggle_recording(self):
        """Toggle recording state (same as original)"""
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Start recording (same as original)"""
        if self.recording:
            return
            
        self.recording = True
        self.frames = []
        
        # Update UI
        self.mic_label.config(fg='red')  # Red
        self.status_label.config(text="Recording...")
        
        # Start flashing
        self.start_flashing()
        
        # Start recording in a separate thread (same as original)
        self.record_thread = threading.Thread(target=self._record_audio)
        self.record_thread.daemon = True
        self.record_thread.start()
        
        print("🎤 Recording started... (Press Alt+F9 again to stop)")
    
    def start_flashing(self):
        """Start flashing animation"""
        if self.flash_running:
            return
        
        self.flash_running = True
        self.flash_thread = threading.Thread(target=self._flash_animation, daemon=True)
        self.flash_thread.start()
    
    def stop_flashing(self):
        """Stop flashing animation"""
        self.flash_running = False
        if self.flash_thread:
            self.flash_thread.join(timeout=0.1)
    
    def _flash_animation(self):
        """Flash animation between red and yellow"""
        while self.flash_running and self.recording:
            self.root.after(0, lambda: self.mic_label.config(fg='red'))  # Red
            time.sleep(0.5)
            if not self.flash_running or not self.recording:
                break
            self.root.after(0, lambda: self.mic_label.config(fg='orange'))  # Orange
            time.sleep(0.5)
    
    def _record_audio(self):
        """Record audio in background thread (same as original)"""
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
        """Stop recording and transcribe (same as original)"""
        if not self.recording:
            return
        
        if self.processing:
            print("⏸️  Already processing, ignoring duplicate request")
            return
            
        self.recording = False
        self.processing = True
        
        # Stop flashing
        self.stop_flashing()
        
        # Update UI
        self.mic_label.config(fg='gray')  # Gray
        self.status_label.config(text="Processing...")
        
        print("⏹️  Recording stopped. Transcribing...")
        
        # Wait for recording thread to finish (same as original)
        if self.record_thread and self.record_thread.is_alive():
            self.record_thread.join(timeout=2.0)
        
        if self.frames:
            # Save audio to temporary file (same as original)
            temp_file = f"/tmp/dictation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            if self._save_audio(temp_file):
                # Process audio in background
                threading.Thread(target=self._process_audio, args=(temp_file,), daemon=True).start()
            else:
                print("❌ Failed to save audio file")
                self.processing = False
        else:
            self.processing = False
    
    def _process_audio(self, temp_file):
        """Process recorded audio (same as original)"""
        try:
            if not self.model:
                self.root.after(0, lambda: self.status_label.config(text="Ready"))
                self.processing = False
                return
            
            # Transcribe with Whisper (same as original)
            print("🔍 Transcribing with Whisper...")
            
            result = self.model.transcribe(
                temp_file,
                task="transcribe",
                language="zh",  # Prefer Chinese; English will still be transcribed as-is
                initial_prompt="本段可能包含中英混合语音。请将中文部分优先以简体中文输出，英文保持原文。",
                condition_on_previous_text=False,
                temperature=0.0  # More deterministic output
            )
            
            transcribed_text = result["text"].strip()
            
            if transcribed_text:
                print(f"📝 Transcribed: {transcribed_text}")
                
                # Always convert traditional Chinese characters to simplified (same as original)
                simplified_text = self._convert_to_simplified(transcribed_text)
                
                # Show conversion if any changes were made
                if simplified_text != transcribed_text:
                    print(f"🔄 Converted to simplified: {simplified_text}")
                
                # Type the text into the active window (same as original)
                self.root.after(0, lambda: self._type_text(simplified_text))
            else:
                print("❌ No speech detected")
                self.root.after(0, lambda: self.status_label.config(text="No speech"))
                
        except Exception as e:
            print(f"Error transcribing: {e}")
            self.root.after(0, lambda: self.status_label.config(text="Error"))
        finally:
            # Reset processing flag
            self.processing = False
            self.root.after(0, lambda: self.status_label.config(text="Ready"))
            
            # Clean up temporary file (same as original)
            try:
                os.remove(temp_file)
            except:
                pass
    
    def _save_audio(self, filename):
        """Save recorded audio to file (same as original)"""
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
    
    def _convert_to_simplified(self, text):
        """Convert traditional Chinese to simplified (same as original)"""
        converted_text = text
        for traditional, simplified in self._chinese_map.items():
            converted_text = converted_text.replace(traditional, simplified)
        return converted_text
    
    def _type_text(self, text):
        """Type text into active window (same as original)"""
        try:
            print(f"🎯 Attempting to type: '{text}'")
            
            # Small delay to ensure focus is on the target window
            time.sleep(0.2)
            
            # Use clipboard method for better Unicode support (same as original)
            original_clipboard = pyperclip.paste()
            
            # Clear clipboard first to avoid contamination
            pyperclip.copy("")
            time.sleep(0.1)
            
            # Copy text to clipboard
            pyperclip.copy(text)
            
            # Verify clipboard content
            clipboard_content = pyperclip.paste()
            if clipboard_content != text:
                print(f"⚠️  Clipboard verification failed! Expected: '{text}', Got: '{clipboard_content}'")
                # Try direct typing instead
                raise Exception("Clipboard content mismatch")
            
            # Paste using Ctrl+V
            pyautogui.hotkey('ctrl', 'v')
            
            # Wait a bit longer for paste to complete
            time.sleep(0.5)
            
            # Don't restore clipboard immediately to avoid triggering additional paste
            # Only restore if original content was not empty and not too long
            if original_clipboard and len(original_clipboard) < 100:
                time.sleep(0.5)  # Longer delay before restoring
                pyperclip.copy(original_clipboard)
            
            print("✅ Text typed successfully via clipboard!")
            self.status_label.config(text="Text typed!")
            
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
                self.status_label.config(text="Text typed!")
            except Exception as e2:
                print(f"❌ Direct typing also failed: {e2}")
                print("💡 Please manually copy and paste the text from the terminal output")
                self.status_label.config(text="Type error")
    
    def show_error(self, message):
        """Show error message"""
        self.status_label.config(text="Error")
        messagebox.showerror("Error", message)
    
    def _check_existing_processes(self):
        """Check if another dictation process is already running"""
        try:
            current_pid = os.getpid()
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # Check if it's a Python process
                    if proc.info['name'] and 'python' in proc.info['name'].lower():
                        cmdline = proc.info['cmdline']
                        if cmdline and len(cmdline) > 1:
                            # Check if it's running dictation-related scripts
                            script_name = cmdline[1] if len(cmdline) > 1 else ""
                            if any(keyword in script_name.lower() for keyword in ['dictation', 'whisper']):
                                # Skip current process
                                if proc.info['pid'] != current_pid:
                                    return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            return False
        except Exception as e:
            print(f"⚠️  Error checking existing processes: {e}")
            return False
    
    def close_app(self):
        """Close the application (same cleanup as original)"""
        # Stop recording if active
        if self.recording:
            self.recording = False
            self.stop_flashing()
        
        # Stop processing
        self.processing = False
        
        # Clean up audio (same as original)
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
            self.stream = None
        
        if self.audio:
            try:
                self.audio.terminate()
            except:
                pass
            self.audio = None
        
        # Stop listener (same as original)
        if hasattr(self, 'listener') and self.listener:
            try:
                self.listener.stop()
            except:
                pass
        
        print("👋 Exiting dictation tool...")
        # Close window
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Application error: {e}")

def main():
    """Main entry point"""
    # Set pyautogui safety settings (same as original)
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    
    try:
        app = IntegratedDictationGUI()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
