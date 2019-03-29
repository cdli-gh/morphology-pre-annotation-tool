import codecs
import json
import os
import shutil
import platform
import click

# Workaround for MPAT missing "HOME" env. var. when running on Windows 
if platform.system()=='Windows' and "HOME" not in os.environ.keys():
    os.environ["HOME"] = os.environ["USERPROFILE"]
DICT_JSON = 'annotated_morph_dict_v2.json'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.environ['HOME']
if HOME_DIR:
    FOLDER = os.path.join(HOME_DIR, '.cdlimpatool')
else:
    FOLDER = os.path.join(ROOT_DIR, '.cdlimpatool')
JSON_PATH = os.path.join(FOLDER, DICT_JSON)


class CONLLAnnotator:
    def __init__(self, pathname, verbose=False, no_output=False, add_underscores=False):
        self.infile = pathname
        self.jsonfile = JSON_PATH
        self.verbose = verbose
        self.no_output = no_output
        self.add_underscores = add_underscores
        self.loaded_dict = {}

    @staticmethod
    def delete_folder():
        click.echo(
            '\nWarning: Deleting annotation json dictionary file at {0}.'.format(FOLDER))
        if not os.path.exists(FOLDER):
            click.echo(
                '\nError: Folder {0} does not exist. The tool will create folder during first time usage'.format(FOLDER))
        else:
            shutil.rmtree(FOLDER)

    def __load_annotations(self):
        if self.verbose:
            click.echo('\nInfo: Loading annotations from {0}.'.format(self.jsonfile))
        try:
            with codecs.open(self.jsonfile, 'r', 'utf-8') as jsonfile:
                self.loaded_dict = json.load(jsonfile)
        except IOError:
            click.echo(
                '\nWarning: First time usage : creating annotation json dictionary file as {0}.'.format(self.jsonfile))
            if not os.path.exists(FOLDER):
                os.makedirs(FOLDER)
            self.loaded_dict = {}
            self.__store_annotations()
            with codecs.open(self.jsonfile, 'r', 'utf-8') as jsonfile:
                self.loaded_dict = json.load(jsonfile)

    def __store_annotations(self):
        if self.verbose:
            click.echo('\nInfo: Storing annotations in {0}.'.format(self.jsonfile))
        with codecs.open(self.jsonfile, 'w', 'utf-8') as jsonfile:
            json.dump(self.loaded_dict, jsonfile, indent=2)

    def __line_process(self, linenumber, line):
        line = line.strip()
        if len(line) > 0 and line[0] != '#':
            line_splitted = line.split('\t')
            if len(line_splitted) >= 2:
                form = line_splitted[1]
                if form not in self.loaded_dict:
                    self.loaded_dict[form] = []
                if len(line_splitted) > 2:
                    if len(line_splitted) > 4:
                        annotated_value = line_splitted[2:4]
                    else:
                        annotated_value = line_splitted[2:]
                    if annotated_value in list(map(lambda x: x['annotation'], self.loaded_dict[form])):
                        for i in range(len(self.loaded_dict[form])):
                            if self.loaded_dict[form][i]['annotation'] == annotated_value:
                                self.loaded_dict[form][i]['count'] += 1
                        self.loaded_dict[form] = sorted(self.loaded_dict[form], key=lambda k: k['count'], reverse=True)
                    elif annotated_value[0] != '_':
                        annotation_dict = {'annotation': annotated_value, 'count': 1}
                        self.loaded_dict[form].append(annotation_dict)
                    else:
                        pass
                elif len(self.loaded_dict[form]) >= 1:
                    line_next = []
                    for i in range(len(self.loaded_dict[form])):
                        line_next.extend(self.loaded_dict[form][i]['annotation'])
                    line_splitted += line_next
                    line = '\t'.join(line_splitted)
                elif self.add_underscores:
                    line_next = ['_', '_']
                    line_splitted += line_next
                    line = '\t'.join(line_splitted)
        else:
            if self.verbose and linenumber > 2:
                click.echo('\nWarning: Empty line or Comment.')
            pass
        return line + '\n'

    def __file_process(self):
        outfolder = os.path.join(os.path.dirname(self.infile), 'output')
        if not self.no_output and not os.path.exists(outfolder):
            os.makedirs(outfolder)
        outfile_name = os.path.join(outfolder, os.path.basename(self.infile))
        if self.verbose and not self.no_output:
            click.echo('\nInfo: Writing in {0}.'.format(outfile_name))
        with codecs.open(self.infile, 'r', 'utf-8') as f:
            if self.no_output:
                for (i, line) in enumerate(f):
                    self.__line_process(i+1, line)
            else:
                with codecs.open(outfile_name, 'w+', 'utf-8') as f1:
                    for (i, line) in enumerate(f):
                        line = self.__line_process(i+1, line)
                        try:
                            f1.writelines(line)
                        except IOError:
                            click.echo('\nError: Could not write the line {0} in file {1}.'.format(line, outfile_name))

    def process(self):
        self.__load_annotations()
        self.__file_process()
        self.__store_annotations()
