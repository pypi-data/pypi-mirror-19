import click
import sys
import validators
import urllib
import os.path
from bs4 import BeautifulSoup

@click.command()
@click.argument('url', type=click.STRING, required=True)
@click.argument('out', type=click.Path(), default=None, required=False)
def imgdl(url, out):
    """This script greets you"""
    provider = url_parser(url)

    if (provider == 'IMGUR'):
        imgur_processor(url, out)

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

def imgur_processor(url, out):
    imgur_log_text = click.style('[imgur]', fg='blue')
    url_parts = url.split('/')
    # populate variables
    is_album = 'a' in url_parts or 'gallery' in url_parts
    key = url_parts[-1]

    click.echo('%s is_abum: %s, key: %s' % (imgur_log_text, is_album, key))

    try:
        click.echo('%s Downloading webpage' % imgur_log_text)

        filename = out if out else key
        if (is_album):
            #soup = BeautifulSoup(r.read(), 'html.parser')
            click.echo(click.style('[imgdl] Downloading album is still under development. Exiting', fg='yellow'))
            #print(soup.prettify())
            sys.exit(1)
        else:
            if os.path.isfile(filename):
                click.echo(click.style('[imgdl] File already exits. Exiting', fg='green'))
            else:
                urllib.urlretrieve(url, filename)
                click.echo(click.style('[imgdl] Download success. Location: %s' % filename, fg='green'))

    except urllib2.HTTPError:
        click.echo(click.style('[imgur] Webpage not found', fg='red'))
        sys.exit(1)
