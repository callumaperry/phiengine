from phi_engine_master import compress, decompress


class TestTextCompression:
    """Test text/bytes compression."""

    def test_compress_decompress_simple_text(self):
        """Text compression should be lossless."""
        original = b"Hello, World!"
        compressed = compress(original, preset="phi-global")
        restored = decompress(compressed)

        assert original == restored
        assert len(compressed) < len(original)

    def test_compress_decompress_repetitive_text(self):
        """Repetitive text should achieve high compression ratios."""
        original = b"Hello, World!" * 100
        compressed = compress(original, preset="phi-global")
        restored = decompress(compressed)

        assert original == restored
        ratio = len(original) / len(compressed)
        assert ratio > 5, f"Expected >5× compression, got {ratio:.2f}×"

    def test_compress_decompress_long_text(self):
        """Long realistic text should achieve good compression ratios."""
        import os

        # Load realistic text sample
        test_dir = os.path.dirname(__file__)
        with open(os.path.join(test_dir, 'sample_text.txt'), 'rb') as f:
            original = f.read()

        compressed = compress(original, preset="phi-global")
        restored = decompress(compressed)

        assert original == restored
        ratio = len(original) / len(compressed)
        assert ratio > 2, f"Expected >2× compression on long text, got {ratio:.2f}×"

    def test_compress_decompress_json(self):
        """JSON data should compress losslessly."""
        original = b'{"key": "value", "number": 123}' * 50
        compressed = compress(original, preset="phi-global")
        restored = decompress(compressed)

        assert original == restored

    def test_empty_bytes(self):
        """Empty bytes should be handled gracefully."""
        original = b""
        # May raise or return minimal compressed form
        # At minimum, should not crash
        try:
            compressed = compress(original, preset="phi-global")
            restored = decompress(compressed)
            assert original == restored or len(restored) == 0
        except (ValueError, IndexError):
            # Acceptable to reject empty input
            pass

    def test_single_byte(self):
        """Single byte should be handled."""
        original = b"A"
        compressed = compress(original, preset="phi-global")
        restored = decompress(compressed)

        assert original == restored

    def test_unicode_text(self):
        """Unicode text should compress correctly."""
        text = "Hello 世界 🌍" * 100
        original = text.encode('utf-8')
        compressed = compress(original, preset="phi-global")
        restored = decompress(compressed)

        assert original == restored
        assert restored.decode('utf-8') == text
