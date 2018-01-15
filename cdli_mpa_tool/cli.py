import os

import click
from stat import ST_MODE, S_ISREG

from cdli_mpa_tool.annotate import CONLLAnnotator
from cdli_mpa_tool.checker import CONLChecker


def check_and_process(pathname, no_output=False, check=False, verbose=False):
    mode = os.stat(pathname)[ST_MODE]
    if S_ISREG(mode) and pathname.lower().endswith('.conll'):
        # It's a file, call the callback function
        if verbose:
            click.echo('\nInfo: Processing {0}.'.format(pathname))
        if not check:
            annotator = CONLLAnnotator(pathname, verbose, no_output)
            annotator.process()
        checker = CONLChecker(pathname, verbose)
        checker.check()


@click.command()
@click.option('--input_path', '-i', type=click.Path(exists=True, writable=True), prompt=True, required=True,
              help='Input the file/folder name.')
@click.option('--no_output', '-n', default=False, required=False, is_flag=True,
              help='Disables output for filling dictionary only')
@click.option('--check', '-c', default=False, required=False, is_flag=True, help='Checks the format of the conll file.')
@click.option('--verbose', '-v', default=False, required=False, is_flag=True, help='Enables verbose mode')
@click.version_option()
def main(input_path, no_output, check, verbose):
    """My Tool does one thing, and one thing well."""
    if os.path.isdir(input_path):
        with click.progressbar(os.listdir(input_path), label='Processing the files') as bar:
            for f in bar:
                pathname = os.path.join(input_path, f)
                check_and_process(pathname, no_output, check, verbose)
    else:
        check_and_process(input_path, no_output, check, verbose)
