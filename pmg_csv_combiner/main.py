import click

@click.command()
@click.argument("src", nargs=-1)
@click.argument("dst", nargs=1)
def main(src: tuple[str], dst: str):
    print(src, dst)

if __name__ == "__main__":
    main()