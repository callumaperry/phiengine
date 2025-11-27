"""
Example: Phase-2 Embeddings Compression (Ultra-Compression Mode)

Demonstrates extreme compression for archival/cold storage.
Expected: 90-124× compression @ 0.90+ cosine similarity
"""

import numpy as np
from phi_engine import compress, decompress

def main():
    print("=" * 70)
    print("PHI ENGINE - Phase-2 Embeddings Compression Demo")
    print("=" * 70)
    
    # Generate synthetic embeddings
    n_vectors = 10_000
    dims = 1536
    print(f"\n📊 Generating {n_vectors:,} synthetic embeddings ({dims}-D)...")
    X = np.random.randn(n_vectors, dims).astype(np.float32)
    
    # L2 normalize
    X = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-8)
    
    print(f"Original size: {X.nbytes / 1e6:.2f} MB")
    
    # Test Phase-2 presets
    presets = ["phi-pq-quality", "phi-pq-balanced"]
    
    for preset in presets:
        print(f"\n🔧 Testing preset: {preset}")
        print("-" * 50)
        
        # Compress (this takes longer due to PQ codebook learning)
        print("⏳ Compressing (PQ codebook learning may take 10-30 seconds)...")
        compressed = compress(X, preset=preset, filename="demo_embeddings.npy")
        
        # Decompress
        print("⏳ Decompressing...")
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
        
        # Storage savings
        savings_pct = (1 - 1/ratio) * 100
        print(f"✅ Storage savings: {savings_pct:.1f}%")
        
        # Quality assessment
        if avg_cos >= 0.95:
            quality = "EXCELLENT (retrieval-safe)"
        elif avg_cos >= 0.90:
            quality = "VERY GOOD (archival-ready)"
        elif avg_cos >= 0.85:
            quality = "GOOD (cold storage)"
        else:
            quality = "MODERATE (deep archival only)"
        
        print(f"✅ Quality: {quality}")
    
    print("\n" + "=" * 70)
    print("✅ Phase-2 Demo Complete!")
    print("=" * 70)
    print("\n💡 Use Cases:")
    print("   - Cold storage / archival of old embeddings")
    print("   - Reducing cloud storage costs by 99%+")
    print("   - Backup compression before deletion")
    print("\n⚠️  Note: Phase-2 is slower to compress (codebook learning)")
    print("   but decompression is fast (~2 seconds for 100K vectors)")

if __name__ == "__main__":
    main()
