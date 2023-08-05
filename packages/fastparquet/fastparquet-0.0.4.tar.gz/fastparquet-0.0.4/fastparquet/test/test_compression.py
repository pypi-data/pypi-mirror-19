from fastparquet.compression import (compress_data, decompress_data,
        compressions, decompressions)

import pytest


@pytest.mark.parametrize('fmt', compressions)
def test_compress_decompress_roundtrip(fmt):
    data = b'123' * 1000
    compressed = compress_data(data, algorithm=fmt)
    if fmt.lower() == 'uncompressed':
        assert compressed is data
    else:
        assert len(compressed) < len(data)

    decompressed = decompress_data(compressed, algorithm=fmt)
    assert data == decompressed


def test_errors():
    with pytest.raises(RuntimeError) as e:
        compress_data(b'123', algorithm='not-an-algorithm')

    assert 'not-an-algorithm' in str(e)
    assert 'gzip' in str(e).lower()
