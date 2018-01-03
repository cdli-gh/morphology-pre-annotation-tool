import os

import click
from stat import ST_MODE, S_ISREG

from cdli_mpa_tool.annotate import file_process


#def check_format(infile, verbose=False):

def check_and_process(pathname, verbose=False, no_output=False):
    mode = os.stat(pathname)[ST_MODE]
    if S_ISREG(mode) and pathname.lower().endswith('.conll'):
        # It's a file, call the callback function
        if verbose:
            click.echo('Processing {0}.'.format(pathname))
        file_process(pathname, verbose, no_output)


@click.command()
@click.option('--input_path', '-i', type=click.Path(exists=True, writable=True), prompt=True, required=True,
              help='Input the file/folder name.')
@click.option('--no_output', '-n', default=False, required=False, is_flag=True,
              help='Disables output for filling dictionary only')
@click.option('-v', '--verbose', default=False, required=False, is_flag=True, help='Enables verbose mode')
@click.version_option()
def main(input_path, no_output, verbose):
    """My Tool does one thing, and one thing well."""
    if os.path.isdir(input_path):
        with click.progressbar(os.listdir(input_path), label='Annotating the files') as bar:
            for f in bar:
                pathname = os.path.join(input_path, f)
                check_and_process(pathname, verbose, no_output)
    else:
        check_and_process(input_path, verbose, no_output)
