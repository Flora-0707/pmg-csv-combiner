import click
from pmg_csv_combiner.combiner import combine_files

@click.command()
@click.argument("srcs", nargs=-1)
def main(srcs: tuple[str]) -> None:
    for line in combine_files(srcs):
        print(line)


if __name__ == "__main__":
    main()