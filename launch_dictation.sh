#!/bin/bash

# Simple Whisper Dictation Launcher
# This script launches the dictation tool in the background

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/whisper_env"
PID_FILE="$SCRIPT_DIR/dictation.pid"

# Check if dictation tool is already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        if command -v notify-send >/dev/null 2>&1; then
            notify-send "Whisper Dictation" "Dictation tool is already running (PID: $PID)"
        else
            echo "Dictation tool is already running (PID: $PID)"
        fi
        exit 0
    else
        # PID file exists but process is dead, clean it up
        rm -f "$PID_FILE"
    fi
fi

# Check if any dictation.py processes are running
if pgrep -f "python.*dictation.py" >/dev/null; then
    if command -v notify-send >/dev/null 2>&1; then
        notify-send "Whisper Dictation" "Dictation tool is already running"
    else
        echo "Dictation tool is already running"
    fi
    exit 0
fi

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    # Show error using notify-send if available
    if command -v notify-send >/dev/null 2>&1; then
        notify-send "Whisper Dictation Error" "Virtual environment not found. Please run setup first."
    fi
    exit 1
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Check if activation was successful
if [ $? -ne 0 ]; then
    if command -v notify-send >/dev/null 2>&1; then
        notify-send "Whisper Dictation Error" "Failed to activate virtual environment"
    fi
    exit 1
fi

# Create log file
LOG_FILE="$SCRIPT_DIR/dictation.log"
echo "Starting Whisper Dictation Tool at $(date)" > "$LOG_FILE"

# Launch dictation tool in background
cd "$SCRIPT_DIR"
nohup python dictation.py > "$LOG_FILE" 2>&1 &

# Get the process ID
DICTATION_PID=$!
echo "Dictation tool started with PID: $DICTATION_PID" >> "$LOG_FILE"

# Save PID to file for later use
echo "$DICTATION_PID" > "$PID_FILE"

# Wait a moment to ensure the process started successfully
sleep 1

# Verify the process is still running
if ! kill -0 "$DICTATION_PID" 2>/dev/null; then
    rm -f "$PID_FILE"
    if command -v notify-send >/dev/null 2>&1; then
        notify-send "Whisper Dictation Error" "Failed to start dictation tool. Check log file."
    fi
    exit 1
fi

# Show success notification
if command -v notify-send >/dev/null 2>&1; then
    notify-send "Whisper Dictation" "Dictation tool started successfully!\n\nUse Alt+D to start/stop recording\nCheck $LOG_FILE for details"
else
    echo "Dictation tool started successfully!"
    echo "Use Alt+D to start/stop recording"
    echo "Check $LOG_FILE for details"
fi

# Exit the launcher (tool continues running in background)
exit 0
