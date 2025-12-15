# PHI Engine v3.1.5 - Quick Start Guide

**⚡ Get started in under 5 minutes**

---

## 1️⃣ Installation (Choose One)

### Option A: Drop-in (Fastest - Recommended)

```bash
# Just copy the engine file to your project
cp phi_engine/phi_engine_master.py ./your_project/

# Done! No pip, no dependencies issues
```

### Option B: Package Install

```bash
# Install from this directory
pip install -e .

# Or just install numpy
pip install numpy
```

---

## 2️⃣ Basic Usage

### Embeddings (Phase-1 - Production)

```python
import numpy as np
from phi_engine import compress, decompress

# Your embeddings (e.g., from OpenAI)
embeddings = np.random.randn(10000, 1536).astype(np.float32)

# Compress (6× ratio, 0.99 quality)
compressed = compress(embeddings, preset="phi-balanced")

# Decompress
restored = decompress(compressed)

# Verify quality
cosine_sim = np.sum(embeddings * restored, axis=1)
print(f"Average cosine similarity: {cosine_sim.mean():.4f}")
# Output: 0.9925+
```

### Text (Lossless)

```python
from phi_engine import compress, decompress

# Your text data
text = b"Your log data or JSON..." * 100

# Compress (13-24× lossless)
compressed = compress(text, preset="phi-global")

# Decompress
restored = decompress(compressed)

# Verify perfect
assert text == restored  # ✅ 100% lossless
```

### Embeddings (Phase-2 - Ultra Compression)

```python
from phi_engine import compress, decompress

# Large embedding dataset
embeddings = np.load('embeddings_1M.npy')

# Ultra-compress (124× ratio, 0.90 quality)
compressed = compress(embeddings, preset="phi-pq-balanced")

# Saves 99%+ storage!
ratio = embeddings.nbytes / len(compressed)
print(f"Compression: {ratio:.1f}×")
# Output: 124.4×
```

---

## 3️⃣ Run Examples

```bash
# Phase-1 demo (6-19× compression)
python examples/example_embeddings_phase1.py

# Phase-2 demo (94-124× compression)
python examples/example_embeddings_phase2.py

# Text demo (13-24× lossless)
python examples/example_text_compression.py
```

Each example runs in ~30 seconds and shows:
- Compression ratios
- Quality metrics
- Use cases

---

## 4️⃣ Preset Guide

### Phase-1 (Fast, Production-Ready)

| Preset | Ratio | Quality | Speed | Use When |
|--------|-------|---------|-------|----------|
| `phi-analytics` | 5.9× | 0.9937 | Fast | Need best quality |
| `phi-balanced` | 6.4× | 0.9925 | Fast | **Default choice** |
| `phi-max` | 18.7× | 0.9873 | Medium | Need more compression |

### Phase-2 (Slower, Maximum Compression)

| Preset | Ratio | Quality | Speed | Use When |
|--------|-------|---------|-------|----------|
| `phi-pq-quality` | 93.9× | 0.9058 | Slow | Archival + quality |
| `phi-pq-balanced` | 124.4× | 0.9068 | Slow | **Maximum savings** |

### Specialized

| Preset | Use Case | Performance |
|--------|----------|-------------|
| `phi-global` | Text only | 13-24× lossless |
| `phi-live` | Timeseries | 5× @ 50dB PSNR |

---

## 5️⃣ Integration Patterns

### RAG System

```python
from phi_engine import compress, decompress

# During indexing (one-time)
docs = ["doc1", "doc2", ...]
embeddings = model.encode(docs)
compressed = compress(embeddings, preset="phi-balanced")

# Save compressed
with open('embeddings.phz', 'wb') as f:
    f.write(compressed)

# During search (many times)
with open('embeddings.phz', 'rb') as f:
    compressed = f.read()

embeddings = decompress(compressed)  # Fast!
results = similarity_search(query, embeddings)
```

### Vector Database

```python
from phi_engine import compress, decompress

# Before: 61 MB for 10K vectors
vectors = get_embeddings(documents)

# After: 9.6 MB (6.4× smaller)
compressed = compress(vectors, preset="phi-balanced")

# Store compressed
db.store(compressed, metadata={'compressed': True})

# Retrieve and decompress
compressed = db.retrieve(doc_id)
vectors = decompress(compressed)
```

### Batch Processing

```python
import glob
from phi_engine import compress

# Process all embeddings in a directory
for file in glob.glob("embeddings/*.npy"):
    data = np.load(file)
    compressed = compress(data, preset="phi-balanced")
    
    # Save with .phz extension
    output = file.replace('.npy', '.phz')
    with open(output, 'wb') as f:
        f.write(compressed)
```

---

## 6️⃣ Troubleshooting

### Q: Low compression ratios?

**A:** Ensure data has structure:
- Embeddings should be L2 normalized
- Text should be UTF-8
- Random/encrypted data compresses poorly

```python
# Normalize embeddings
embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
```

### Q: Quality too low?

**A:** Use higher-quality presets:
- Phase-1: `phi-analytics` (0.9937 quality)
- Phase-2: `phi-pq-quality` (0.9058 quality)

### Q: Out of memory?

**A:** Process in batches:

```python
# Instead of compressing 10M at once
for i in range(0, len(big_data), 100000):
    batch = big_data[i:i+100000]
    compressed = compress(batch)
    save(compressed)
```

### Q: Compression too slow?

**A:** Use Phase-1 instead of Phase-2:
- Phase-1: 6-16s for 100K vectors
- Phase-2: 4-6min for 100K vectors (k-means)

---

## 7️⃣ CLI Usage

```bash
# Test engine
python phi_engine/phi_engine_master.py test

# Compress file
python phi_engine/phi_engine_master.py compress input.npy output.phz phi-balanced

# Decompress file
python phi_engine/phi_engine_master.py decompress output.phz restored.npy

# Show presets
python phi_engine/phi_engine_master.py presets
```

---

## 8️⃣ Next Steps

### For Evaluation
1. ✅ Run examples (see section 3)
2. ✅ Test on your data
3. ✅ Check quality metrics
4. ✅ Review `docs/BENCHMARKS.md`

### For Integration
1. ✅ Choose preset (see section 4)
2. ✅ Adapt integration pattern (see section 5)
3. ✅ Deploy to test environment
4. ✅ Monitor performance

### For Deep Dive
1. ✅ Read `docs/TECHNICAL_SUMMARY.md`
2. ✅ Review `docs/REAL_DATA_ANALYSIS.md`
3. ✅ Check `docs/TEST_REVIEW.md`
4. ✅ Explore source code

---

## ✅ Success Checklist

After following this guide, you should have:

- [x] Engine installed (drop-in or pip)
- [x] Run at least one example
- [x] Tested compression on sample data
- [x] Verified quality metrics
- [x] Understood preset options
- [x] Ready to integrate

**Time to complete:** ~5-10 minutes

---

## 🎯 Common Use Cases

### OpenAI Embeddings
```python
# Compress OpenAI embeddings
import openai
from phi_engine import compress

response = openai.Embedding.create(
    input=["Hello world"], 
    model="text-embedding-ada-002"
)
embedding = np.array(response['data'][0]['embedding'])
compressed = compress(embedding, preset="phi-analytics")
```

### Vector Search
```python
# Compress vector database
from phi_engine import compress, decompress

# Index time: compress and store
compressed_db = compress(all_vectors, preset="phi-balanced")
save_to_disk(compressed_db)

# Search time: decompress and search
vectors = decompress(compressed_db)
results = faiss_search(query_vector, vectors, k=10)
```

### Log Archival
```python
# Compress logs losslessly
from phi_engine import compress

logs = read_log_file('app.log')
compressed = compress(logs.encode(), preset="phi-global")

# Saves 13-24× space, 100% lossless
```

---

## 📞 Need Help?

- **Examples not working?** Check Python 3.7+ and NumPy installed
- **Quality issues?** Try `phi-analytics` preset
- **Integration questions?** See `docs/PACKAGE_MANIFEST.md`
- **Performance tuning?** See `docs/BENCHMARKS.md`

---

**You're ready to start!** 🚀

Choose your path:
1. **Quick test:** Run examples (section 3)
2. **Production:** Use `phi-balanced` preset (section 2)
3. **Maximum compression:** Use `phi-pq-balanced` (section 2)

---

**PHI Engine v3.1.5** | Production Ready | Patent Pending
