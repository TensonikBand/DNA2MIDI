#!/usr/bin/env python3
"""
Ambient DNA Composition Gallery
Interactive examples showcasing different DNA sequences and musical modes
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ambient_composer import DNAAmbientComposer, AmbientConfig
from sequence_analyzer import SequenceAnalyzer
from Bio import SeqIO


def create_output_directory():
    """Create output directory for generated MIDI files"""
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    return output_dir


def load_sequence(fasta_file: Path) -> str:
    """Load DNA sequence from FASTA file"""
    try:
        with open(fasta_file, 'r') as f:
            record = next(SeqIO.parse(f, "fasta"))
            return str(record.seq)
    except Exception as e:
        print(f"Error loading {fasta_file}: {e}")
        return None


def example_1_ethereal_human_gene():
    """Create ethereal ambient from human BRCA1 gene"""
    print("\nExample 1: Ethereal Human Gene Soundscape")
    print("=" * 50)
    
    data_dir = Path(__file__).parent.parent / 'data'
    output_dir = create_output_directory()
    
    sequence = load_sequence(data_dir / 'brca1_fragment.fasta')
    if not sequence:
        return
    
    config = AmbientConfig(
        tempo=48,
        key_signature='A',
        mode='lydian',  # Dreamy, floating quality
        composition_length=480,  # 8 minutes
        track_count=6
    )
    
    composer = DNAAmbientComposer(config)
    
    # Analyze the sequence
    stats = SequenceAnalyzer.calculate_statistics(sequence)
    print(f"Sequence: BRCA1 tumor suppressor gene ({len(sequence)} bp)")
    print(f"GC Content: {stats['gc_content']:.1%}")
    print(f"Musical Key: {config.key_signature} {config.mode}")
    print(f"ORFs found: {len(stats['orfs'])}")
    
    output_file = output_dir / "ethereal_brca1.mid"
    midi = composer.create_ambient_soundscape(sequence, str(output_file))
    print(f"Generated: {output_file}")
    print("  Character: Ethereal, floating, transcendent")


def example_2_dark_viral_sequence():
    """Create dark ambient from viral sequence"""
    print("\nExample 2: Dark Viral Soundscape")
    print("=" * 50)
    
    data_dir = Path(__file__).parent.parent / 'data'
    output_dir = create_output_directory()
    
    sequence = load_sequence(data_dir / 'covid_spike.fasta')
    if not sequence:
        return
    
    config = AmbientConfig(
        tempo=42,
        key_signature='Eb',
        mode='phrygian',  # Dark, mysterious
        composition_length=600,
        track_count=6
    )
    
    composer = DNAAmbientComposer(config)
    
    stats = SequenceAnalyzer.calculate_statistics(sequence)
    print(f"Sequence: SARS-CoV-2 spike protein ({len(sequence)} bp)")
    print(f"GC Content: {stats['gc_content']:.1%}")
    print(f"Musical Key: {config.key_signature} {config.mode}")
    print(f"Codon diversity: {len(stats['codon_counts'])}")
    
    output_file = output_dir / "dark_covid_spike.mid"
    midi = composer.create_ambient_soundscape(sequence, str(output_file))
    print(f"Generated: {output_file}")
    print("  Character: Dark, mysterious, unsettling")


def example_3_warm_plant_chlorophyll():
    """Create warm ambient from plant photosynthesis genes"""
    print("\nExample 3: Warm Chlorophyll Soundscape")
    print("=" * 50)
    
    data_dir = Path(__file__).parent.parent / 'data'
    output_dir = create_output_directory()
    
    sequence = load_sequence(data_dir / 'chlorophyll_synth.fasta')
    if not sequence:
        return
    
    config = AmbientConfig(
        tempo=58,
        key_signature='G',
        mode='mixolydian',  # Warm, grounded
        composition_length=360,  # 6 minutes
        track_count=6
    )
    
    composer = DNAAmbientComposer(config)
    
    stats = SequenceAnalyzer.calculate_statistics(sequence)
    print(f"Sequence: Chlorophyll biosynthesis ({len(sequence)} bp)")
    print(f"GC Content: {stats['gc_content']:.1%}")
    print(f"Musical Key: {config.key_signature} {config.mode}")
    print(f"Repetitive nature: High GC content, structured patterns")
    
    output_file = output_dir / "warm_chlorophyll.mid"
    midi = composer.create_ambient_soundscape(sequence, str(output_file))
    print(f"Generated: {output_file}")
    print("  Character: Warm, grounded, organic growth")


def example_4_meditative_mitochondrial():
    """Create meditative ambient from mitochondrial DNA"""
    print("\nExample 4: Meditative Mitochondrial Soundscape")
    print("=" * 50)
    
    data_dir = Path(__file__).parent.parent / 'data'
    output_dir = create_output_directory()
    
    sequence = load_sequence(data_dir / 'mitochondrial_atp.fasta')
    if not sequence:
        return
    
    config = AmbientConfig(
        tempo=52,
        key_signature='C',
        mode='dorian',  # Balanced, meditative
        composition_length=720,  # 12 minutes
        track_count=6
    )
    
    composer = DNAAmbientComposer(config)
    
    stats = SequenceAnalyzer.calculate_statistics(sequence)
    print(f"Sequence: Mitochondrial ATP synthase ({len(sequence)} bp)")
    print(f"GC Content: {stats['gc_content']:.1%}")
    print(f"Musical Key: {config.key_signature} {config.mode}")
    print(f"Cellular energy: Powers life at the cellular level")
    
    output_file = output_dir / "meditative_mitochondrial.mid"
    midi = composer.create_ambient_soundscape(sequence, str(output_file))
    print(f"Generated: {output_file}")
    print("  Character: Meditative, balanced, life-sustaining energy")


def example_5_gentle_insulin():
    """Create gentle ambient from human insulin gene"""
    print("\nExample 5: Gentle Insulin Soundscape")
    print("=" * 50)
    
    data_dir = Path(__file__).parent.parent / 'data'
    output_dir = create_output_directory()
    
    sequence = load_sequence(data_dir / 'human_insulin.fasta')
    if not sequence:
        return
    
    config = AmbientConfig(
        tempo=55,
        key_signature='F',
        mode='ionian',  # Gentle major
        composition_length=540,  # 9 minutes
        track_count=6
    )
    
    composer = DNAAmbientComposer(config)
    
    stats = SequenceAnalyzer.calculate_statistics(sequence)
    print(f"Sequence: Human insulin gene ({len(sequence)} bp)")
    print(f"GC Content: {stats['gc_content']:.1%}")
    print(f"Musical Key: {config.key_signature} {config.mode}")
    print(f"Function: Blood sugar regulation, metabolic balance")
    
    output_file = output_dir / "gentle_insulin.mid"
    midi = composer.create_ambient_soundscape(sequence, str(output_file))
    print(f"Generated: {output_file}")
    print("  Character: Gentle, nurturing, regulatory balance")


def generate_all_examples():
    """Generate all example compositions"""
    print("DNA Ambient Composition Gallery")
    print("Creating ambient soundscapes from biological sequences...")
    print("=" * 60)
    
    examples = [
        example_1_ethereal_human_gene,
        example_2_dark_viral_sequence,
        example_3_warm_plant_chlorophyll,
        example_4_meditative_mitochondrial,
        example_5_gentle_insulin
    ]
    
    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"Error in {example_func.__name__}: {e}")
    
    output_dir = Path(__file__).parent / 'output'
    midi_files = list(output_dir.glob("*.mid"))
    
    print(f"\nGallery Complete! Generated {len(midi_files)} ambient compositions")
    print("\nGenerated Files:")
    for file in sorted(midi_files):
        print(f"  {file.name}")
    
    print(f"\nFiles saved to: {output_dir}")
    print("\n🎧 Open these MIDI files in your favorite DAW or music player")
    print("   Recommended: Add reverb and slow attack/release for full ambient effect")


def main():
    """Interactive gallery menu"""
    examples = [
        ("Ethereal Human Gene (BRCA1)", example_1_ethereal_human_gene),
        ("Dark Viral Sequence (COVID-19)", example_2_dark_viral_sequence),
        ("Warm Plant Chlorophyll", example_3_warm_plant_chlorophyll),
        ("Meditative Mitochondrial", example_4_meditative_mitochondrial),
        ("Gentle Insulin Regulation", example_5_gentle_insulin),
        ("Generate All Examples", generate_all_examples)
    ]
    
    print("DNA Ambient Composition Gallery")
    print("=" * 40)
    print("Transform biological sequences into ambient soundscapes")
    print("\nAvailable compositions:")
    
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    print("0. Exit")
    
    while True:
        try:
            choice = input(f"\nSelect composition (0-{len(examples)}): ")
            choice = int(choice)
            
            if choice == 0:
                print("Thank you for exploring DNA ambient composition!")
                break
            elif 1 <= choice <= len(examples):
                examples[choice - 1][1]()
            else:
                print("Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()