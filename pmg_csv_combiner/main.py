import csv
import os
import sys
from contextlib import ExitStack

import click


CSV_COLUMN_FILENAME = "filename"


def combine(srcs: tuple[str]) -> None:
    with ExitStack() as stack:
        fds = [stack.enter_context(open(src, newline='')) for src in srcs]
        readers = [csv.DictReader(fd, doublequote=False, escapechar='\\') for fd in fds]

        columns = []
        for reader in readers:
            columns += reader.fieldnames
        columns = list(dict.fromkeys(columns))
        columns.append(CSV_COLUMN_FILENAME)

        writer = csv.DictWriter(
            sys.stdout,
            fieldnames=columns,
            restval='',
            doublequote=False,
            escapechar='\\', 
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()

        for src, reader in zip(srcs, readers):
            for row in reader:
                row[CSV_COLUMN_FILENAME] = os.path.basename(src)
                writer.writerow(row)


@click.command()
@click.argument("srcs", nargs=-1)
def main(srcs: tuple[str]) -> None:
    combine(srcs)


if __name__ == "__main__":
    main()