#!/bin/bash
# Start script for Integrated Whisper Dictation GUI

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment
source "$SCRIPT_DIR/whisper_env/bin/activate"

# Change to the script directory
cd "$SCRIPT_DIR"

# Run the integrated GUI
python3 dictation_integrated_gui.py

# Deactivate virtual environment when done
deactivate
