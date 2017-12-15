import click
import json
import codecs
import os
from stat import *

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.environ['HOME']
if HOME_DIR:
    FOLDER = os.path.join(HOME_DIR, '.cdlimpatool')
else:
    FOLDER = os.path.join(ROOT_DIR, '.cdlimpatool')
JSON_PATH = os.path.join(FOLDER, 'annotated_morph_dict.json')


def load_annotations(infile, verbose=False):
    if verbose:
        click.echo('Loading annotations from {0}.'.format(infile))
    try:
        with codecs.open(infile, 'r', 'utf-8') as jsonfile:
            loaded_dict = json.load(jsonfile)
    except IOError:
        click.echo('First time usage : creating annotation json dictionary file as {0}.'.format(infile))
        if not os.path.exists(FOLDER):
            os.makedirs(FOLDER)
        store_annotations(infile, {}, verbose)
        with codecs.open(infile, 'r', 'utf-8') as jsonfile:
            loaded_dict = json.load(jsonfile)
    return loaded_dict


def store_annotations(outfile, loaded_dict, verbose=False):
    if verbose:
        click.echo('Storing annotations in {0}.'.format(outfile))
    with codecs.open(outfile, 'w', 'utf-8') as jsonfile:
        json.dump(loaded_dict, jsonfile, indent=2)


def line_process(line, loaded_dict):
    line = line.strip()
    if line[0] != '#':
        line_splitted = line.split('\t')
        if len(line_splitted) >= 2:
            form = line_splitted[1]
            if form not in loaded_dict:
                loaded_dict[form] = []
            if len(line_splitted) > 2:
                loaded_dict[form].append(line_splitted[2:])
            elif len(loaded_dict[form]) >= 1:
                line_next = loaded_dict[form][0]
                line_splitted += line_next
                line = '\t'.join(line_splitted)
    return line + '\n'


def file_process(infile, verbose=False, no_output=False):
    loaded_dict = load_annotations(JSON_PATH, verbose)
    outfolder = os.path.join(os.path.dirname(infile), 'output')
    if not no_output and not os.path.exists(outfolder):
        os.makedirs(outfolder)
    outfile_name = os.path.join(outfolder, os.path.basename(infile))
    if verbose and not no_output:
        click.echo('Writing in {0}.'.format(outfile_name))
    with codecs.open(infile, 'r', 'utf-8') as f:
        lines = f.readlines()
        with codecs.open(outfile_name, 'w+', 'utf-8') as f1:
            for line in lines:
                line = line_process(line, loaded_dict)
                if not no_output:
                    try:
                        f1.writelines(line)
                    except Exception:
                        click.echo('Could not write the following line. {0}.'.format(line))
    store_annotations(JSON_PATH, loaded_dict, verbose)


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
