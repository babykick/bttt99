import click

from .core import search, find_subtitle
from .common import copy_to_clipboard


@click.command()
@click.argument('moviename', required=False)
@click.option('--subtitle', '-s', help='Given keyword(usually the file name) to search')
def main(moviename, subtitle):
    if moviename:
        search(moviename)
    elif subtitle:
        link = find_subtitle(subtitle)
        print(link)
        copy_to_clipboard(link)
        print('Subtitle download link copied')


if __name__ == "__main__":
    main()
