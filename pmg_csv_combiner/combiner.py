import csv
import io
import os
from contextlib import ExitStack
from typing import Iterator


CSV_COLUMN_FILENAME = "filename"


class _InternalBuffer:
    '''
    Buffer to retrieve CSV writer rows.
    Each call to `write` overwrites the current content.
    '''

    def __init__(self) -> None:
        self._data: str = ""

    def write(self, s: str, /) -> int:
        self._data = s
        return len(s)

    @property
    def data(self) -> str:
        return self._data


def combine(*fds: io.TextIOWrapper) -> Iterator[str]:
    '''
    Combines CSV files.
    The function returns a generator in which each value corresponds to a row.
    Each input must be an object which supports the iterator protocol.
    '''
    readers = [csv.DictReader(fd, doublequote=False, escapechar='\\') for fd in fds]

    columns: list[str] = []
    for reader in readers:
        if reader.fieldnames is not None:
            columns += reader.fieldnames
    columns = list(dict.fromkeys(columns))
    columns.append(CSV_COLUMN_FILENAME)

    output = _InternalBuffer()
    writer = csv.DictWriter(
        output,
        fieldnames=columns,
        restval='',
        doublequote=False,
        escapechar='\\', 
        quoting=csv.QUOTE_ALL,
        lineterminator='',
    )
    writer.writeheader()
    yield output.data

    for fd, reader in zip(fds, readers):
        for row in reader:
            row[CSV_COLUMN_FILENAME] = os.path.basename(fd.name)
            writer.writerow(row)
            yield output.data


def combine_files(srcs: Iterator[str]) -> Iterator[str]:
    '''
    Wrapper for `combine` to handle file names input.
    '''
    with ExitStack() as stack:
        fds = [stack.enter_context(open(src, newline='')) for src in srcs]
        for line in combine(*fds):
            yield line