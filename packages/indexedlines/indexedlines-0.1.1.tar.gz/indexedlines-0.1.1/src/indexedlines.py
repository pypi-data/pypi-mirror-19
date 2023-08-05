
import logging
import openfile
import os.path


logger = logging.getLogger(__name__)


__version__ = "0.1.1"


class IndexedLines:
    """
    IndexedLines implements a list-like immutable view over lines of text files

    It allows access to any line given it's zero-based index.
    Thus, if you have a big text file and you want to get line number 100001,
    you don't have to read the first 100000 sentences before getting that one.
    """

    def __init__(self, fname, suf=".idx.gz"):
        self.fname = fname
        self.suf = suf
        self.f = openfile.openfile(fname)
        try:
            self.load_line_offs()
        except (FileNotFoundError, OffsetsAreOutdated):
            self.compute_line_offs()
            self.save_line_offs()

    def compute_line_offs(self):
        logger.info("computing line offsets for %s", self.fname)
        self.lineoffs = [0]
        self.f.seek(0)
        while self.f.readline():
            self.lineoffs.append(self.f.tell())
        # del self.lineoffs[-1]

    def save_line_offs(self):
        logger.info("saving line offsets to %s%s", self.fname, self.suf)
        with openfile.openfile(self.fname + self.suf, "wt") as f:
            for off in self.lineoffs:
                print(off, file=f)
        logger.info("saved line offsets to %s%s", self.fname, self.suf)

    def load_line_offs(self):
        offs_fname = self.fname + self.suf
        if os.path.getmtime(self.fname) > os.path.getmtime(offs_fname):
            raise OffsetsAreOutdated
        with openfile.openfile(offs_fname) as f:
            logger.info("loading line offsets from %s", offs_fname)
            self.lineoffs = list(map(int, f))
            logger.info("loaded line offsets to %s", offs_fname)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()
        self.f = None
        self.lineoffs = None

    def __getitem__(self, i):
        self.f.seek(self.lineoffs[i])
        return self.f.readline()

    def __len__(self):
        return len(self.lineoffs) - 1

    def __iter__(self):
        return IndexedLinesIterator(self)


class IndexedLinesIterator:
    def __init__(self, idx):
        self.idx = idx
        self.i = 0

    def __next__(self):
        if self.i == len(self.idx):
            raise StopIteration
        value = self.idx[self.i]
        self.i += 1
        return value

    def __iter__(self):  # pragma: no cover
        return self


class OffsetsAreOutdated(Exception):
    pass
