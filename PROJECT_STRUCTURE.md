## Quick Start

### Installation
```bash
git clone <repository-url>
cd DNA-Ambient-Composer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Instant Demo
```bash
python quickstart.py
```

### Command Line Usage
```bash
# Basic ambient composition
python src/ambient_composer.py data/human_insulin.fasta -o my_composition.mid

# Custom parameters
python src/ambient_composer.py data/brca1_fragment.fasta -k A -m lydian -d 720 -t 50
```

### Interactive Examples
```bash
# Curated gallery
python examples/ambient_gallery.py

# Modal comparison
python examples/modal_comparison.py
```

### Testing
```bash
python -m pytest tests/ -v
```

## Sample Data Included

1. **human_insulin.fasta** - Human insulin gene (chromosome 11)
2. **brca1_fragment.fasta** - BRCA1 tumor suppressor gene fragment
3. **covid_spike.fasta** - SARS-CoV-2 spike protein gene
4. **chlorophyll_synth.fasta** - Plant chlorophyll biosynthesis gene
5. **mitochondrial_atp.fasta** - Human mitochondrial ATP synthase

## Generated Output

All examples generate standard MIDI files with 6 tracks:
- **Track 0**: Bass Foundation
- **Track 1**: Harmonic Pad
- **Track 2**: Lead Melody
- **Track 3**: Arpeggiation
- **Track 4**: Atmospheric Texture
- **Track 5**: Rhythmic Pulse

## Dependencies

- **biopython** - DNA sequence analysis
- **MIDIUtil** - MIDI file generation
- **numpy** - Numerical computations
- **pytest** - Testing framework
- **hypothesis** - Property-based testing

## Musical Features

- **6 Musical Modes**: Dorian, Lydian, Phrygian, Mixolydian, Aeolian, Ionian
- **12 Key Signatures**: All major and minor keys
- **Ambient Tempos**: 40-70 BPM range
- **Long-form Compositions**: 8-15 minute pieces
- **Music Theory Based**: Voice leading, modal harmony, pentatonic melodies

## Research Foundation

Based on:
- DNA sonification research (BMC Bioinformatics)
- Ambient music composition techniques
- Music theory and modal harmony
- Bioinformatics sequence analysis
