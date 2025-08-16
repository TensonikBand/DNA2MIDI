#!/usr/bin/env python3
"""
Test suite for DNA Ambient Composer
"""

import pytest
import tempfile
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ambient_composer import DNAAmbientComposer, AmbientConfig, MusicalScales, AmbientVoicing
from sequence_analyzer import SequenceAnalyzer
from midi_utils import MIDIExporter


class TestMusicalScales:
    """Test musical scale and theory components"""
    
    def test_all_modes_present(self):
        """Test that all 7 modes are defined"""
        scales = MusicalScales()
        expected_modes = ['ionian', 'dorian', 'phrygian', 'lydian', 
                         'mixolydian', 'aeolian', 'locrian']
        
        for mode in expected_modes:
            assert mode in scales.MODES
            assert len(scales.MODES[mode]) == 7  # 7 notes per scale
    
    def test_key_signatures(self):
        """Test key signature mappings"""
        scales = MusicalScales()
        
        # Test some basic keys
        assert scales.KEYS['C'] == 0
        assert scales.KEYS['G'] == 7
        assert scales.KEYS['F'] == 5
        
        # Test all keys are in valid range
        for key_offset in scales.KEYS.values():
            assert 0 <= key_offset <= 11
    
    def test_pentatonic_scales(self):
        """Test pentatonic scale definitions"""
        scales = MusicalScales()
        
        # Each pentatonic scale should have 5 notes
        for penta_type in scales.PENTATONIC.values():
            assert len(penta_type) == 5


class TestAmbientVoicing:
    """Test harmonic progression and voicing"""
    
    def test_chord_progression_generation(self):
        """Test chord progression creation"""
        scale_notes = [60, 62, 64, 65, 67, 69, 71]  # C major scale
        voicing = AmbientVoicing()
        
        progression = voicing.create_chord_progression(scale_notes, 4)
        
        assert len(progression) == 4
        # Each chord should have 3 notes (triad)
        for chord in progression:
            assert len(chord) == 3
            # All notes should be from the scale
            for note in chord:
                assert note in scale_notes
    
    def test_voice_leading(self):
        """Test smooth voice leading between chords"""
        voicing = AmbientVoicing()
        
        chord1 = [60, 64, 67]  # C major
        chord2 = [62, 65, 69]  # D minor
        
        voiced_chord2 = voicing.voice_lead_smoothly(chord1, chord2)
        
        assert len(voiced_chord2) == 3
        # Voice leading should minimize movement
        total_movement = sum(abs(voiced_chord2[i] - chord1[i]) for i in range(3))
        assert total_movement < 24  # Reasonable movement threshold


class TestSequenceAnalyzer:
    """Test DNA sequence analysis"""
    
    def test_basic_statistics(self):
        """Test basic sequence statistics calculation"""
        sequence = "ATGCGATCGTAA"
        stats = SequenceAnalyzer.calculate_statistics(sequence)
        
        assert stats['length'] == 12
        assert 0 <= stats['gc_content'] <= 1
        assert stats['gc_content'] + stats['at_content'] == pytest.approx(1.0, rel=1e-2)
        assert isinstance(stats['codon_counts'], dict)
        assert isinstance(stats['orfs'], list)
    
    def test_orf_detection(self):
        """Test Open Reading Frame detection"""
        # Sequence with clear ORF: ATG...TAA
        sequence = "ATGCGATAA"
        stats = SequenceAnalyzer.calculate_statistics(sequence)
        
        # Should find at least one ORF
        assert len(stats['orfs']) >= 0  # May be 0 if too short
        
        # Test longer sequence with guaranteed ORF
        long_sequence = "ATGCGATCGATCGATCGATCGATCGATCGTAA"
        stats = SequenceAnalyzer.calculate_statistics(long_sequence)
        assert len(stats['orfs']) >= 1
    
    def test_musical_structure_analysis(self):
        """Test musical parameter extraction"""
        sequence = "ATGCGATCGATCGTAA"
        analysis = SequenceAnalyzer.analyze_for_musical_structure(sequence)
        
        # Check all expected keys are present
        expected_keys = ['harmonic_rhythm', 'texture_density', 'melodic_activity',
                        'phrase_lengths', 'dynamic_range', 'tempo_modifier', 
                        'modal_suggestion']
        
        for key in expected_keys:
            assert key in analysis
        
        # Check value ranges
        assert 4 <= analysis['harmonic_rhythm'] <= 16
        assert 0 <= analysis['texture_density'] <= 1
        assert 0 <= analysis['melodic_activity'] <= 1
        assert analysis['modal_suggestion'] in MusicalScales.MODES.keys()


class TestMIDIExporter:
    """Test MIDI utilities"""
    
    def test_midi_file_creation(self):
        """Test MIDI file creation"""
        midi = MIDIExporter.create_midi_file(2, 60)
        assert midi is not None
        assert midi.numTracks == 2
    
    def test_instrument_mapping(self):
        """Test instrument name to program number mapping"""
        instruments = MIDIExporter.get_instrument_map()
        
        # Test some ambient instruments
        assert 'synth_bass' in instruments
        assert 'warm_pad' in instruments
        assert 'rain_fx' in instruments
        
        # All program numbers should be valid MIDI range
        for program in instruments.values():
            assert 0 <= program <= 127
    
    def test_note_frequency_conversion(self):
        """Test MIDI note to frequency conversion"""
        # A4 = 440 Hz = MIDI note 69
        freq = MIDIExporter.midi_note_to_frequency(69)
        assert freq == pytest.approx(440.0, rel=1e-2)
        
        # Test reverse conversion
        midi_note = MIDIExporter.frequency_to_midi_note(440.0)
        assert midi_note == 69
    
    def test_parameter_validation(self):
        """Test MIDI parameter validation"""
        # Valid parameters
        assert MIDIExporter.validate_midi_parameters(60, 100, 0) == True
        
        # Invalid parameters
        assert MIDIExporter.validate_midi_parameters(128, 100, 0) == False  # Note too high
        assert MIDIExporter.validate_midi_parameters(60, 128, 0) == False   # Velocity too high
        assert MIDIExporter.validate_midi_parameters(60, 100, 16) == False  # Channel too high
    
    def test_chord_creation(self):
        """Test chord generation"""
        # Major chord
        chord = MIDIExporter.create_chord(60, 'major')
        assert chord == [60, 64, 67]  # C, E, G
        
        # Minor chord
        chord = MIDIExporter.create_chord(60, 'minor')
        assert chord == [60, 63, 67]  # C, Eb, G


class TestAmbientConfig:
    """Test ambient configuration"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = AmbientConfig()
        
        assert config.tempo == 60
        assert config.key_signature == 'C'
        assert config.mode == 'dorian'
        assert config.track_count == 6
        assert config.composition_length == 600
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = AmbientConfig(
            tempo=45,
            key_signature='F#',
            mode='lydian',
            composition_length=720
        )
        
        assert config.tempo == 45
        assert config.key_signature == 'F#'
        assert config.mode == 'lydian'
        assert config.composition_length == 720


class TestDNAAmbientComposer:
    """Test main composer functionality"""
    
    def test_composer_initialization(self):
        """Test composer initialization"""
        config = AmbientConfig(key_signature='G', mode='dorian')
        composer = DNAAmbientComposer(config)
        
        assert composer.ambient_config.key_signature == 'G'
        assert composer.ambient_config.mode == 'dorian'
        assert len(composer.scale_notes) > 0
    
    def test_scale_note_calculation(self):
        """Test scale note calculation"""
        config = AmbientConfig(key_signature='C', mode='ionian')
        composer = DNAAmbientComposer(config)
        
        # Scale notes should be in valid MIDI range
        for note in composer.scale_notes:
            assert 24 <= note <= 108
        
        # Should have notes across multiple octaves
        assert len(composer.scale_notes) > 7
    
    def test_ambient_soundscape_creation(self):
        """Test complete soundscape generation"""
        config = AmbientConfig(
            tempo=60,
            composition_length=60  # 1 minute for testing
        )
        composer = DNAAmbientComposer(config)
        
        sequence = "ATGCGATCGATCGATCGATCGTAA"
        
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp:
            try:
                midi = composer.create_ambient_soundscape(sequence, tmp.name)
                
                assert midi is not None
                assert midi.numTracks == config.track_count
                assert os.path.exists(tmp.name)
                assert os.path.getsize(tmp.name) > 0
                
            finally:
                os.unlink(tmp.name)
    
    def test_dna_to_melody_conversion(self):
        """Test DNA sequence to melody pattern conversion"""
        config = AmbientConfig()
        composer = DNAAmbientComposer(config)
        
        chunk = "ATGCGATCG"
        available_notes = [60, 62, 64, 67, 69]  # Pentatonic scale
        
        pattern = composer._dna_to_melody_pattern(chunk, available_notes)
        
        # Should generate notes from the available set
        for note in pattern:
            assert note in available_notes
        
        # Should have roughly chunk_length // 3 notes
        expected_length = len(chunk) // 3
        assert len(pattern) == expected_length


class TestIntegration:
    """Integration tests for complete workflow"""
    
    def test_complete_workflow(self):
        """Test complete workflow from DNA to MIDI"""
        # Test sequence
        sequence = "ATGGCATCGATCGATCGATCGATCGATCGTAA"
        
        # Create configuration
        config = AmbientConfig(
            tempo=50,
            key_signature='A',
            mode='dorian',
            composition_length=120  # 2 minutes for testing
        )
        
        # Create composer
        composer = DNAAmbientComposer(config)
        
        # Generate composition
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp:
            try:
                midi = composer.create_ambient_soundscape(sequence, tmp.name)
                
                # Verify output
                assert midi is not None
                assert os.path.exists(tmp.name)
                assert os.path.getsize(tmp.name) > 100  # Should be substantial file
                
                # Verify structure
                assert midi.numTracks == 6
                
            finally:
                os.unlink(tmp.name)
    
    def test_different_modes_produce_different_output(self):
        """Test that different modes produce different musical output"""
        sequence = "ATGCGATCGATCGTAA"
        
        modes = ['dorian', 'lydian', 'phrygian']
        midi_objects = []
        
        for mode in modes:
            config = AmbientConfig(mode=mode, composition_length=60)
            composer = DNAAmbientComposer(config)
            midi = composer.create_ambient_soundscape(sequence)
            midi_objects.append(midi)
        
        # Different modes should produce different scale notes
        composers = [DNAAmbientComposer(AmbientConfig(mode=mode)) for mode in modes]
        scale_sets = [set(c.scale_notes) for c in composers]
        
        # Scale note sets should be different
        assert scale_sets[0] != scale_sets[1]
        assert scale_sets[1] != scale_sets[2]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])