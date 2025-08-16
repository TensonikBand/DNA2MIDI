"""
DNA Ambient Composer - Transform DNA sequences into ambient soundscapes
"""

from .ambient_composer import DNAAmbientComposer, AmbientConfig, MusicalScales
from .sequence_analyzer import SequenceAnalyzer
from .midi_utils import MIDIExporter

__version__ = "1.0.0"
__author__ = "DNA Ambient Composer Team"
__email__ = "contact@dna-ambient-composer.org"

__all__ = [
    "DNAAmbientComposer",
    "AmbientConfig", 
    "MusicalScales",
    "SequenceAnalyzer",
    "MIDIExporter"
]