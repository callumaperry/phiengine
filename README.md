# PHI Engine - Examples

This directory contains working examples demonstrating the PHI Engine's capabilities.

## Quick Start

```bash
# Run any example directly
python examples/example_embeddings_phase1.py
python examples/example_embeddings_phase2.py
python examples/example_text_compression.py
```

## Examples Overview

### 1. `example_embeddings_phase1.py`
**Production-grade embeddings compression**

- Demonstrates Phase-1 compression (6-19× ratios)
- Tests three presets: phi-analytics, phi-balanced, phi-max
- Shows quality metrics (cosine similarity)
- **Use case:** Production serving, real-time retrieval

**Expected output:**
- phi-analytics: 5.9× @ 0.993+ cosine
- phi-balanced: 6.4× @ 0.992+ cosine  
- phi-max: 18.7× @ 0.987+ cosine

---

### 2. `example_embeddings_phase2.py`
**Ultra-compression for archival**

- Demonstrates Phase-2 compression (90-124× ratios)
- Tests PQ presets: phi-pq-quality, phi-pq-balanced
- Shows extreme storage savings (99%+)
- **Use case:** Cold storage, archival, backup compression

**Expected output:**
- phi-pq-quality: 93.9× @ 0.905+ cosine
- phi-pq-balanced: 124.4× @ 0.906+ cosine

**Note:** Phase-2 compression takes 10-30 seconds due to PQ codebook learning.

---

### 3. `example_text_compression.py`
**Lossless text compression**

- Demonstrates 100% lossless text compression
- Tests multiple text types: logs, JSON, code, markdown
- Verifies perfect reconstruction
- **Use case:** Log archival, JSON storage, code compression

**Expected output:**
- 13-24× compression ratios
- 100% perfect reconstruction (lossless)

---

## Running tests
```bash
source venv/bin/activate && python -m pytest test -v
```

---

## Running the Examples

### Requirements
```bash
pip install numpy
```

### Run Phase-1 Demo
```bash
python examples/example_embeddings_phase1.py
```

Sample output:
```
======================================================================
PHI ENGINE - Phase-1 Embeddings Compression Demo
======================================================================

📊 Generating 10,000 synthetic embeddings (1536-D)...
Original size: 61.44 MB

🔧 Testing preset: phi-balanced
--------------------------------------------------
✅ Compression ratio: 6.40×
✅ Compressed size: 9.60 MB
✅ Avg cosine similarity: 0.9925
✅ Min cosine similarity: 0.9811
✅ Quality: VERY GOOD (production-ready)
```

---

## Integration Examples

### Example 1: RAG System Integration
```python
from phi_engine import compress, decompress
import numpy as np

# Generate embeddings from documents
embeddings = generate_embeddings(documents)  # Your embedding function

# Compress for storage
compressed = compress(embeddings, preset="phi-balanced")

# Save to database/file
save_to_storage(compressed)

# Later: retrieve and decompress
compressed = load_from_storage()
embeddings = decompress(compressed)

# Use for similarity search
results = semantic_search(query_embedding, embeddings)
```

### Example 2: Vector Database Optimization
```python
from phi_engine import compress, decompress
import pinecone  # or weaviate, qdrant, etc.

# Before: store raw embeddings (61 MB for 10K vectors)
index.upsert(vectors=embeddings)

# After: compress first (9.6 MB for 10K vectors = 6.4× savings)
compressed = compress(embeddings, preset="phi-balanced")
index.upsert(vectors=compressed, metadata={"compressed": True})

# On retrieval: decompress
results = index.query(query_vector, top_k=10)
if results['metadata']['compressed']:
    results['vectors'] = decompress(results['vectors'])
```

### Example 3: Batch Processing Pipeline
```python
from phi_engine import compress, decompress
import glob

# Process all embedding files in a directory
for filepath in glob.glob("embeddings/*.npy"):
    # Load embeddings
    embeddings = np.load(filepath)
    
    # Compress
    compressed = compress(embeddings, preset="phi-balanced")
    
    # Save with .phz extension
    output_path = filepath.replace('.npy', '.phz')
    with open(output_path, 'wb') as f:
        f.write(compressed)
    
    print(f"{filepath}: {embeddings.nbytes / len(compressed):.1f}× compression")
```

---

## Performance Benchmarks

Based on 100K vector validation:

| Preset | Ratio | Avg Cosine | Min Cosine | Speed | Use Case |
|--------|-------|------------|------------|-------|----------|
| **Phase-1** |  |  |  |  |  |
| phi-analytics | 5.9× | 0.9937 | 0.9831 | 6.4s | Production |
| phi-balanced | 6.4× | 0.9925 | 0.9811 | 7.3s | Default |
| phi-max | 18.7× | 0.9873 | 0.9714 | 15.6s | Aggressive |
| **Phase-2** |  |  |  |  |  |
| phi-pq-quality | 93.9× | 0.9058 | 0.8422 | 370s | Archival |
| phi-pq-balanced | 124.4× | 0.9068 | 0.8523 | 224s | Extreme |

**Dataset:** 100,000 × 1,536 embeddings (600 MB)

## Validation & Test Suite

- ✅ Synthetic OpenAI-style embeddings (6 datasets, 15 presets) — see `OPENAI_SIMULATION_RESULTS.md`
- ✅ Real Kaggle OpenFWI geophysical data (46 files, up to 350K vectors) — see `REAL_DATA_ANALYSIS.md` and `REAL_DATA_SUMMARY.txt`
- ✅ Full system test summary — 19/19 checks passed, production-ready (see `TEST_SUMMARY.txt` and `TEST_REVIEW.md`)
- ✅ Initial test suite contributed by **@jsdevtom** — 100% pass on lossless text/JSON/Unicode compression.

### Large-Scale Vector Validation

📌 **Validated on 50K, 100K, 150K, 250K, and 350K real-world vectors**

- **Source:** Kaggle OpenFWI scientific geophysical datasets
- **Results:** 29×–62× compression, 52–55 dB PSNR, cosine 0.93–0.99
- **Significance:** These tests demonstrate PHI Engine's ability to operate at near-million-scale vector workloads without degradation.

## 🔬 Validation Highlights (Read First)

Across synthetic, OpenAI-style, and real Kaggle datasets, PHI Engine has been validated at scale.

**Observed results:**
- Phase-1 (Production): 6× – 20× compression @ 0.98–0.994 cosine
- Phase-2 (Archival): 90× – 124× typical
- **Phase-2 (Extreme cases): up to 204× compression**
- **Total vectors tested across datasets: ~350,000+**

Extreme ratios occur under specific archival configurations and are documented in:
- LARGE_SCALE_VALIDATION_UPDATES.md
- BENCHMARKS.md
- REAL_DATA_ANALYSIS.md

These results exceed standard FAISS PQ baselines under comparable quality constraints.

---

## Next Steps

1. **Try the examples** - Run the demo scripts to see the engine in action
2. **Read the docs** - Check `docs/` for detailed technical information
3. **Review benchmarks** - See `benchmarks/` for validation results
4. **Integrate** - Use the patterns above in your own projects

## Patent & IP Status

PHI Engine's core golden-ratio-optimised multimodal compression method is covered by:

- **UK Patent Application GB2520758.0**  
  *"Methods and Systems for Golden-Ratio-Optimised Multimodal Data Compression"*.

This repository represents the reference implementation of the patented system.

## Support

- Technical details: See `docs/TECHNICAL_SUMMARY.md`
- Integration guide: See `docs/INTEGRATION_GUIDE.md`
- Full API: See main `README.md`

⚠️ Patent Pending (UK application filed Dec 2025)

This repository contains:
• The PHI Engine core implementation
• Reproducible benchmarks and validation
• A consolidated acquisition / diligence pack

Start here:
→ START_HERE.md
→ ACQUISITION_PACK_README.md
