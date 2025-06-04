#!/usr/bin/env python3
"""
MIDI Pattern Generator for Ableton Live
"""

import mido
import time
import random

class MidiPatternGenerator:
    """MIDI pattern generator with proper note-off handling"""
    
    def __init__(self, bpm=128):
        self.bpm = bpm
        self.beat_duration = 60.0 / bpm
        self.output_port = None
        self.is_playing = False
        
    def setup_midi_port(self, port_name=None):
        """Setup virtual MIDI port - use existing port if available"""
        try:
            # Search for existing Python port first
            available_ports = mido.get_output_names()
            existing_port = None
            
            for port in available_ports:
                if "Python" in port:
                    existing_port = port
                    break
            
            if existing_port:
                # Use existing port
                self.output_port = mido.open_output(existing_port)
                print(f"Connected to existing MIDI port: '{existing_port}'")
            else:
                # Create new port if none exists
                new_port_name = port_name or "Python to Ableton"
                self.output_port = mido.open_output(new_port_name, virtual=True)
                print(f"Created new virtual MIDI port: '{new_port_name}'")
            
            print("\nSetup instructions for Ableton Live:")
            print("1. If you see a new port, go to Preferences > Link/Tempo/MIDI")
            print("2. Enable the Python port as MIDI Input")
            print("3. Ensure you have 3 MIDI tracks:")
            print("   - Track 1: Drums (MIDI Channel 10)")
            print("   - Track 2: Bass (MIDI Channel 2)")  
            print("   - Track 3: Melody (MIDI Channel 3)")
            print("4. Set tracks to 'Arm' or 'Monitor'")
            return True
        except Exception as e:
            print(f"Error creating MIDI port: {e}")
            return False
    
    def play_techno_loop(self):
        """Play a techno loop with proper note-off handling"""
        print(f"\nStarting techno loop at {self.bpm} BPM")
        print("Press Ctrl+C to stop\n")
        
        self.is_playing = True
        loop_count = 0
        
        # Track which notes are active for note-off
        active_bass_notes = []
        active_melody_notes = []
        
        try:
            while self.is_playing:
                loop_count += 1
                print(f"\nLoop {loop_count} started (16 bars)")
                
                # Play 16 bars
                for bar in range(16):
                    if not self.is_playing:
                        break
                        
                    print(f"Bar {bar + 1}/16")
                    
                    # 4 beats per bar
                    for beat in range(4):
                        if not self.is_playing:
                            break
                            
                        beat_start = time.time()
                        print(f"  Beat {beat + 1}")
                        
                        # DRUMS: Kick on every beat (Channel 10)
                        kick_velocity = random.randint(100, 127)
                        kick_on = mido.Message('note_on', channel=9, note=36, velocity=kick_velocity)
                        self.output_port.send(kick_on)
                        print(f"    Kick: velocity {kick_velocity}")
                        
                        # DRUMS: Snare on beat 2 and 4 (Channel 10)
                        if beat in [1, 3]:
                            snare_velocity = random.randint(90, 120)
                            snare_on = mido.Message('note_on', channel=9, note=38, velocity=snare_velocity)
                            self.output_port.send(snare_on)
                            print(f"    Snare: velocity {snare_velocity}")
                        
                        # BASS: On beat 1 and 3 (Channel 2)
                        if beat in [0, 2] and random.random() > 0.2:  # 80% chance
                            bass_notes = [36, 38, 41, 43]
                            bass_note = bass_notes[bar // 4 % len(bass_notes)]
                            bass_velocity = random.randint(80, 110)
                            bass_on = mido.Message('note_on', channel=1, note=bass_note, velocity=bass_velocity)
                            self.output_port.send(bass_on)
                            active_bass_notes.append((bass_note, beat_start + 0.7))  # Note off after 0.7 sec
                            print(f"    Bass: note {bass_note}, velocity {bass_velocity}")
                        
                        # MELODY: Sparse (Channel 3)
                        if bar % 4 == 0 and beat == 0 and random.random() > 0.4:  # 60% chance
                            melody_notes = [60, 62, 65, 67, 69, 72]
                            melody_note = random.choice(melody_notes)
                            melody_velocity = random.randint(70, 100)
                            melody_on = mido.Message('note_on', channel=2, note=melody_note, velocity=melody_velocity)
                            self.output_port.send(melody_on)
                            active_melody_notes.append((melody_note, beat_start + 1.5))  # Note off after 1.5 sec
                            print(f"    Melody: note {melody_note}, velocity {melody_velocity}")
                        
                        # Wait half beat for hi-hat
                        time.sleep(self.beat_duration / 2)
                        
                        # DRUMS: Hi-hat on off-beats (Channel 10)
                        hihat_velocity = random.randint(60, 90)
                        hihat_on = mido.Message('note_on', channel=9, note=42, velocity=hihat_velocity)
                        self.output_port.send(hihat_on)
                        
                        # Short delay for note offs
                        time.sleep(0.05)
                        
                        # DRUM NOTE-OFFS (short after note-on)
                        kick_off = mido.Message('note_off', channel=9, note=36, velocity=0)
                        self.output_port.send(kick_off)
                        hihat_off = mido.Message('note_off', channel=9, note=42, velocity=0)
                        self.output_port.send(hihat_off)
                        
                        if beat in [1, 3]:
                            snare_off = mido.Message('note_off', channel=9, note=38, velocity=0)
                            self.output_port.send(snare_off)
                        
                        # Check for BASS and MELODY note-offs
                        current_time = time.time()
                        
                        # Bass note-offs
                        new_active_bass = []
                        for note, off_time in active_bass_notes:
                            if current_time >= off_time:
                                bass_off = mido.Message('note_off', channel=1, note=note, velocity=0)
                                self.output_port.send(bass_off)
                                print(f"    Bass OFF: note {note}")
                            else:
                                new_active_bass.append((note, off_time))
                        active_bass_notes = new_active_bass
                        
                        # Melody note-offs
                        new_active_melody = []
                        for note, off_time in active_melody_notes:
                            if current_time >= off_time:
                                melody_off = mido.Message('note_off', channel=2, note=note, velocity=0)
                                self.output_port.send(melody_off)
                                print(f"    Melody OFF: note {note}")
                            else:
                                new_active_melody.append((note, off_time))
                        active_melody_notes = new_active_melody
                        
                        # Wait for rest of beat
                        elapsed = time.time() - beat_start
                        remaining = self.beat_duration - elapsed
                        if remaining > 0:
                            time.sleep(remaining)
                
                print(f"Loop {loop_count} completed")
                
        except KeyboardInterrupt:
            print("\nStopping...")
            self.is_playing = False
        
        # Clean shutdown - stop all active notes
        print("Stopping all active notes...")
        for note, _ in active_bass_notes:
            bass_off = mido.Message('note_off', channel=1, note=note, velocity=0)
            self.output_port.send(bass_off)
        
        for note, _ in active_melody_notes:
            melody_off = mido.Message('note_off', channel=2, note=note, velocity=0)
            self.output_port.send(melody_off)
        
        if self.output_port:
            self.output_port.close()
            print("MIDI port closed")

def main():
    """Main function"""
    print("MIDI Pattern Generator for Ableton Live")
    print("=" * 50)
    
    # Create generator
    generator = MidiPatternGenerator(bpm=128)
    
    # Setup MIDI
    if not generator.setup_midi_port():
        print("Failed to setup MIDI port. Exiting.")
        return
    
    # Start the jam
    try:
        generator.play_techno_loop()
    except Exception as e:
        print(f"Error during playback: {e}")
    finally:
        print("Session ended")

if __name__ == "__main__":
    main() 