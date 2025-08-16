#!/usr/bin/env python3
"""
Ambient DNA Composer - Music Theory-Based Sonification
Creates structured ambient soundscapes from DNA sequences using compositional techniques
"""

import os
import math
import random
import argparse
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
from Bio import SeqIO

from .sequence_analyzer import SequenceAnalyzer
from .midi_utils import MIDIExporter, MIDITrackBuilder
from midiutil import MIDIFile


@dataclass
class AmbientConfig:
    """Configuration for ambient DNA composition"""
    tempo: int = 60  # Slow ambient tempo
    key_signature: str = 'C'  # Base key
    mode: str = 'dorian'  # Modal harmony
    track_count: int = 6  # Number of simultaneous tracks
    composition_length: int = 600  # 10 minutes in seconds
    reverb_send: int = 80  # Ambient reverb level
    attack_time: float = 2.0  # Slow attack for pads
    release_time: float = 4.0  # Long release


class MusicalScales:
    """Music theory scales and modes for ambient composition"""
    
    # Interval patterns (semitones from root)
    MODES = {
        'ionian': [0, 2, 4, 5, 7, 9, 11],      # Major - bright
        'dorian': [0, 2, 3, 5, 7, 9, 10],     # Minor with raised 6th - ethereal
        'phrygian': [0, 1, 3, 5, 7, 8, 10],   # Dark, mysterious
        'lydian': [0, 2, 4, 6, 7, 9, 11],     # Dreamy, floating
        'mixolydian': [0, 2, 4, 5, 7, 9, 10], # Bluesy, grounded
        'aeolian': [0, 2, 3, 5, 7, 8, 10],    # Natural minor - melancholic
        'locrian': [0, 1, 3, 5, 6, 8, 10]     # Unstable, otherworldly
    }
    
    # Pentatonic scales for melodic content
    PENTATONIC = {
        'major': [0, 2, 4, 7, 9],
        'minor': [0, 3, 5, 7, 10],
        'suspended': [0, 2, 5, 7, 10]
    }
    
    # Key signatures (semitones from C)
    KEYS = {
        'C': 0, 'G': 7, 'D': 2, 'A': 9, 'E': 4, 'B': 11, 'F#': 6,
        'F': 5, 'Bb': 10, 'Eb': 3, 'Ab': 8, 'Db': 1, 'Gb': 6
    }


class AmbientVoicing:
    """Voice leading and harmonic progression for ambient music"""
    
    @staticmethod
    def create_chord_progression(scale_notes: List[int], length: int, mode: str = 'dorian') -> List[List[int]]:
        """Generate ambient chord progression using modal harmony"""
        # Common ambient progressions in modal contexts
        progressions = {
            'dorian': [1, 4, 1, 7],      # i - IV - i - VII
            'lydian': [1, 2, 4, 1],      # I - ii - IV - I
            'aeolian': [1, 6, 4, 7],     # i - VI - iv - VII
            'phrygian': [1, 2, 1, 7],    # i - bII - i - bVII
            'mixolydian': [1, 7, 4, 1],  # I - bVII - IV - I
            'ionian': [1, 6, 4, 5],      # I - vi - IV - V
            'locrian': [1, 2, 5, 1]      # i - bII - bV - i
        }
        
        chord_pattern = progressions.get(mode, progressions['dorian'])
        chords = []
        
        for i in range(length):
            degree = chord_pattern[i % len(chord_pattern)]
            root = scale_notes[(degree - 1) % len(scale_notes)]
            
            # Build triad (root, third, fifth)
            chord = [
                root,
                scale_notes[(degree + 1) % len(scale_notes)],
                scale_notes[(degree + 3) % len(scale_notes)]
            ]
            chords.append(chord)
            
        return chords
    
    @staticmethod
    def voice_lead_smoothly(prev_chord: List[int], next_chord: List[int]) -> List[int]:
        """Apply voice leading principles for smooth transitions"""
        if not prev_chord:
            return next_chord
            
        # Find the voicing with minimal movement
        voiced_chord = []
        for note in next_chord:
            # Find closest octave to previous chord
            closest_note = note
            min_distance = float('inf')
            
            for prev_note in prev_chord:
                for octave_offset in [-12, 0, 12]:
                    candidate = note + octave_offset
                    distance = abs(candidate - prev_note)
                    if distance < min_distance:
                        min_distance = distance
                        closest_note = candidate
            
            voiced_chord.append(closest_note)
        
        return voiced_chord


class DNAAmbientComposer:
    """Ambient music composer using DNA sequence analysis"""
    
    def __init__(self, ambient_config: AmbientConfig = None):
        self.ambient_config = ambient_config or AmbientConfig()
        self.scales = MusicalScales()
        self.voicing = AmbientVoicing()
        
        # Calculate scale notes in MIDI range
        self.base_key = self.scales.KEYS[self.ambient_config.key_signature]
        self.scale_intervals = self.scales.MODES[self.ambient_config.mode]
        self.scale_notes = self._calculate_scale_notes()
    
    def _calculate_scale_notes(self) -> List[int]:
        """Calculate MIDI notes for the selected scale across multiple octaves"""
        notes = []
        for octave in range(2, 7):  # Cover wide range for ambient
            for interval in self.scale_intervals:
                midi_note = (octave * 12) + self.base_key + interval
                if 24 <= midi_note <= 108:  # Keep in reasonable MIDI range
                    notes.append(midi_note)
        return sorted(notes)
    
    def create_ambient_soundscape(self, sequence: str, output_file: str = None) -> MIDIFile:
        """Create a complete ambient soundscape from DNA sequence"""
        # Analyze sequence for musical structure
        musical_analysis = SequenceAnalyzer.analyze_for_musical_structure(sequence)
        
        # Calculate composition parameters
        beats_per_minute = self.ambient_config.tempo
        beats_total = (self.ambient_config.composition_length * beats_per_minute) // 60
        measures = beats_total // 4  # 4/4 time signature
        
        # Create MIDI file with multiple tracks
        midi = MIDIExporter.create_midi_file(self.ambient_config.track_count, beats_per_minute)
        
        # Set up each track with different instruments and roles
        self._setup_tracks(midi, musical_analysis)
        
        # Generate harmonic foundation (bass and pad tracks)
        self._generate_harmonic_foundation(midi, sequence, musical_analysis, measures)
        
        # Generate melodic content (lead and arp tracks)
        self._generate_melodic_content(midi, sequence, musical_analysis, measures)
        
        # Generate atmospheric elements (texture tracks)
        self._generate_atmospheric_elements(midi, sequence, musical_analysis, measures)
        
        # Add expression and automation
        self._add_expression_automation(midi, musical_analysis, measures)
        
        # Save if output file specified
        if output_file:
            MIDIExporter.save_midi_file(midi, output_file)
        
        return midi
    
    def _setup_tracks(self, midi: MIDIFile, analysis: Dict):
        """Configure MIDI tracks with appropriate instruments"""
        instruments = MIDIExporter.get_instrument_map()
        
        # Track 0: Bass foundation
        MIDIExporter.add_track_info(midi, 0, instruments['synth_bass'], "Bass Foundation")
        MIDIExporter.add_reverb_send(midi, 0, 0, 60)
        
        # Track 1: Harmonic pad
        MIDIExporter.add_track_info(midi, 1, instruments['warm_pad'], "Harmonic Pad")
        MIDIExporter.add_reverb_send(midi, 1, 1, 100)
        
        # Track 2: Lead melody
        MIDIExporter.add_track_info(midi, 2, instruments['poly_synth'], "Lead Melody")
        MIDIExporter.add_reverb_send(midi, 2, 2, 80)
        
        # Track 3: Arpeggiation
        MIDIExporter.add_track_info(midi, 3, instruments['synth_lead'], "Arpeggiation")
        MIDIExporter.add_reverb_send(midi, 3, 3, 70)
        
        # Track 4: Atmospheric texture
        MIDIExporter.add_track_info(midi, 4, instruments['rain_fx'], "Atmospheric Texture")
        MIDIExporter.add_reverb_send(midi, 4, 4, 120)
        
        # Track 5: Rhythmic pulse (subtle)
        MIDIExporter.add_track_info(midi, 5, instruments['synth_voice'], "Rhythmic Pulse")
        MIDIExporter.add_reverb_send(midi, 5, 5, 90)
    
    def _generate_harmonic_foundation(self, midi: MIDIFile, sequence: str, 
                                    analysis: Dict, measures: int):
        """Generate bass and harmonic pad tracks"""
        harmonic_rhythm = analysis['harmonic_rhythm']
        
        # Generate chord progression
        chord_count = max(8, measures // 4)
        chord_progression = self.voicing.create_chord_progression(
            self.scale_notes[:7], chord_count, self.ambient_config.mode
        )
        
        current_time = 0
        prev_chord = None
        
        for measure in range(measures):
            chord_index = measure % len(chord_progression)
            current_chord = chord_progression[chord_index]
            
            # Apply voice leading
            if prev_chord:
                current_chord = self.voicing.voice_lead_smoothly(prev_chord, current_chord)
            
            # Bass line (Track 0) - root notes in low octave
            bass_note = current_chord[0] - 24  # Two octaves down
            bass_note = max(24, bass_note)  # Don't go below C1
            
            midi.addNote(0, 0, bass_note, current_time, 4.0, 70)
            
            # Harmonic pad (Track 1) - full chords
            for i, note in enumerate(current_chord):
                pad_note = note + 12  # One octave up for warmth
                velocity = 60 - (i * 5)  # Decreasing velocity for voicing
                midi.addNote(1, 1, pad_note, current_time, 4.0, velocity)
            
            current_time += 4  # 4 beats per measure
            prev_chord = current_chord
    
    def _generate_melodic_content(self, midi: MIDIFile, sequence: str,
                                analysis: Dict, measures: int):
        """Generate lead melody and arpeggiation tracks"""
        melodic_activity = analysis['melodic_activity']
        
        # Use pentatonic subset for melody
        melody_notes = [note for note in self.scale_notes 
                       if (note % 12) in [interval % 12 for interval in self.scales.PENTATONIC['minor']]]
        
        current_time = 0
        
        # Process sequence in chunks for melodic phrases
        chunk_size = 30  # 30 bases per phrase
        sequence_chunks = [sequence[i:i+chunk_size] for i in range(0, len(sequence), chunk_size)]
        
        for measure in range(measures):
            if measure % 8 == 0 and sequence_chunks:  # New phrase every 8 measures
                chunk = sequence_chunks[measure // 8 % len(sequence_chunks)]
                melody_pattern = self._dna_to_melody_pattern(chunk, melody_notes)
            
            # Lead melody (Track 2) - sparse, expressive
            if melodic_activity > 0.3 and measure % 2 == 0:  # Play every other measure
                for i, note in enumerate(melody_pattern[:4]):
                    note_time = current_time + i
                    velocity = int(50 + (melodic_activity * 30))
                    midi.addNote(2, 2, note + 24, note_time, 0.75, velocity)
            
            # Arpeggiation (Track 3) - flowing, continuous
            if measure % 4 < 3:  # Play 3 out of 4 measures
                arp_pattern = melody_pattern[:8]
                for i, note in enumerate(arp_pattern):
                    note_time = current_time + (i * 0.5)
                    velocity = 45 + int((analysis['texture_density'] * 20))
                    midi.addNote(3, 3, note, note_time, 0.25, velocity)
            
            current_time += 4
    
    def _dna_to_melody_pattern(self, chunk: str, available_notes: List[int]) -> List[int]:
        """Convert DNA chunk to melodic pattern using interval relationships"""
        pattern = []
        
        for i in range(0, len(chunk) - 2, 3):
            codon = chunk[i:i+3]
            
            # Map codon to scale degree
            codon_value = sum(ord(base) for base in codon) % len(available_notes)
            note = available_notes[codon_value]
            
            # Add some stepwise motion for melodic coherence
            if pattern:
                # Prefer stepwise motion (within 2-3 semitones)
                prev_note = pattern[-1]
                candidates = [n for n in available_notes 
                            if abs(n - prev_note) <= 4]
                if candidates:
                    # Choose closest candidate to codon mapping
                    note = min(candidates, key=lambda x: abs(x - note))
            
            pattern.append(note)
        
        return pattern
    
    def _generate_atmospheric_elements(self, midi: MIDIFile, sequence: str,
                                     analysis: Dict, measures: int):
        """Generate atmospheric texture and subtle rhythm tracks"""
        gc_content = analysis['gc_content']
        texture_density = analysis['texture_density']
        
        current_time = 0
        
        for measure in range(measures):
            # Atmospheric texture (Track 4) - based on GC content
            if measure % 8 < int(gc_content * 8):  # Vary activity based on GC
                # High notes for atmospheric shimmer
                for i in range(int(texture_density * 4)):
                    note = random.choice(self.scale_notes[-12:])  # High register
                    note_time = current_time + random.uniform(0, 4)
                    velocity = random.randint(25, 40)
                    duration = random.uniform(1.0, 3.0)
                    midi.addNote(4, 4, note, note_time, duration, velocity)
            
            # Subtle rhythmic pulse (Track 5) - very minimal
            if measure % 16 == 0:  # Every 16 measures
                pulse_note = self.scale_notes[len(self.scale_notes)//2]  # Mid-range
                midi.addNote(5, 5, pulse_note, current_time, 0.1, 35)
            
            current_time += 4
    
    def _add_expression_automation(self, midi: MIDIFile, analysis: Dict, measures: int):
        """Add MIDI controllers for expression and atmosphere"""
        current_time = 0
        
        for measure in range(measures):
            # Modulation (CC1) for atmospheric movement
            mod_value = int(64 + 32 * math.sin(measure * 0.1))
            midi.addControllerEvent(1, 1, current_time, 1, mod_value)
            
            # Volume swells (CC7) based on sequence characteristics
            volume_base = 80
            volume_variation = int(analysis['melodic_activity'] * 20)
            volume = volume_base + int(volume_variation * math.sin(measure * 0.05))
            midi.addControllerEvent(2, 2, current_time, 7, volume)
            
            # Pan automation (CC10) for spatial movement
            pan_value = int(64 + 20 * math.sin(measure * 0.03))
            midi.addControllerEvent(3, 3, current_time, 10, pan_value)
            
            current_time += 4


def main():
    """Command-line interface for ambient DNA composition"""
    parser = argparse.ArgumentParser(
        description="Create ambient soundscapes from DNA sequences using music theory"
    )
    
    parser.add_argument('input', help='Input FASTA file with DNA sequence')
    parser.add_argument('-o', '--output', help='Output MIDI file', 
                       default='ambient_dna_composition.mid')
    parser.add_argument('-k', '--key', default='C',
                       choices=['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb'],
                       help='Musical key signature')
    parser.add_argument('-m', '--mode', default='dorian',
                       choices=['dorian', 'lydian', 'phrygian', 'mixolydian', 'aeolian', 'ionian', 'locrian'],
                       help='Musical mode')
    parser.add_argument('-d', '--duration', type=int, default=600,
                       help='Composition duration in seconds')
    parser.add_argument('-t', '--tempo', type=int, default=50,
                       help='Tempo in beats per minute (40-65 recommended for ambient)')
    parser.add_argument('--tracks', type=int, default=6,
                       help='Number of tracks in composition')
    
    args = parser.parse_args()
    
    # Load DNA sequence
    try:
        with open(args.input, 'r') as f:
            record = next(SeqIO.parse(f, "fasta"))
            sequence = str(record.seq)
    except Exception as e:
        print(f"Error reading sequence file: {e}")
        return
    
    # Create ambient configuration
    config = AmbientConfig(
        tempo=args.tempo,
        key_signature=args.key,
        mode=args.mode,
        composition_length=args.duration,
        track_count=args.tracks
    )
    
    # Create composer and generate soundscape
    composer = DNAAmbientComposer(config)
    
    print(f"Generating ambient DNA soundscape...")
    print(f"Sequence: {len(sequence)} base pairs")
    print(f"Key: {args.key} {args.mode}")
    print(f"Tempo: {args.tempo} BPM")
    print(f"Duration: {args.duration // 60}:{args.duration % 60:02d}")
    
    # Analyze sequence for information
    analysis = SequenceAnalyzer.analyze_for_musical_structure(sequence)
    print(f"GC Content: {analysis['gc_content']:.1%}")
    print(f"Suggested mode: {analysis['modal_suggestion']}")
    
    midi = composer.create_ambient_soundscape(sequence, args.output)
    
    print(f"✓ Ambient soundscape generated: {args.output}")
    print("\nTrack Structure:")
    print("Track 0: Bass Foundation")
    print("Track 1: Harmonic Pad")
    print("Track 2: Lead Melody")
    print("Track 3: Arpeggiation")
    print("Track 4: Atmospheric Texture")
    print("Track 5: Rhythmic Pulse")


if __name__ == "__main__":
    main()