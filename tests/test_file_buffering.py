from paramiko.file import BufferedFile


class PrefilledBufferedFile(BufferedFile):
    def __init__(self, data):
        super().__init__()
        self._flags = self.FLAG_READ | self.FLAG_BINARY
        self._rbuffer = data

    def _read(self, size):
        return bytes()


def test_small_reads_reuse_unread_backing_buffer():
    data = b"abcdefgh"
    f = PrefilledBufferedFile(data)

    assert f.read(1) == b"a"
    assert isinstance(f._rbuffer, memoryview)
    assert f._rbuffer.obj is data
    assert bytes(f._rbuffer) == b"bcdefgh"

    assert f.read(1) == b"b"
    assert isinstance(f._rbuffer, memoryview)
    assert f._rbuffer.obj is data
    assert bytes(f._rbuffer) == b"cdefgh"


def test_readline_after_small_buffered_read():
    f = PrefilledBufferedFile(b"abc\ndef")

    assert f.read(1) == b"a"
    assert f.readline() == b"bc\n"
    assert f.readline() == b"def"
