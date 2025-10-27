# 🎤 Whisper Dictation Tool

A powerful speech-to-text dictation tool that uses OpenAI's Whisper model to transcribe speech and automatically type it into the active window. Perfect for multilingual dictation with special support for Chinese-English mixed speech.

## ✨ Features

- 🎤 **Hotkey Control**: Press `Alt+D` to start/stop recording
- 🗣️ **Real-time Transcription**: Uses Whisper for accurate speech recognition
- 🌍 **Smart Mixed Language**: Optimized for Chinese-English mixed speech with fallback transcription
- 🇨🇳 **Simplified Chinese**: Automatically converts traditional Chinese characters to simplified
- 🇺🇸 **Universal Support**: Works with any language Whisper supports
- ⌨️ **Auto-typing**: Automatically types transcribed text into the active window
- 🖥️ **GUI Interface**: User-friendly graphical interface
- 🔧 **Easy Setup**: Simple installation script with virtual environment management
- 🚀 **Background Mode**: Run in background for continuous use

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/whisper-dictation-tool.git
   cd whisper-dictation-tool
   ```

2. **Run the installation script:**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Launch the tool:**
   - **GUI Mode**: `./start_dictation_gui.sh`
   - **Background Mode**: `./launch_dictation.sh`
   - **From Applications Menu**: Search for "Whisper Dictation"

## Usage

### Quick Start

1. **From Applications Menu**: Search for "Whisper Dictation" in your applications menu
2. **From Terminal**: Type `whisper` (after restarting terminal) or `~/APPS/Whisper/start_dictation.sh`
3. **From Favorites**: Add to your favorites for quick access

### How to Use

1. **Start the tool** - Launch the application
2. **Position cursor** - Click in the text field where you want the text to appear
3. **Start recording** - Press `Alt+D` (you'll see "Recording started...")
4. **Speak clearly** - Talk into your microphone in any language
5. **Stop recording** - Press `Alt+D` again (you'll see "Recording stopped. Transcribing...")
6. **Wait for transcription** - Whisper will transcribe your speech
7. **Text appears** - The transcribed text will be automatically typed, with traditional Chinese converted to simplified

### Controls

- `Alt+D` - Start/stop recording
- `Ctrl+C` - Exit the application

## Requirements

- **Microphone**: Working microphone input
- **Audio**: PortAudio support (already installed)
- **Python**: Python 3.11 with required packages (already set up)
- **Hotkey**: Uses pynput library (no root privileges required)

## Troubleshooting

### No Audio Input
- Check microphone permissions
- Ensure microphone is not muted
- Test microphone in system settings

### Transcription Issues
- Speak clearly and at normal volume
- Reduce background noise
- Ensure good microphone quality

### Mixed Language Issues
- If Chinese parts come out as garbage, try speaking more slowly
- Ensure clear pronunciation of both languages
- The app now has automatic fallback transcription for mixed languages
- Uses the "small" Whisper model for balanced mixed language accuracy and speed

### Hotkey Not Working
- Make sure the application has focus
- Check if `Alt+D` conflicts with other applications
- The tool uses pynput library (no root privileges required)
- Ensure no other applications are capturing the Alt+D combination

## Files

- `dictation.py` - Main Python script
- `start_dictation.sh` - Launcher script
- `whisper_env/` - Python virtual environment
- **System Integration**: Added to applications menu and favorites

## Technical Details

- **Audio Format**: 16-bit PCM, 16kHz, mono
- **Whisper Model**: Small model (balanced accuracy and speed for mixed languages)
- **Language Processing**: Smart transcription with fallback for mixed Chinese-English
- **Fallback System**: Automatically tries alternative transcription if first attempt is poor
- **Hotkey Library**: Python keyboard library
- **Auto-typing**: PyAutoGUI for cross-platform text input

## Support

If you encounter issues:
1. Check the terminal output for error messages
2. Ensure all dependencies are installed
3. Verify microphone permissions
4. Test with a simple text editor first
