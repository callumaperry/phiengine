"""
PHI Engine v3.1.5 - Universal Compression for AI Embeddings, Text & Scientific Data

Enterprise-grade compression system using golden ratio (φ) mathematics.
Validated on synthetic OpenAI-style embeddings, real Kaggle OpenFWI data, and mixed workloads
with world-leading 6–124× compression ratios.

Patent pending: UK Patent Application GB2520758.0

Usage:
    from phi_engine import compress, decompress
    
    compressed = compress(data, preset="phi-balanced")
    restored = decompress(compressed)
"""

from .phi_engine_master import compress, decompress, PRESETS

__version__ = "3.1.5"
__all__ = ["compress", "decompress", "PRESETS", "__version__"]
