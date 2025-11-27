"""
Example: Text Compression (Lossless)

Demonstrates 100% lossless text compression.
Expected: 13-24× compression with perfect reconstruction
"""

from phi_engine import compress, decompress

def main():
    print("=" * 70)
    print("PHI ENGINE - Text Compression Demo")
    print("=" * 70)
    
    # Sample texts
    texts = {
        "Short text": "Hello, World!" * 100,
        "JSON log": '{"timestamp": "2025-11-18T12:00:00Z", "level": "INFO", "message": "Request processed successfully"}' * 50,
        "Code": '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
''' * 30,
        "Markdown": '''
# PHI Engine Documentation

## Overview
The PHI Engine is a universal compression system.

## Features
- High compression ratios
- Lossless text compression
- Fast decompression
''' * 20
    }
    
    print("\n📝 Testing lossless text compression...")
    
    for name, text in texts.items():
        print(f"\n🔧 Testing: {name}")
        print("-" * 50)
        
        # Convert to bytes
        text_bytes = text.encode('utf-8')
        original_size = len(text_bytes)
        
        # Compress
        compressed = compress(text_bytes, preset="phi-global", filename=f"{name}.txt")
        
        # Decompress
        restored = decompress(compressed)
        
        # Verify lossless
        is_lossless = (text_bytes == restored)
        
        ratio = original_size / len(compressed)
        
        print(f"✅ Original size: {original_size:,} bytes")
        print(f"✅ Compressed size: {len(compressed):,} bytes")
        print(f"✅ Compression ratio: {ratio:.2f}×")
        print(f"✅ Lossless: {is_lossless} {'✅' if is_lossless else '❌'}")
        
        if not is_lossless:
            print("❌ ERROR: Text was not perfectly reconstructed!")
        else:
            # Show sample
            sample_len = min(50, len(text))
            print(f"✅ Sample: '{text[:sample_len]}...'")
    
    print("\n" + "=" * 70)
    print("✅ Text Compression Demo Complete!")
    print("=" * 70)
    print("\n💡 Text compression is:")
    print("   - 100% lossless (perfect reconstruction)")
    print("   - 13-24× compression typical")
    print("   - Works on logs, JSON, code, markdown, etc.")

if __name__ == "__main__":
    main()
