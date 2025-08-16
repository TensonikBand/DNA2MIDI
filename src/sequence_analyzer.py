#!/usr/bin/env python3
"""
DNA Sequence Analysis for Musical Composition
Extracts biological features for mapping to musical parameters
"""

from typing import Dict, List, Tuple
import re


class SequenceAnalyzer:
    """Analyze DNA sequences for musical composition parameters"""

    @staticmethod
    def calculate_statistics(sequence: str) -> Dict:
        """Calculate comprehensive sequence statistics for musical mapping"""
        sequence = sequence.upper().replace(' ', '').replace('\n', '')
        
        # Basic composition
        length = len(sequence)
        if length == 0:
            return {
                'length': 0,
                'gc_content': 0,
                'at_content': 0,
                'codon_counts': {},
                'orfs': [],
                'purine_content': 0,
                'pyrimidine_content': 0,
                'complexity': 0
            }
        
        # Base composition
        a_count = sequence.count('A')
        t_count = sequence.count('T') 
        g_count = sequence.count('G')
        c_count = sequence.count('C')
        
        gc_content = (g_count + c_count) / length
        at_content = (a_count + t_count) / length
        purine_content = (a_count + g_count) / length  # A, G
        pyrimidine_content = (c_count + t_count) / length  # C, T
        
        # Codon usage
        codon_counts = {}
        for i in range(0, len(sequence) - 2, 3):
            codon = sequence[i:i + 3]
            if len(codon) == 3 and all(base in 'ATGC' for base in codon):
                codon_counts[codon] = codon_counts.get(codon, 0) + 1
        
        # Find ORFs (Open Reading Frames)
        orfs = SequenceAnalyzer._find_orfs(sequence)
        
        # Calculate sequence complexity (Shannon entropy approximation)
        complexity = SequenceAnalyzer._calculate_complexity(sequence)
        
        # Repetitive patterns
        repetitive_score = SequenceAnalyzer._calculate_repetitive_score(sequence)
        
        return {
            'length': length,
            'gc_content': gc_content,
            'at_content': at_content,
            'purine_content': purine_content,
            'pyrimidine_content': pyrimidine_content,
            'codon_counts': codon_counts,
            'orfs': orfs,
            'complexity': complexity,
            'repetitive_score': repetitive_score,
            'base_counts': {
                'A': a_count,
                'T': t_count,
                'G': g_count,
                'C': c_count
            }
        }
    
    @staticmethod
    def _find_orfs(sequence: str) -> List[Tuple[int, int, int]]:
        """Find Open Reading Frames in all three reading frames"""
        orfs = []
        
        for frame in range(3):
            seq = sequence[frame:]
            start_positions = []
            
            for i in range(0, len(seq) - 2, 3):
                codon = seq[i:i + 3]
                
                if codon == 'ATG':  # Start codon
                    start_positions.append(i + frame)
                elif codon in ['TAA', 'TAG', 'TGA'] and start_positions:  # Stop codons
                    start_pos = start_positions.pop(0)
                    end_pos = i + frame + 3
                    orf_length = end_pos - start_pos
                    
                    # Only include ORFs longer than 30 bp
                    if orf_length >= 30:
                        orfs.append((start_pos, end_pos, orf_length))
        
        # Sort by length (longest first)
        orfs.sort(key=lambda x: x[2], reverse=True)
        return orfs
    
    @staticmethod
    def _calculate_complexity(sequence: str) -> float:
        """Calculate sequence complexity using dinucleotide frequency"""
        if len(sequence) < 2:
            return 0.0
        
        # Count dinucleotides
        dinuc_counts = {}
        for i in range(len(sequence) - 1):
            dinuc = sequence[i:i + 2]
            if all(base in 'ATGC' for base in dinuc):
                dinuc_counts[dinuc] = dinuc_counts.get(dinuc, 0) + 1
        
        total_dinucs = sum(dinuc_counts.values())
        if total_dinucs == 0:
            return 0.0
        
        # Calculate Shannon entropy
        entropy = 0.0
        for count in dinuc_counts.values():
            if count > 0:
                p = count / total_dinucs
                entropy -= p * (p.bit_length() - 1)  # Approximation of log2
        
        # Normalize to 0-1 range
        max_entropy = 4.0  # log2(16) for 16 possible dinucleotides
        return entropy / max_entropy
    
    @staticmethod
    def _calculate_repetitive_score(sequence: str) -> float:
        """Calculate how repetitive the sequence is"""
        if len(sequence) < 6:
            return 0.0
        
        # Look for repeating patterns of length 3-10
        total_bases = len(sequence)
        repetitive_bases = 0
        
        for pattern_length in range(3, min(11, len(sequence) // 2)):
            for i in range(len(sequence) - pattern_length * 2):
                pattern = sequence[i:i + pattern_length]
                
                # Check how many times this pattern repeats consecutively
                repeats = 1
                pos = i + pattern_length
                
                while pos + pattern_length <= len(sequence):
                    if sequence[pos:pos + pattern_length] == pattern:
                        repeats += 1
                        pos += pattern_length
                    else:
                        break
                
                if repeats >= 2:
                    repetitive_bases += repeats * pattern_length
        
        return min(1.0, repetitive_bases / total_bases)
    
    @staticmethod
    def analyze_for_musical_structure(sequence: str) -> Dict:
        """Analyze sequence specifically for musical composition parameters"""
        stats = SequenceAnalyzer.calculate_statistics(sequence)
        
        # Map biological features to musical parameters
        gc_content = stats['gc_content']
        complexity = stats['complexity']
        repetitive_score = stats['repetitive_score']
        
        # Musical structure parameters
        musical_analysis = {
            # Harmonic rhythm (chord change frequency)
            'harmonic_rhythm': max(4, int(gc_content * 16)),  # 4-16 beats per chord
            
            # Texture density (number of active voices)
            'texture_density': complexity,
            
            # Melodic activity (frequency of melodic events)
            'melodic_activity': stats['purine_content'],
            
            # Phrase lengths based on ORFs
            'phrase_lengths': [orf[2] for orf in stats['orfs'][:8]],
            
            # Dynamic range (volume variation)
            'dynamic_range': 1.0 - repetitive_score,
            
            # Tempo modifier
            'tempo_modifier': 0.8 + (gc_content * 0.4),  # 0.8-1.2 multiplier
            
            # Modal character (which mode fits best)
            'modal_suggestion': SequenceAnalyzer._suggest_musical_mode(stats),
            
            # Original stats for reference
            **stats
        }
        
        return musical_analysis
    
    @staticmethod
    def _suggest_musical_mode(stats: Dict) -> str:
        """Suggest the most appropriate musical mode based on sequence characteristics"""
        gc_content = stats['gc_content']
        complexity = stats['complexity']
        repetitive_score = stats['repetitive_score']
        
        # High GC content + high complexity = bright modes
        if gc_content > 0.6 and complexity > 0.7:
            return 'lydian'  # Bright, ethereal
        
        # Low GC content + low complexity = dark modes  
        elif gc_content < 0.4 and complexity < 0.3:
            return 'phrygian'  # Dark, mysterious
        
        # High repetition = stable modes
        elif repetitive_score > 0.5:
            return 'ionian'  # Stable major
        
        # Moderate GC, high complexity = exotic modes
        elif complexity > 0.6:
            return 'locrian'  # Unstable, otherworldly
        
        # Balanced characteristics = balanced modes
        elif 0.4 <= gc_content <= 0.6:
            return 'dorian'  # Balanced minor
        
        # Default to mixolydian for warm, grounded feel
        else:
            return 'mixolydian'


if __name__ == "__main__":
    # Example usage
    test_sequence = "ATGGCATCGATCGATCGATCGATCGATCGATCGATCGATCGTAA"
    stats = SequenceAnalyzer.calculate_statistics(test_sequence)
    musical = SequenceAnalyzer.analyze_for_musical_structure(test_sequence)
    
    print("Sequence Analysis:")
    print(f"Length: {stats['length']} bp")
    print(f"GC Content: {stats['gc_content']:.1%}")
    print(f"Complexity: {stats['complexity']:.2f}")
    print(f"ORFs found: {len(stats['orfs'])}")
    print(f"\nMusical Parameters:")
    print(f"Suggested mode: {musical['modal_suggestion']}")
    print(f"Harmonic rhythm: {musical['harmonic_rhythm']} beats")
    print(f"Texture density: {musical['texture_density']:.2f}")
    print(f"Melodic activity: {musical['melodic_activity']:.2f}")