#!/bin/bash

# Whisper Dictation Tool Launcher (GUI Mode)
# This script activates the virtual environment and starts the dictation tool

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/whisper_env"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    # Show error dialog if possible
    if command -v zenity >/dev/null 2>&1; then
        zenity --error --title="Whisper Dictation Error" --text="Virtual environment not found at $VENV_PATH\n\nPlease run the setup script first."
    else
        echo "Error: Virtual environment not found at $VENV_PATH"
        echo "Please run the setup script first."
        read -p "Press Enter to continue..."
    fi
    exit 1
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Check if activation was successful
if [ $? -ne 0 ]; then
    if command -v zenity >/dev/null 2>&1; then
        zenity --error --title="Whisper Dictation Error" --text="Failed to activate virtual environment"
    else
        echo "Error: Failed to activate virtual environment"
        read -p "Press Enter to continue..."
    fi
    exit 1
fi

# Create a log file for debugging
LOG_FILE="$SCRIPT_DIR/dictation.log"
echo "Starting Whisper Dictation Tool at $(date)" > "$LOG_FILE"

# Run the dictation tool and redirect output to log file
echo "Starting dictation tool..." >> "$LOG_FILE"
python "$SCRIPT_DIR/dictation.py" >> "$LOG_FILE" 2>&1

# If we get here, the tool has exited
echo "Dictation tool exited at $(date)" >> "$LOG_FILE"

# Keep the window open if there was an error
if [ $? -ne 0 ]; then
    if command -v zenity >/dev/null 2>&1; then
        zenity --info --title="Whisper Dictation" --text="The dictation tool has stopped.\n\nCheck the log file for details: $LOG_FILE"
    else
        echo "The dictation tool has stopped. Check the log file for details: $LOG_FILE"
        read -p "Press Enter to continue..."
    fi
fi
