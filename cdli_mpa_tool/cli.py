import os

import click
from stat import ST_MODE, S_ISREG

from cdli_mpa_tool.annotate import CONLLAnnotator
from cdli_mpa_tool.checker import CONLChecker
from cdli_mpa_tool.format import CONLLFormattor


def check_and_process(pathname, no_output=False, check=False, format_conll=False, verbose=False):
    mode = os.stat(pathname)[ST_MODE]
    if S_ISREG(mode) and pathname.lower().endswith('.conll'):
        # It's a file, call the callback function
        if verbose:
            click.echo('\nInfo: Processing {0}.'.format(pathname))
        if format_conll:
            formattor = CONLLFormattor(pathname, verbose)
            formattor.process()
        elif check:
            checker = CONLChecker(pathname, verbose)
            checker.check()
        else:
            annotator = CONLLAnnotator(pathname, verbose, no_output)
            annotator.process()


def delete_dictionary(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    CONLLAnnotator.delete_folder()
    ctx.exit()


@click.command()
@click.option('--input_path', '-i', type=click.Path(exists=True, writable=True), prompt=True, required=True,
              help='Input the file/folder name.')
@click.option('--no_output', '-n', default=False, required=False, is_flag=True,
              help='Disables output for filling dictionary only')
@click.option('--delete_dict', '-d', is_flag=True, default=False, callback=delete_dictionary,
              expose_value=False, is_eager=True, help='Deletes the dictionary')
@click.option('--check', '-c', default=False, required=False, is_flag=True, help='Checks the format of the conll file.')
@click.option('--format_conll', '-f', default=False, required=False, is_flag=True,
              help='Formats the file as per requirement of Conll-U convertor.')
@click.option('--verbose', '-v', default=False, required=False, is_flag=True, help='Enables verbose mode')
@click.version_option()
def main(input_path, no_output, check, format_conll, verbose):
    """My Tool does one thing, and one thing well."""
    if os.path.isdir(input_path):
        with click.progressbar(os.listdir(input_path), label='Processing the files') as bar:
            for f in bar:
                pathname = os.path.join(input_path, f)
                check_and_process(pathname, no_output, check, format_conll, verbose)
    else:
        check_and_process(input_path, no_output, check, format_conll, verbose)
