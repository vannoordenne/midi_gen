#!/usr/bin/env python3
"""
Interactive MIDI Jam Session for Ableton Live
"""

import mido
import time
import random
import threading
import sys

class InteractiveJamSession:
    
    def __init__(self):
        # MIDI setup
        self.output_port = None
        self.is_playing = False
        self.jam_thread = None
        
        # Jam parameters
        self.bpm = 128
        self.beat_duration = 60.0 / self.bpm
        
        # Pattern controls
        self.drums_enabled = True
        self.bass_enabled = True
        self.melody_enabled = True
        
        # Intensity controls (0.0 - 1.0)
        self.drum_intensity = 1.0
        self.bass_intensity = 0.8
        self.melody_intensity = 0.3
        
        # Musical parameters
        self.key_root = 0  # 0=C, 1=C#, 2=D, etc.
        self.scale_type = 0  # 0=major, 1=minor, 2=pentatonic
        
        # Scales
        self.scales = {
            0: [0, 2, 4, 5, 7, 9, 11],  # Major
            1: [0, 2, 3, 5, 7, 8, 10],  # Minor  
            2: [0, 2, 4, 7, 9],         # Pentatonic
            3: [0, 2, 3, 6, 7, 8, 11]   # Blues
        }
        
        # Pattern variations
        self.drum_pattern = 0  # 0=basic, 1=breaks
        self.bass_pattern = 0  # 0=basic, 1=acid
        
        # Performance state
        self.loop_count = 0
        
    def setup_midi(self):
        """Setup MIDI connection"""
        available_ports = mido.get_output_names()
        
        for port in available_ports:
            if "Python" in port:
                self.output_port = mido.open_output(port)
                print(f"Connected to: {port}")
                return True
        
        print("No Python MIDI port found")
        return False
    
    def get_current_scale(self):
        """Get current scale notes"""
        base_notes = self.scales[self.scale_type]
        root = 60 + self.key_root  # C4 + offset
        return [root + note for note in base_notes]
    
    def play_kick(self, velocity=None):
        """Play kick drum"""
        if not self.drums_enabled or not self.output_port:
            return
        vel = velocity or int(100 + (27 * self.drum_intensity))
        kick_on = mido.Message('note_on', channel=9, note=36, velocity=vel)
        self.output_port.send(kick_on)
        
        threading.Timer(0.1, lambda: self.output_port.send(
            mido.Message('note_off', channel=9, note=36, velocity=0)
        )).start()
    
    def play_snare(self, velocity=None):
        """Play snare"""
        if not self.drums_enabled or not self.output_port:
            return
        vel = velocity or int(90 + (30 * self.drum_intensity))
        snare_on = mido.Message('note_on', channel=9, note=38, velocity=vel)
        self.output_port.send(snare_on)
        
        threading.Timer(0.1, lambda: self.output_port.send(
            mido.Message('note_off', channel=9, note=38, velocity=0)
        )).start()
    
    def play_hihat(self, velocity=None):
        """Play hi-hat"""
        if not self.drums_enabled or not self.output_port:
            return
        vel = velocity or int(60 + (30 * self.drum_intensity))
        hihat_on = mido.Message('note_on', channel=9, note=42, velocity=vel)
        self.output_port.send(hihat_on)
        
        threading.Timer(0.05, lambda: self.output_port.send(
            mido.Message('note_off', channel=9, note=42, velocity=0)
        )).start()
    
    def play_bass_note(self, note, duration=0.7):
        """Play bass note"""
        if not self.bass_enabled or not self.output_port:
            return
        vel = int(80 + (30 * self.bass_intensity))
        bass_on = mido.Message('note_on', channel=1, note=note, velocity=vel)
        self.output_port.send(bass_on)
        
        threading.Timer(duration, lambda: self.output_port.send(
            mido.Message('note_off', channel=1, note=note, velocity=0)
        )).start()
    
    def play_melody_note(self, note, duration=1.5):
        """Play melody note"""
        if not self.melody_enabled or not self.output_port:
            return
        vel = int(70 + (30 * self.melody_intensity))
        melody_on = mido.Message('note_on', channel=2, note=note, velocity=vel)
        self.output_port.send(melody_on)
        
        threading.Timer(duration, lambda: self.output_port.send(
            mido.Message('note_off', channel=2, note=note, velocity=0)
        )).start()
    
    def drum_pattern_basic(self, beat):
        """Basic 4-on-the-floor"""
        self.play_kick()
        if beat % 2 == 1:
            self.play_snare()
    
    def drum_pattern_breaks(self, beat):
        """Breakbeat style"""
        if beat == 0:
            self.play_kick()
        elif beat == 1:
            self.play_snare()
        elif beat == 2:
            if random.random() > 0.3:
                self.play_kick()
        elif beat == 3:
            self.play_snare()
            if random.random() > 0.7:
                self.play_kick()
    
    def bass_pattern_basic(self, beat, bar):
        """Basic bassline"""
        if beat in [0, 2] and random.random() < self.bass_intensity:
            scale = self.get_current_scale()
            note = scale[bar % len(scale)] - 24
            self.play_bass_note(note)
    
    def bass_pattern_acid(self, beat, bar):
        """Acid bassline"""
        if beat % 1 == 0 and random.random() < self.bass_intensity:
            scale = self.get_current_scale()
            note = scale[random.randint(0, len(scale)-1)] - 24
            if random.random() > 0.7:
                note += 3
            self.play_bass_note(note, 0.3)
    
    def melody_pattern_sparse(self, beat, bar):
        """Sparse melody"""
        if beat == 0 and bar % 4 == 0 and random.random() < self.melody_intensity:
            scale = self.get_current_scale()
            note = random.choice(scale)
            self.play_melody_note(note)
    
    def jam_loop(self):
        """Main jam loop"""
        print(f"JAM STARTED at {self.bpm} BPM")
        print("   (Return to menu for controls)")
        
        self.is_playing = True
        
        while self.is_playing:
            self.loop_count += 1
            
            # 16 bars per loop
            for bar in range(16):
                if not self.is_playing:
                    break
                
                # 4 beats per bar
                for beat in range(4):
                    if not self.is_playing:
                        break
                    
                    beat_start = time.time()
                    
                    # DRUMS
                    if self.drum_pattern == 0:
                        self.drum_pattern_basic(beat)
                    else:
                        self.drum_pattern_breaks(beat)
                    
                    # BASS
                    if self.bass_pattern == 0:
                        self.bass_pattern_basic(beat, bar)
                    else:
                        self.bass_pattern_acid(beat, bar)
                    
                    # MELODY
                    self.melody_pattern_sparse(beat, bar)
                    
                    # Hi-hat on off-beats
                    self.play_hihat()
                    
                    # Wait for next beat
                    elapsed = time.time() - beat_start
                    remaining = self.beat_duration - elapsed
                    if remaining > 0:
                        time.sleep(remaining)
    
    def start_jam(self):
        """Start jam session in background thread"""
        if not self.is_playing:
            self.jam_thread = threading.Thread(target=self.jam_loop)
            self.jam_thread.daemon = True
            self.jam_thread.start()
            print("Jam session started")
    
    def stop_jam(self):
        """Stop jam session"""
        if self.is_playing:
            self.is_playing = False
            print("Jam session stopped")
    
    def get_status(self):
        """Get current status"""
        status = f"STATUS:\n"
        status += f"  Playing: {'Yes' if self.is_playing else 'No'}\n"
        status += f"  BPM: {self.bpm}\n"
        status += f"  Loop: {self.loop_count}\n"
        status += f"\nINSTRUMENTS:\n"
        status += f"  Drums: {'ON' if self.drums_enabled else 'OFF'} (intensity: {self.drum_intensity:.1f})\n"
        status += f"  Bass: {'ON' if self.bass_enabled else 'OFF'} (intensity: {self.bass_intensity:.1f})\n"
        status += f"  Melody: {'ON' if self.melody_enabled else 'OFF'} (intensity: {self.melody_intensity:.1f})\n"
        
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        scales = ['Major', 'Minor', 'Pentatonic', 'Blues']
        status += f"\nMUSICAL:\n"
        status += f"  Key: {keys[self.key_root]}\n"
        status += f"  Scale: {scales[self.scale_type]}\n"
        
        return status
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("INTERACTIVE JAM SESSION - MAIN MENU")
        print("="*50)
        print("PLAYBACK:")
        print("  [1] Start Jam")
        print("  [2] Stop Jam")
        print("  [3] Show Status")
        print("  [4] Change BPM")
        print("\nINSTRUMENTS:")
        print("  [5] Toggle Drums")
        print("  [6] Toggle Bass")
        print("  [7] Toggle Melody")
        print("  [8] Adjust Intensities")
        print("\nMUSICAL:")
        print("  [9] Change Key")
        print("  [10] Change Scale")
        print("  [11] Change Patterns")
        print("\nOTHER:")
        print("  [0] Exit")
        print("="*50)

def main():
    """Main application"""
    print("Interactive MIDI Jam Session for Ableton Live")
    print("Professional Version")
    print("="*50)
    
    session = InteractiveJamSession()
    
    # Setup MIDI
    if not session.setup_midi():
        print("Failed to connect to MIDI. Please ensure a Python MIDI port exists.")
        return
    
    # Main menu loop
    while True:
        session.show_menu()
        
        try:
            choice = input("\nEnter choice: ").strip()
            
            if choice == "0":
                session.stop_jam()
                print("Goodbye!")
                break
                
            elif choice == "1":
                session.start_jam()
                
            elif choice == "2":
                session.stop_jam()
                
            elif choice == "3":
                print(session.get_status())
                
            elif choice == "4":
                try:
                    new_bpm = int(input("Enter new BPM (60-200): "))
                    if 60 <= new_bpm <= 200:
                        session.bpm = new_bpm
                        session.beat_duration = 60.0 / new_bpm
                        print(f"BPM set to {new_bpm}")
                    else:
                        print("BPM must be between 60 and 200")
                except ValueError:
                    print("Invalid BPM value")
                    
            elif choice == "5":
                session.drums_enabled = not session.drums_enabled
                print(f"Drums: {'ON' if session.drums_enabled else 'OFF'}")
                
            elif choice == "6":
                session.bass_enabled = not session.bass_enabled
                print(f"Bass: {'ON' if session.bass_enabled else 'OFF'}")
                
            elif choice == "7":
                session.melody_enabled = not session.melody_enabled
                print(f"Melody: {'ON' if session.melody_enabled else 'OFF'}")
                
            elif choice == "8":
                print("\nADJUST INTENSITIES (0.0 - 1.0):")
                try:
                    drum_int = float(input(f"Drum intensity ({session.drum_intensity}): ") or session.drum_intensity)
                    bass_int = float(input(f"Bass intensity ({session.bass_intensity}): ") or session.bass_intensity)
                    melody_int = float(input(f"Melody intensity ({session.melody_intensity}): ") or session.melody_intensity)
                    
                    session.drum_intensity = max(0.0, min(1.0, drum_int))
                    session.bass_intensity = max(0.0, min(1.0, bass_int))
                    session.melody_intensity = max(0.0, min(1.0, melody_int))
                    
                    print("Intensities updated")
                except ValueError:
                    print("Invalid intensity values")
                    
            elif choice == "9":
                keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
                print("\nSELECT KEY:")
                for i, key in enumerate(keys):
                    print(f"  [{i}] {key}")
                try:
                    key_choice = int(input("Enter key number: "))
                    if 0 <= key_choice < len(keys):
                        session.key_root = key_choice
                        print(f"Key set to {keys[key_choice]}")
                    else:
                        print("Invalid key choice")
                except ValueError:
                    print("Invalid key choice")
                    
            elif choice == "10":
                scales = ['Major', 'Minor', 'Pentatonic', 'Blues']
                print("\nSELECT SCALE:")
                for i, scale in enumerate(scales):
                    print(f"  [{i}] {scale}")
                try:
                    scale_choice = int(input("Enter scale number: "))
                    if 0 <= scale_choice < len(scales):
                        session.scale_type = scale_choice
                        print(f"Scale set to {scales[scale_choice]}")
                    else:
                        print("Invalid scale choice")
                except ValueError:
                    print("Invalid scale choice")
                    
            elif choice == "11":
                print("\nCHANGE PATTERNS:")
                print("Drum patterns: [0] Basic 4/4, [1] Breakbeat")
                print("Bass patterns: [0] Basic, [1] Acid")
                try:
                    drum_pat = int(input(f"Drum pattern ({session.drum_pattern}): ") or session.drum_pattern)
                    bass_pat = int(input(f"Bass pattern ({session.bass_pattern}): ") or session.bass_pattern)
                    
                    if drum_pat in [0, 1]:
                        session.drum_pattern = drum_pat
                    if bass_pat in [0, 1]:
                        session.bass_pattern = bass_pat
                    
                    print("Patterns updated")
                except ValueError:
                    print("Invalid pattern choice")
                    
            else:
                print("Invalid choice")
                
        except KeyboardInterrupt:
            session.stop_jam()
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main() 