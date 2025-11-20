#!/usr/bin/env python3
"""
DNA Ambient Composer - Quick Start
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from ambient_composer import DNAAmbientComposer, AmbientConfig
    from sequence_analyzer import SequenceAnalyzer
    print("DNA Ambient Composer modules loaded successfully")
except ImportError as e:
    print(f"Import error: {e}")
    print("\nPlease install requirements first:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def quick_demo():
    """Generate a quick ambient demo"""
    print("\n🧬 DNA Ambient Composer - Quick Demo")
    print("=" * 40)
    
    # Sample DNA sequence (human insulin gene fragment)
    sample_sequence = """
    ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCTGAC
    CCAGCCGCAGCCTTTGTGAACCAACACCTGTGCGGCTCACACCTGGTGGAAGCTCTCTAC
    CTAGTGTGCGGGGAACGAGGCTTCTTCTACACACCCAAGACCCGCCGGGAGGCAGAGGAC
    """.replace('\n', '').replace(' ', '')
    
    print(f"Sample DNA sequence: {len(sample_sequence)} base pairs")
    
    # Analyze the sequence
    stats = SequenceAnalyzer.calculate_statistics(sample_sequence)
    musical_analysis = SequenceAnalyzer.analyze_for_musical_structure(sample_sequence)
    
    print(f"GC Content: {stats['gc_content']:.1%}")
    print(f"Suggested musical mode: {musical_analysis['modal_suggestion']}")
    
    # Create ambient configuration
    config = AmbientConfig(
        tempo=55,
        key_signature='C',
        mode='dorian',
        composition_length=180,  # 3 minutes for quick demo
        track_count=6
    )
    
    print(f"\nGenerating ambient composition...")
    print(f"Key: {config.key_signature} {config.mode}")
    print(f"Tempo: {config.tempo} BPM")
    print(f"Duration: {config.composition_length // 60}:{config.composition_length % 60:02d}")
    
    # Create composer and generate
    composer = DNAAmbientComposer(config)
    
    output_file = "quickstart_demo.mid"
    midi = composer.create_ambient_soundscape(sample_sequence, output_file)
    
    print(f"\nSuccess! Generated: {output_file}")
    print("\nTrack Structure:")
    print("Track 0: Bass Foundation")
    print("Track 1: Harmonic Pad") 
    print("Track 2: Lead Melody")
    print("Track 3: Arpeggiation")
    print("Track 4: Atmospheric Texture")
    print("Track 5: Rhythmic Pulse")
    
    print(f"\n🎧 Open '{output_file}' in your favorite music software!")
    print("Recommended: Add reverb and slow attack/release for full ambient effect.")
    
    return output_file


def interactive_composer():
    """Interactive composition tool"""
    print("\nInteractive Ambient Composer")
    print("=" * 35)
    
    # Get user preferences
    print("\nCustomize your ambient composition:")
    
    # Key selection
    keys = ['C', 'G', 'D', 'A', 'E', 'F', 'Bb', 'Eb']
    print(f"\nAvailable keys: {', '.join(keys)}")
    key = input("Select key (default C): ").strip().upper() or 'C'
    if key not in keys:
        print(f"Invalid key, using C")
        key = 'C'
    
    # Mode selection
    modes = {
        '1': ('dorian', 'Ethereal, balanced'),
        '2': ('lydian', 'Dreamy, floating'),
        '3': ('phrygian', 'Dark, mysterious'),
        '4': ('mixolydian', 'Warm, grounded'),
        '5': ('aeolian', 'Melancholic'),
        '6': ('ionian', 'Bright, optimistic')
    }
    
    print(f"\nMusical modes:")
    for num, (mode, desc) in modes.items():
        print(f"{num}. {mode.title()} - {desc}")
    
    mode_choice = input("Select mode (1-6, default 1): ").strip() or '1'
    mode_name, mode_desc = modes.get(mode_choice, modes['1'])
    
    # Duration
    try:
        duration = int(input("Duration in minutes (default 5): ") or 5)
        duration = max(1, min(duration, 20))  # Limit 1-20 minutes
    except ValueError:
        duration = 5
    
    # Tempo
    try:
        tempo = int(input("Tempo in BPM (40-70, default 50): ") or 50)
        tempo = max(40, min(tempo, 70))  # Ambient range
    except ValueError:
        tempo = 50
    
    # Use provided sequence or default
    data_dir = Path(__file__).parent / 'data'
    sequences = {
        '1': ('human_insulin.fasta', 'Human insulin gene'),
        '2': ('brca1_fragment.fasta', 'BRCA1 tumor suppressor'),
        '3': ('covid_spike.fasta', 'SARS-CoV-2 spike protein'),
        '4': ('chlorophyll_synth.fasta', 'Chlorophyll biosynthesis'),
        '5': ('mitochondrial_atp.fasta', 'Mitochondrial ATP synthase')
    }
    
    print(f"\nAvailable DNA sequences:")
    for num, (file, desc) in sequences.items():
        print(f"{num}. {desc}")
    
    seq_choice = input("Select sequence (1-5, default 1): ").strip() or '1'
    seq_file, seq_desc = sequences.get(seq_choice, sequences['1'])
    
    # Load sequence
    try:
        from Bio import SeqIO
        with open(data_dir / seq_file, 'r') as f:
            record = next(SeqIO.parse(f, "fasta"))
            sequence = str(record.seq)
    except Exception as e:
        print(f"Error loading sequence, using default: {e}")
        sequence = "ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCTGAC"
        seq_desc = "Default insulin fragment"
    
    # Create configuration
    config = AmbientConfig(
        tempo=tempo,
        key_signature=key,
        mode=mode_name,
        composition_length=duration * 60,
        track_count=6
    )
    
    # Generate composition
    print(f"\nGenerating ambient composition...")
    print(f"DNA: {seq_desc} ({len(sequence)} bp)")
    print(f"Music: {key} {mode_name} at {tempo} BPM")
    print(f"Duration: {duration} minutes")
    
    composer = DNAAmbientComposer(config)
    output_file = f"ambient_{key}_{mode_name}_{duration}min.mid"
    
    try:
        midi = composer.create_ambient_soundscape(sequence, output_file)
        print(f"\nGenerated: {output_file}")
        print(f"Character: {mode_desc}")
        return output_file
    except Exception as e:
        print(f"Error generating composition: {e}")
        return None


def main():
    """Main quickstart interface"""
    print("DNA Ambient Composer")
    print("Transform biological sequences into ambient soundscapes")
    print("=" * 55)
    
    options = [
        ("Quick Demo (30 seconds)", quick_demo),
        ("Interactive Composer", interactive_composer),
        ("Exit", lambda: None)
    ]
    
    print("\nQuick Start Options:")
    for i, (name, _) in enumerate(options, 1):
        print(f"{i}. {name}")
    
    while True:
        try:
            choice = input(f"\nSelect option (1-{len(options)}): ")
            choice = int(choice)
            
            if choice == len(options):  # Exit
                print("🎵 Happy composing!")
                break
            elif 1 <= choice <= len(options) - 1:
                result = options[choice - 1][1]()
                if result:
                    again = input("\nGenerate another composition? (y/n): ")
                    if again.lower() != 'y':
                        print("🎵 Happy composing!")
                        break
            else:
                print("Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n🎵 Goodbye!")
            break
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()