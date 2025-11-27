"""
Example: Phase-1 Embeddings Compression (Production Mode)

Demonstrates high-fidelity compression suitable for production serving.
Expected: 6-19× compression @ 0.98-0.99 cosine similarity
"""

import numpy as np
from phi_engine import compress, decompress

def main():
    print("=" * 70)
    print("PHI ENGINE - Phase-1 Embeddings Compression Demo")
    print("=" * 70)
    
    # Generate synthetic embeddings (1536-D like OpenAI ada-002)
    n_vectors = 10_000
    dims = 1536
    print(f"\n📊 Generating {n_vectors:,} synthetic embeddings ({dims}-D)...")
    X = np.random.randn(n_vectors, dims).astype(np.float32)
    
    # L2 normalize (like real embeddings)
    X = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-8)
    
    print(f"Original size: {X.nbytes / 1e6:.2f} MB")
    
    # Test three Phase-1 presets
    presets = ["phi-analytics", "phi-balanced", "phi-max"]
    
    for preset in presets:
        print(f"\n🔧 Testing preset: {preset}")
        print("-" * 50)
        
        # Compress
        compressed = compress(X, preset=preset, filename="demo_embeddings.npy")
        
        # Decompress
        restored = decompress(compressed)
        
        # Calculate metrics
        ratio = X.nbytes / len(compressed)
        
        # Cosine similarity
        X_norm = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-8)
        R_norm = restored / (np.linalg.norm(restored, axis=1, keepdims=True) + 1e-8)
        cosines = np.sum(X_norm * R_norm, axis=1)
        
        avg_cos = cosines.mean()
        min_cos = cosines.min()
        
        print(f"✅ Compression ratio: {ratio:.2f}×")
        print(f"✅ Compressed size: {len(compressed) / 1e6:.2f} MB")
        print(f"✅ Avg cosine similarity: {avg_cos:.4f}")
        print(f"✅ Min cosine similarity: {min_cos:.4f}")
        
        # Quality assessment
        if avg_cos >= 0.99:
            quality = "EXCELLENT (near-lossless)"
        elif avg_cos >= 0.95:
            quality = "VERY GOOD (production-ready)"
        elif avg_cos >= 0.90:
            quality = "GOOD (suitable for most tasks)"
        else:
            quality = "MODERATE (archival use only)"
        
        print(f"✅ Quality: {quality}")
    
    print("\n" + "=" * 70)
    print("✅ Phase-1 Demo Complete!")
    print("=" * 70)
    print("\n💡 Recommendation:")
    print("   - Use 'phi-balanced' for production (best balance)")
    print("   - Use 'phi-analytics' for highest quality")
    print("   - Use 'phi-max' for aggressive compression")

if __name__ == "__main__":
    main()
