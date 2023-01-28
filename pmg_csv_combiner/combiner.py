import csv
import io
import os
from contextlib import ExitStack
from typing import Iterator


CSV_COLUMN_FILENAME = "filename"


class _InternalBuffer:
    def __init__(self) -> None:
        self._data: str = ""

    def write(self, s: str, /) -> int:
        self._data = s
        return len(s)

    @property
    def data(self) -> str:
        return self._data


def combine(*fds: io.TextIOWrapper) -> Iterator[str]:
    readers = [csv.DictReader(fd, doublequote=False, escapechar='\\') for fd in fds]

    columns: list[str] = []
    for reader in readers:
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
    with ExitStack() as stack:
        fds = [stack.enter_context(open(src, newline='')) for src in srcs]
        for line in combine(*fds):
            yield line