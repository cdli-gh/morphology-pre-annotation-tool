import codecs
import os

import click


class CONLLFormattor:
    def __init__(self, pathname, verbose=False):
        self.infile = pathname
        self.verbose = verbose

    def __line_process(self, linenumber, line):
        line = line.strip()
        if len(line) > 0 and line[0] != '#':
            line_splitted = line.split('\t')
            line_splitted = list(map(lambda x: x.strip(), line_splitted))
            line_splitted = list(map(lambda x: '_' if x == '' else x, line_splitted))
            line_splitted = line_splitted[:4]
            while len(line_splitted) != 7:
                line_splitted.extend(['_'])
            line = '\t'.join(line_splitted)
        else:
            if self.verbose and linenumber > 2:
                click.echo('\nWarning: Empty line.')
            pass
        return line + '\n'

    def __file_process(self):
        outfolder = os.path.join(os.path.dirname(self.infile), 'output')
        if not os.path.exists(outfolder):
            os.makedirs(outfolder)
        outfile_name = os.path.join(outfolder, os.path.basename(self.infile))
        if self.verbose:
            click.echo('\nInfo: Writing in {0}.'.format(outfile_name))
        with codecs.open(self.infile, 'r', 'utf-8') as f:
            with codecs.open(outfile_name, 'w+', 'utf-8') as f1:
                for (i, line) in enumerate(f):
                    line = self.__line_process(i+1, line)
                    try:
                        f1.writelines(line)
                    except IOError:
                        click.echo('\nError: Could not write the line {0} in file {1}.'.format(line, outfile_name))

    def process(self):
        self.__file_process()
