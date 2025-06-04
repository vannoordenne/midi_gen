#!/usr/bin/env python3
"""
Setup script for MIDI Generator system
"""

import subprocess
import sys
import os

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 7):
        print("Python 3.7 or higher is required")
        sys.exit(1)
    print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} found")

def install_dependencies():
    """Install required packages"""
    print("\nInstalling dependencies...")
    
    packages = ["mido", "python-rtmidi"]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"Error installing {package}")
            return False
    
    return True

def test_midi_setup():
    """Test MIDI functionality"""
    print("\nTesting MIDI setup...")
    
    try:
        import mido
        # Test virtual port
        test_port = mido.open_output("Test Port", virtual=True)
        test_port.close()
        print("Virtual MIDI ports working correctly")
        return True
    except Exception as e:
        print(f"MIDI test failed: {e}")
        return False

def create_launch_script():
    """Create an easy launch script"""
    script_content = '''#!/bin/bash
echo "Starting MIDI Generator..."
cd "$(dirname "$0")"
python3 midi_generator.py
'''
    
    with open("start_midi.sh", "w") as f:
        f.write(script_content)
    
    # Make executable
    os.chmod("start_midi.sh", 0o755)
    print("Launch script 'start_midi.sh' created")

def show_usage_instructions():
    """Display usage instructions"""
    print("""
Setup completed! 

NEXT STEPS:

1. Open Ableton Live
2. Go to Preferences > Link/Tempo/MIDI
3. Enable 'Python to Ableton' as MIDI Input
4. Create 3 MIDI tracks:
   - Track 1: Drums (MIDI Channel 10) 
   - Track 2: Bass (MIDI Channel 2)
   - Track 3: Melody (MIDI Channel 3)
5. Load your favorite instruments on these tracks
6. Set the tracks to 'Arm' or 'Monitor'

STARTING THE APPLICATION:

Option 1: Direct start
python3 midi_generator.py

Option 2: Using launch script  
./start_midi.sh

""")

def main():
    print("MIDI Generator Setup")
    print("=" * 40)
    
    # Check Python
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        print("Setup failed during dependency installation")
        sys.exit(1)
    
    # Test MIDI
    if not test_midi_setup():
        print("Setup failed during MIDI test")
        sys.exit(1)
    
    # Create launch script
    create_launch_script()
    
    # Show instructions
    show_usage_instructions()

if __name__ == "__main__":
    main() 