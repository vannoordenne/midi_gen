# MIDI Generator for Ableton Live

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)

A Python application that generates techno MIDI patterns and sends them in real-time to Ableton Live via virtual MIDI. This project serves as a proof of concept for real-time MIDI communication between Python and Ableton Live.

## Features

- Real-time MIDI pattern generation
- Direct communication with Ableton Live
- Multiple instrument channels (Drums, Bass, Melody)
- Interactive jam session mode
- Configurable patterns and parameters

## Project Structure

```
├── midi_generator.py     # Basic MIDI pattern generator
├── jam_session.py        # Interactive jam session
├── setup.py             # Installation helper
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the basic generator:
```bash
python midi_generator.py
```

Or try the interactive jam session:
```bash
python jam_session.py
```

## Ableton Live Setup

1. Open Ableton Live
2. Go to Preferences > Link/Tempo/MIDI
3. Enable the "Python to Ableton" MIDI port
4. Create 3 MIDI tracks:
   - Track 1: Drums (MIDI Channel 10)
   - Track 2: Bass (MIDI Channel 2)
   - Track 3: Melody (MIDI Channel 3)

## Development

This project is designed to be easily extended. You can:
- Add new pattern generators
- Modify MIDI channel mappings
- Create custom rhythm patterns
- Implement new musical scales

## Requirements

- Python 3.7 or higher
- Ableton Live
- macOS (for native MIDI support)

## Dependencies

- mido
- python-rtmidi


## Features

- **Automatic techno pattern generation**: Drums (4-on-the-floor), Bass (acid-style), Melody
- **Real-time MIDI output**: Direct to Ableton Live via virtual MIDI port
- **16-bar loops**: Optimal length for techno tracks
- **3 MIDI channels**: Drums (ch 10), Bass (ch 2), Melody (ch 3)
- **Pattern variations**: Each loop includes subtle variations

## Installation

### 1. Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. macOS MIDI Setup

On macOS, no additional drivers are required - the system supports virtual MIDI natively via Core MIDI.

## Usage

### 1. Start the Python Script

```bash
python midi_generator.py
```

The script will:
- Create a virtual MIDI port named "Python to Ableton"
- Generate techno patterns for drums, bass and melody
- Play the patterns in a continuous loop

### 2. Configure Ableton Live

1. **Open Ableton Live**
2. **Go to Preferences** (Cmd+, or Ableton Live > Preferences)
3. **Select "Link/Tempo/MIDI"**
4. **In the "MIDI" section:**
   - Find "Python to Ableton" in the Input list
   - Enable "Track" and "Remote" for this port

### 3. Setup MIDI Tracks in Ableton

Create 3 MIDI tracks:

#### Track 1: Drums
- **MIDI Input**: "Python to Ableton", Channel 10
- **Instrument**: Drum Rack or other drum sampler
- **Mapping**: Ensure kick (C1/note 36), snare (D1/note 38), hihat (F#1/note 42) are correctly mapped

#### Track 2: Bass  
- **MIDI Input**: "Python to Ableton", Channel 2
- **Instrument**: Bass synthesizer (e.g. Operator, Wavetable)
- **Range**: Low notes (C1-C3)

#### Track 3: Melody
- **MIDI Input**: "Python to Ableton", Channel 3  
- **Instrument**: Lead synthesizer
- **Range**: Mid register (C3-C5)

### 4. Start Recording/Monitoring

- **Arm** the tracks for recording or enable **monitoring**
- The script will automatically start sending MIDI data
- You will hear the patterns in real-time through your instruments

## MIDI Channel Mapping

| Instrument | MIDI Channel | Notes |
|------------|-------------|--------|
| Drums | 10 | General MIDI drum mapping |
| Bass | 2 | Low range (C1-C3) |
| Melody | 3 | Mid range (C3-C5) |

## Drum Note Mapping

| Sound | MIDI Note | Note Name |
|-------|-----------|-----------|
| Kick | 36 | C1 |
| Snare | 38 | D1 |
| Closed Hi-hat | 42 | F#1 |
| Open Hi-hat | 46 | A#1 |
| Crash | 49 | C#2 |
| Ride | 51 | D#2 |

## Configuration

### Changing Tempo
In `midi_generator.py`, modify this line:
```python
self.tempo_bpm = 128  # Change to desired BPM
```

### Adding New Patterns
Add methods to the `TechnoPatternGenerator` class:
```python
def generate_custom_pattern(self) -> MidiPattern:
    # Your custom pattern logic here
    pass
```

### Changing MIDI Port Name
```python
sender = MidiSender("Your Port Name")
```

## Advanced Tips

### Synchronization with Ableton
- Set Ableton's tempo to the same BPM as the script (128 BPM)
- Use Ableton's metronome to verify synchronization

### Recording
- Record the MIDI input as clips in Ableton
- Edit the recorded clips for perfect loops
- Use Ableton's quantization for timing corrections

### Live Performance
- Start/stop the script during live sets
- Use different versions of the script for track variations
- Combine with Ableton's built-in MIDI effects

## Troubleshooting

### "Cannot create MIDI port"
- Restart the script
- Check if other MIDI applications are blocking the ports
- Restart Ableton Live

### "No sound in Ableton"
- Verify that MIDI tracks are "armed" or "monitored"
- Check MIDI channel settings
- Ensure instruments are properly loaded

### Timing issues
- Ensure Ableton and the script are set to the same BPM
- Check your system's audio latency settings
- Close other audio applications