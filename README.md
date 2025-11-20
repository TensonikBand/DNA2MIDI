# DNA Ambient Composer

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Transform DNA sequences into beautiful ambient soundscapes using music theory and compositional techniques. This system creates 10+ minute structured ambient compositions that map biological features to musical parameters.

## Features

- **Music Theory-Based**: Uses modal harmony, voice leading, and proper compositional structure
- **6-Track Ambient Soundscapes**: Each track generated individually with specific roles
- **Multiple Musical Modes**: Dorian, Lydian, Phrygian, Mixolydian, Aeolian, Ionian
- **Biological Mapping**: GC content, ORF structure, and sequence complexity drive musical parameters
- **Long-Form Compositions**: 8-15 minute ambient pieces suitable for meditation and study
- **Professional Output**: Standard MIDI files compatible with any DAW

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/DNA-Ambient-Composer.git
cd DNA-Ambient-Composer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Generate a 10-minute ambient piece
python src/ambient_composer.py data/sample_human_gene.fasta -o my_ambient_piece.mid

# Custom ambient composition
python src/ambient_composer.py data/viral_sequence.fasta -k A -m lydian -d 720 -t 50 -o ethereal_soundscape.mid
```

### Examples

```bash
# Run interactive examples
python examples/ambient_gallery.py

# Generate comparison suite
python examples/modal_comparison.py
```

## Musical Structure

### Track Layout
- **Track 0**: Bass Foundation (harmonic grounding)
- **Track 1**: Harmonic Pad (warm chord progressions)
- **Track 2**: Lead Melody (expressive melodic lines)
- **Track 3**: Arpeggiation (flowing patterns)
- **Track 4**: Atmospheric Texture (high-register movement)
- **Track 5**: Rhythmic Pulse (subtle temporal anchoring)

### DNA-to-Music Mapping
- **GC Content** → Harmonic activity and texture density
- **Sequence Length** → Phrase structure and development  
- **Codon Diversity** → Melodic complexity
- **ORF Structure** → Large-scale musical form
- **Purine/Pyrimidine Balance** → Melodic direction

## Sample Data

Included sample sequences:
- `human_insulin.fasta` - Human insulin gene
- `brca1_fragment.fasta` - Tumor suppressor gene
- `covid_spike.fasta` - SARS-CoV-2 spike protein
- `chlorophyll_synth.fasta` - Plant photosynthesis gene
- `mitochondrial_atp.fasta` - ATP synthase gene

## Use Cases

- **Research**: Sonification for pattern recognition in genomic data
- **Education**: Teaching genetics through multisensory experience
- **Art**: Creating music from personal or species genomes
- **Meditation**: Long-form ambient music for relaxation
- **Accessibility**: Making genomic data accessible through sound

## API Reference

### Basic Usage

```python
from src.ambient_composer import DNAAmbientComposer, AmbientConfig

# Configure composition
config = AmbientConfig(
    tempo=50,
    key_signature='A',
    mode='dorian',
    composition_length=600,  # 10 minutes
    track_count=6
)

# Create composer
composer = DNAAmbientComposer(config)

# Generate ambient piece
midi = composer.create_ambient_soundscape(dna_sequence, "output.mid")
```

### Command Line Interface

```bash
python src/ambient_composer.py [sequence.fasta] [options]

Options:
  -o, --output FILE         Output MIDI file
  -k, --key KEY            Musical key (C, G, D, A, E, B, F#, F, Bb, Eb, Ab, Db, Gb)
  -m, --mode MODE          Musical mode (dorian, lydian, phrygian, mixolydian, aeolian, ionian)
  -d, --duration SECONDS   Composition duration in seconds (default: 600)
  -t, --tempo BPM          Tempo in beats per minute (default: 50)
  --tracks COUNT           Number of tracks (default: 6)
```

## Musical Modes Guide

- **Dorian**: Minor with raised 6th - ethereal, balanced, great for human genes
- **Lydian**: Major with raised 4th - dreamy, floating, perfect for transcendent themes
- **Phrygian**: Minor with flat 2nd - dark, mysterious, ideal for viral sequences
- **Mixolydian**: Major with flat 7th - bluesy, grounded, good for plant genes
- **Aeolian**: Natural minor - melancholic, introspective
- **Ionian**: Major scale - bright, optimistic

## Biological Context

The system analyzes DNA sequences for:
- **GC Content**: Ratio of guanine and cytosine bases
- **Codon Usage**: Frequency of genetic codons
- **Open Reading Frames (ORFs)**: Potential protein-coding regions
- **Sequence Complexity**: Information content and patterns
- **Base Composition**: Purine vs pyrimidine balance

These biological features are mapped to musical parameters using compositional techniques from ambient music theory.

## Research Background

Based on research in:
- DNA sonification (Temple, M.D. BMC Bioinformatics 2017)
- Ambient music composition techniques (Brian Eno, Harold Budd)
- Music theory and modal harmony
- Bioinformatics sequence analysis

## Acknowledgments

- BioPython community for sequence analysis tools
- MIDIUtil library for MIDI generation
- Ambient music pioneers for compositional inspiration
- Genomics research community for scientific foundation
