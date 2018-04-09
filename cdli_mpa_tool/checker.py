import codecs
import click
import collections
import re


class CONLChecker:
    def __init__(self, pathname, verbose):
        self.inputFileName = pathname
        self.verbose = verbose
        self.iscorrect = True
        self.__reset__()

    def __reset__(self):
        self.surfaceMode = ''
        self.inEnvelope = ''
        self.column = ''
        self.IDlist = []

    def check(self):
        if self.verbose:
            click.echo('\nInfo: Checking file {0}.'.format(self.inputFileName))
        with codecs.open(self.inputFileName, 'r', 'utf-8') as openedFile:
            total_lines = 0
            for (i, line) in enumerate(openedFile):
                self.__parse(i, line.strip())
                total_lines += 1
            if total_lines < 2:
                click.echo('\nError: The first 2 lines of the file {0} are not present.'.format(self.inputFileName))
                self.iscorrect = False
            if len(self.IDlist) != len(set(self.IDlist)):
                click.echo('\nError: File {0} : IDs generated are not unique'.format(self.inputFileName))
                duplicates = [item for item, count in collections.Counter(self.IDlist).items() if count > 1]
                click.echo('\n Duplicate IDs : {0).'.format(duplicates))
                self.iscorrect = False
            if self.iscorrect:
                click.echo('\nInfo: The file {0} has correct format.'.format(self.inputFileName))

    def check_line(self, linenumber, line):
        line_splitted = line.split('\t')
        if len(line_splitted) < 4:
            click.echo(
                "\nError: No field should be empty in file {0} linenumber {1} (An underscore should be added in fields where we can't add something)."
                .format(self.inputFileName, linenumber))
            self.iscorrect = False
        if len(line_splitted) > 0:
            id_form = line_splitted[0]
            id_pattern = r"^e?(o|r|t|b|l|ri|(s?[a-z]?[0-9]?))\.(col[0-9]'?\.)?[0-9]+'?\.[0-9]+$"
            if not re.compile(id_pattern).match(id_form):
                click.echo('\nError: The id {0} in line number {1} in file {2} does not follow the Conll format "{3}".'
                           .format(id_form, linenumber, self.inputFileName, id_pattern))
                self.iscorrect = False
            self.IDlist.append(id_form)

    def __parse(self, linenumber, line):
        p_pattern = r"^#new_text=[a-zA-Z0-9]+\s*$"
        heading_pattern = r"#\s+ID\s+FORM\s+SEGM\s+XPOSTAG\s+HEAD\s+DEPREL\s+MISC\s*"
        if linenumber == 0 and not re.compile(p_pattern).match(line):
            click.echo('\nError: The line number {0} in file {1} does not follow the Conll format "{2}".'
                       .format(linenumber, self.inputFileName, p_pattern))
            self.iscorrect = False
        elif linenumber == 1 and not re.compile(heading_pattern).match(line):
            click.echo('\nError: The line number {0} in file {1} does not follow the Conll format "{2}".'
                       .format(linenumber, self.inputFileName, heading_pattern))
            self.iscorrect = False
        elif linenumber > 1:
            self.check_line(linenumber, line)
        else:
            pass
