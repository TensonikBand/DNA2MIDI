#!/usr/bin/env python3
"""
Modal Comparison Suite
Demonstrates how different musical modes affect the same DNA sequence
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ambient_composer import DNAAmbientComposer, AmbientConfig
from sequence_analyzer import SequenceAnalyzer
from Bio import SeqIO


def create_modal_comparison():
    """Create the same DNA sequence in different musical modes"""
    print("Modal Comparison Suite")
    print("=" * 40)
    print("Same DNA sequence, different musical characters")
    
    # Create output directory
    output_dir = Path(__file__).parent / 'output' / 'modal_comparison'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load a sequence for comparison
    data_dir = Path(__file__).parent.parent / 'data'
    
    try:
        with open(data_dir / 'human_insulin.fasta', 'r') as f:
            record = next(SeqIO.parse(f, "fasta"))
            sequence = str(record.seq)
    except Exception as e:
        print(f"Error loading sequence: {e}")
        return
    
    # Analyze the base sequence
    stats = SequenceAnalyzer.calculate_statistics(sequence)
    print(f"\nBase Sequence: Human insulin gene ({len(sequence)} bp)")
    print(f"GC Content: {stats['gc_content']:.1%}")
    
    # Define modes with their characteristics
    modes = {
        'dorian': {
            'description': 'Ethereal, balanced minor with raised 6th',
            'character': 'Mystical, contemplative',
            'key': 'D'
        },
        'lydian': {
            'description': 'Dreamy major with raised 4th', 
            'character': 'Floating, transcendent',
            'key': 'F'
        },
        'phrygian': {
            'description': 'Dark minor with flat 2nd',
            'character': 'Mysterious, ancient',
            'key': 'E'
        },
        'mixolydian': {
            'description': 'Bluesy major with flat 7th',
            'character': 'Warm, grounded',
            'key': 'G'
        },
        'aeolian': {
            'description': 'Natural minor scale',
            'character': 'Melancholic, introspective',
            'key': 'A'
        },
        'ionian': {
            'description': 'Bright major scale',
            'character': 'Optimistic, clear',
            'key': 'C'
        }
    }
    
    generated_files = []
    
    print(f"\nGenerating compositions in {len(modes)} different modes...")
    print("-" * 50)
    
    for mode_name, mode_info in modes.items():
        print(f"\n{mode_name.title()} Mode ({mode_info['key']} {mode_name})")
        print(f"   Character: {mode_info['character']}")
        print(f"   Theory: {mode_info['description']}")
        
        # Create configuration for this mode
        config = AmbientConfig(
            tempo=55,  # Consistent tempo for comparison
            key_signature=mode_info['key'],
            mode=mode_name,
            composition_length=240,  # 4 minutes each for comparison
            track_count=6
        )
        
        # Generate composition
        composer = DNAAmbientComposer(config)
        output_file = output_dir / f"insulin_{mode_name}_{mode_info['key']}.mid"
        
        try:
            midi = composer.create_ambient_soundscape(sequence, str(output_file))
            generated_files.append(output_file)
            print(f"   Generated: {output_file.name}")
        except Exception as e:
            print(f"   Error: {e}")
    
    # Summary
    print(f"\nModal Comparison Complete!")
    print(f"Generated {len(generated_files)} compositions from the same DNA sequence")
    print(f"\nFiles saved to: {output_dir}")
    
    print(f"\nListening Guide:")
    print("=" * 30)
    for mode_name, mode_info in modes.items():
        filename = f"insulin_{mode_name}_{mode_info['key']}.mid"
        print(f" {filename}")
        print(f"   Listen for: {mode_info['character']}")
        print(f"   Key feeling: {mode_info['description']}")
        print()
    
    print("Notice how the same biological data creates completely different")
    print("   emotional experiences through different musical modes!")
    
    return generated_files


def create_key_comparison():
    """Create the same mode in different keys"""
    print("\nKey Comparison Suite")
    print("=" * 40)
    print("Same mode (Dorian), different keys")
    
    # Create output directory
    output_dir = Path(__file__).parent / 'output' / 'key_comparison'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load sequence
    data_dir = Path(__file__).parent.parent / 'data'
    
    try:
        with open(data_dir / 'brca1_fragment.fasta', 'r') as f:
            record = next(SeqIO.parse(f, "fasta"))
            sequence = str(record.seq)
    except Exception as e:
        print(f"Error loading sequence: {e}")
        return
    
    # Different keys to compare
    keys = ['C', 'D', 'F#', 'Ab']
    key_descriptions = {
        'C': 'Neutral, balanced',
        'D': 'Bright, energetic', 
        'F#': 'Sharp, crystalline',
        'Ab': 'Dark, rich'
    }
    
    generated_files = []
    
    print(f"Using BRCA1 gene sequence in Dorian mode")
    print("-" * 40)
    
    for key in keys:
        print(f"\n{key} Dorian")
        print(f"   Character: {key_descriptions[key]}")
        
        config = AmbientConfig(
            tempo=50,
            key_signature=key,
            mode='dorian',
            composition_length=180,  # 3 minutes each
            track_count=6
        )
        
        composer = DNAAmbientComposer(config)
        output_file = output_dir / f"brca1_dorian_{key}.mid"
        
        try:
            midi = composer.create_ambient_soundscape(sequence, str(output_file))
            generated_files.append(output_file)
            print(f"   Generated: {output_file.name}")
        except Exception as e:
            print(f"   Error: {e}")
    
    print(f"\nKey Comparison Complete!")
    print(f"Generated {len(generated_files)} compositions in different keys")
    print(f"Files saved to: {output_dir}")
    
    return generated_files


def main():
    """Main comparison suite"""
    print("DNA Musical Mode & Key Comparison")
    print("=" * 50)
    print("Explore how music theory transforms the same biological data")
    
    options = [
        ("Modal Comparison (6 modes, same DNA)", create_modal_comparison),
        ("Key Comparison (4 keys, same mode)", create_key_comparison),
        ("Generate Both Suites", lambda: [create_modal_comparison(), create_key_comparison()])
    ]
    
    print("\nComparison options:")
    for i, (name, _) in enumerate(options, 1):
        print(f"{i}. {name}")
    print("0. Exit")
    
    while True:
        try:
            choice = input(f"\nSelect comparison (0-{len(options)}): ")
            choice = int(choice)
            
            if choice == 0:
                print("Comparison complete!")
                break
            elif 1 <= choice <= len(options):
                result = options[choice - 1][1]()
                
                if choice == 3:  # Both suites
                    print("\nBoth comparison suites generated!")
                    print("Explore how the same DNA creates different musical experiences")
                    print("through the lens of music theory!")
                
                input("\nPress Enter to continue...")
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