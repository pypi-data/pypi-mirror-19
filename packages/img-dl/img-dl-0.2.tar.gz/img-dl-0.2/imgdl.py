import click
import sys
import validators

from processors.imgur_processor import ImgurProcessor

@click.command()
@click.argument('url', type=click.STRING, required=True)
@click.argument('out', type=click.Path(), default=None, required=False)
def imgdl(url, out):
    """This script greets you"""
    provider = url_parser(url)

    if (provider == 'IMGUR'):
        ImgurProcessor().process(url, out)

def url_parser(url):
    click.echo('[imgdl] Validating url...')
    is_valid = validators.url(url)

    # Exit if url is not valid
    if not is_valid:
        click.echo(click.style('[imgdl] Url is not valid. Exiting', fg='red'))
        sys.exit(1)

    url_parts = url.split('/')
    if 'imgur.com' in url_parts or 'i.imgur.com' in url_parts:
        return 'IMGUR'
    else:
        click.echo(click.style('[imgdl] Only supports imgur.com', fg='red'))
        sys.exit(1)
