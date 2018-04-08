import codecs
import os

import click


class CONLLFormattor:
    def __init__(self, pathname, verbose=False):
        self.infile = pathname
        self.verbose = verbose

    @staticmethod
    def __line_process(line):
        line = line.strip()
        if line[0] != '#':
            line_splitted = line.split('\t')
            line_splitted = map(lambda x: x.strip(), line_splitted)
            line_splitted = map(lambda x: '_' if x == '' else x, line_splitted)
            line_splitted = line_splitted[:4]
            while len(line_splitted) != 7:
                line_splitted.extend(['_'])
            line = '\t'.join(line_splitted)
        return line + '\n'

    def __file_process(self):
        outfolder = os.path.join(os.path.dirname(self.infile), 'output')
        if not os.path.exists(outfolder):
            os.makedirs(outfolder)
        outfile_name = os.path.join(outfolder, os.path.basename(self.infile))
        if self.verbose:
            click.echo('\nInfo: Writing in {0}.'.format(outfile_name))
        with codecs.open(self.infile, 'r', 'utf-8') as f:
            lines = f.readlines()
            with codecs.open(outfile_name, 'w+', 'utf-8') as f1:
                for line in lines:
                    line = self.__line_process(line)
                    try:
                        f1.writelines(line)
                    except IOError:
                        click.echo('\nError: Could not write the line {0} in file {1}.'.format(line, outfile_name))

    def process(self):
        self.__file_process()
