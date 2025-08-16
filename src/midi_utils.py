#!/usr/bin/env python3
"""
MIDI Utilities for DNA Ambient Composition
Helper functions for MIDI file creation and manipulation
"""

import os
from typing import List, Dict, Optional
from midiutil import MIDIFile


class MIDIExporter:
    """Utilities for exporting and managing MIDI files"""
    
    @staticmethod
    def create_midi_file(track_count: int, tempo: int = 60) -> MIDIFile:
        """Create a new MIDI file with specified tracks and tempo"""
        midi = MIDIFile(track_count)
        midi.addTempo(0, 0, tempo)
        return midi
    
    @staticmethod
    def add_track_info(midi: MIDIFile, track: int, program: int, 
                       track_name: str = None, channel: int = None):
        """Add program change and track name to a MIDI track"""
        if channel is None:
            channel = track
            
        midi.addProgramChange(track, channel, 0, program)
        
        if track_name:
            midi.addTrackName(track, 0, track_name)
    
    @staticmethod
    def add_controller_automation(midi: MIDIFile, track: int, channel: int,
                                  controller: int, values: List[int], 
                                  times: List[float]):
        """Add controller automation to a track"""
        for time, value in zip(times, values):
            midi.addControllerEvent(track, channel, time, controller, value)
    
    @staticmethod
    def save_midi_file(midi: MIDIFile, filename: str):
        """Save MIDI file to disk"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'wb') as f:
            midi.writeFile(f)
    
    @staticmethod
    def get_instrument_map() -> Dict[str, int]:
        """Get mapping of instrument names to MIDI program numbers"""
        return {
            # Ambient-friendly instruments
            'synth_bass': 38,
            'warm_pad': 92,
            'poly_synth': 95,
            'synth_lead': 89,
            'rain_fx': 97,
            'synth_voice': 55,
            
            # Traditional instruments
            'piano': 0,
            'electric_piano': 4,
            'harpsichord': 6,
            'celesta': 8,
            'vibraphone': 11,
            'marimba': 12,
            'xylophone': 13,
            'tubular_bells': 14,
            'dulcimer': 15,
            'organ': 19,
            'accordion': 21,
            'harmonica': 22,
            'guitar': 24,
            'electric_guitar': 27,
            'bass': 32,
            'violin': 40,
            'viola': 41,
            'cello': 42,
            'harp': 46,
            'strings': 48,
            'voice': 52,
            'choir': 53,
            'trumpet': 56,
            'french_horn': 60,
            'saxophone': 66,
            'oboe': 68,
            'clarinet': 71,
            'flute': 73,
            'whistle': 78,
            'synth_pad': 90,
            'crystal': 98,
            'atmosphere': 99,
            'brightness': 100,
            'goblins': 101,
            'echoes': 102,
            'sci_fi': 103
        }
    
    @staticmethod
    def midi_note_to_frequency(midi_note: int) -> float:
        """Convert MIDI note number to frequency in Hz"""
        return 440 * (2 ** ((midi_note - 69) / 12))
    
    @staticmethod
    def frequency_to_midi_note(frequency: float) -> int:
        """Convert frequency in Hz to nearest MIDI note number"""
        import math
        return int(round(69 + 12 * math.log2(frequency / 440)))
    
    @staticmethod
    def validate_midi_parameters(note: int, velocity: int, channel: int) -> bool:
        """Validate MIDI parameters are in correct ranges"""
        return (0 <= note <= 127 and 
                0 <= velocity <= 127 and 
                0 <= channel <= 15)
    
    @staticmethod
    def create_chord(root_note: int, chord_type: str = 'major') -> List[int]:
        """Create a chord from root note and chord type"""
        chord_intervals = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            'diminished': [0, 3, 6],
            'augmented': [0, 4, 8],
            'sus2': [0, 2, 7],
            'sus4': [0, 5, 7],
            'major7': [0, 4, 7, 11],
            'minor7': [0, 3, 7, 10],
            'dominant7': [0, 4, 7, 10],
            'minor7b5': [0, 3, 6, 10]
        }
        
        intervals = chord_intervals.get(chord_type, chord_intervals['major'])
        return [root_note + interval for interval in intervals]
    
    @staticmethod
    def add_reverb_send(midi: MIDIFile, track: int, channel: int, 
                        amount: int = 80, time: float = 0):
        """Add reverb send (CC91) to a track"""
        midi.addControllerEvent(track, channel, time, 91, amount)
    
    @staticmethod
    def add_chorus_send(midi: MIDIFile, track: int, channel: int,
                        amount: int = 40, time: float = 0):
        """Add chorus send (CC93) to a track"""
        midi.addControllerEvent(track, channel, time, 93, amount)
    
    @staticmethod
    def add_pan(midi: MIDIFile, track: int, channel: int,
                pan: int = 64, time: float = 0):
        """Add pan position (CC10) to a track"""
        midi.addControllerEvent(track, channel, time, 10, pan)
    
    @staticmethod
    def add_expression(midi: MIDIFile, track: int, channel: int,
                       expression: int = 127, time: float = 0):
        """Add expression (CC11) to a track"""
        midi.addControllerEvent(track, channel, time, 11, expression)


class MIDITrackBuilder:
    """Helper class for building individual MIDI tracks"""
    
    def __init__(self, midi: MIDIFile, track_number: int, channel: int = None):
        self.midi = midi
        self.track = track_number
        self.channel = channel if channel is not None else track_number
        self.current_time = 0.0
    
    def set_instrument(self, program: int, track_name: str = None):
        """Set the instrument for this track"""
        MIDIExporter.add_track_info(self.midi, self.track, program, track_name, self.channel)
        return self
    
    def add_note(self, note: int, duration: float, velocity: int = 100, time: float = None):
        """Add a note to the track"""
        if time is None:
            time = self.current_time
        
        if MIDIExporter.validate_midi_parameters(note, velocity, self.channel):
            self.midi.addNote(self.track, self.channel, note, time, duration, velocity)
        
        return self
    
    def add_chord(self, notes: List[int], duration: float, velocity: int = 100, time: float = None):
        """Add a chord (multiple notes) to the track"""
        if time is None:
            time = self.current_time
            
        for note in notes:
            self.add_note(note, duration, velocity, time)
        
        return self
    
    def advance_time(self, beats: float):
        """Advance the current time position"""
        self.current_time += beats
        return self
    
    def set_time(self, time: float):
        """Set the current time position"""
        self.current_time = time
        return self
    
    def add_controller(self, controller: int, value: int, time: float = None):
        """Add a controller event"""
        if time is None:
            time = self.current_time
            
        self.midi.addControllerEvent(self.track, self.channel, time, controller, value)
        return self
    
    def add_reverb(self, amount: int = 80):
        """Add reverb to the track"""
        return self.add_controller(91, amount, 0)
    
    def add_pan(self, position: int = 64):
        """Add pan position to the track"""
        return self.add_controller(10, position, 0)


if __name__ == "__main__":
    # Example usage
    midi = MIDIExporter.create_midi_file(2, 60)
    
    # Track 0: Bass
    bass_track = MIDITrackBuilder(midi, 0)
    bass_track.set_instrument(38, "Bass Foundation")
    bass_track.add_reverb(60)
    bass_track.add_note(36, 4.0, 80)
    
    # Track 1: Pad
    pad_track = MIDITrackBuilder(midi, 1)
    pad_track.set_instrument(92, "Harmonic Pad")
    pad_track.add_reverb(100)
    chord_notes = MIDIExporter.create_chord(60, 'minor')
    pad_track.add_chord(chord_notes, 4.0, 70)
    
    # Save example
    MIDIExporter.save_midi_file(midi, "example_output.mid")
    print("Created example MIDI file: example_output.mid")