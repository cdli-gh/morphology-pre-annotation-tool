import click
import json
import codecs
import os
from stat import *

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(ROOT_DIR, 'annotated_morph_dict.json')


def load_annotations(infile):
    click.echo('Loading annotations from {0}.'.format(infile))
    with codecs.open(infile, 'r', 'utf-8') as jsonfile:
        loaded_dict = json.load(jsonfile)
    return loaded_dict


def store_annotations(outfile, loaded_dict):
    click.echo('Storing annotations in {0}.'.format(outfile))
    with codecs.open(outfile, 'wb', 'utf-8') as jsonfile:
        json.dump(loaded_dict, jsonfile)


def line_process(line, loaded_dict):
    line = line.strip()
    if line[0] != '#':
        line_splitted = line.split('\t')
        if len(line_splitted) >= 2:
            form = line_splitted[1]
            if form not in loaded_dict:
                loaded_dict[form] = []
            if len(line_splitted) > 2:
                loaded_dict[form].append(line[2:])
            elif len(loaded_dict[form]) >= 1:
                line_next = loaded_dict[form][0]
                line_splitted += line_next
                line = '\t'.join(line_splitted)
    return line+'\n'


def file_process(infile):
    loaded_dict = load_annotations(JSON_PATH)
    infile_seperated = infile.split('.')
    outfile_name = ".".join(infile_seperated[:-1] + ['tsv'])
    click.echo('Writing in {0}.'.format(outfile_name))
    with click.open_file(infile, 'rb') as f:
        lines = f.readlines()
        with click.open_file(outfile_name, 'w+') as f1:
            for line in lines:
                line = line_process(line, loaded_dict)
                f1.writelines(line)
    store_annotations(JSON_PATH, loaded_dict)


def check_and_process(pathname):
    mode = os.stat(pathname)[ST_MODE]
    if S_ISREG(mode) and pathname.lower().endswith('.conll'):
        # It's a file, call the callback function
        click.echo('Processing {0}.'.format(pathname))
        file_process(pathname)


@click.command()
@click.option('--input_path', '-i', type=click.Path(exists=True, writable=True), prompt=True, required=True, help='Input the file/folder name.')
def main(input_path):
    """My Tool does one thing, and one thing well."""
    if os.path.isdir(input_path):
        for f in os.listdir(input_path):
            pathname = os.path.join(input_path, f)
            check_and_process(pathname)
    else:
        check_and_process(input_path)



