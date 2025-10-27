#!/bin/bash

# Whisper Dictation Tool Installation Script
# This script sets up the virtual environment and installs all dependencies

set -e  # Exit on any error

echo "🎤 Whisper Dictation Tool - Installation Script"
echo "=============================================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python $RETHON_VERSION is installed, but Python $REQUIRED_VERSION or higher is required."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "whisper_env" ]; then
    echo "⚠️  Virtual environment already exists. Removing old one..."
    rm -rf whisper_env
fi

python3 -m venv whisper_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source whisper_env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Test installation
echo "🧪 Testing installation..."
python -c "import whisper, pyaudio, pynput, pyautogui, pyperclip; print('✅ All dependencies installed successfully!')"

# Create desktop entry
echo "🖥️  Creating desktop entry..."
DESKTOP_ENTRY="$HOME/.local/share/applications/whisper-dictation.desktop"
cat > "$DESKTOP_ENTRY" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Whisper Dictation
GenericName=Speech-to-Text Dictation
Comment=Speech-to-Text Dictation Tool using OpenAI Whisper
Exec=$SCRIPT_DIR/launch_dictation.sh
Icon=audio-input-microphone
Terminal=false
Categories=AudioVideo;Audio;Utility;Accessibility;
Keywords=dictation;speech;whisper;transcription;accessibility;
StartupNotify=true
StartupWMClass=whisper-dictation
EOF

chmod +x "$DESKTOP_ENTRY"

# Make scripts executable
chmod +x launch_dictation.sh
chmod +x start_dictation_gui.sh

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Usage:"
echo "  • GUI Mode: ./start_dictation_gui.sh"
echo "  • Background Mode: ./launch_dictation.sh"
echo "  • From Applications Menu: Search for 'Whisper Dictation'"
echo ""
echo "🎤 Controls:"
echo "  • Alt+D: Start/stop recording"
echo "  • Ctrl+C: Exit the application"
echo ""
echo "📖 For more information, see README.md"
