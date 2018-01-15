import codecs
import click
import re


class CONLChecker:
    def __init__(self, pathname, verbose):
        self.inputFileName = pathname
        self.verbose = verbose
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
            iscorrect = True
            total_lines = 0
            for (i, line) in enumerate(openedFile):
                iscorrect &= self.__parse(i, line.strip())
                total_lines += 1
            if total_lines < 2:
                click.echo('\nError: The first 2 lines of the file {0} are not present.'.format(self.inputFileName))
                iscorrect = False
            if len(self.IDlist) != len(set(self.IDlist)):
                click.echo('\nError: File {0} : IDs generated are not unique'.format(self.inputFileName))
                iscorrect = False
            if iscorrect:
                click.echo('\nInfo: The file {0} has correct format.'.format(self.inputFileName))

    def check_line(self, linenumber, line):
        iscorrect = True
        line_splitted = line.split('\t')
        if len(line_splitted) < 4:
            click.echo(
                "\nError: No field should be empty in file {0} linenumber {1} (An underscore should be added in fields where we can't add something)."
                    .format(self.inputFileName, linenumber))
            iscorrect = False
        if len(line_splitted) > 0:
            id = line_splitted[0]
            self.IDlist.append(id)
        return iscorrect

    def __parse(self, linenumber, line):
        iscorrect = True
        p_pattern = "^#new_text=[a-zA-Z0-9]+\s*$"
        heading_pattern = "#\s+ID\s+FORM\s+SEGM\s+XPOSTAG\s+HEAD\s+DEPREL\s+MISC\s*"
        if linenumber == 0 and not re.compile(p_pattern).match(line):
            click.echo(
                '\nError: The line number {0} in file {1} does not follow the Conll format "{2}".'
                .format(linenumber, self.inputFileName, p_pattern))
            iscorrect = False
        elif linenumber == 1 and not re.compile(heading_pattern).match(line):
            click.echo(
                '\nError: The line number {0} in file {1} does not follow the Conll format "{2}".'
                .format(linenumber, self.inputFileName, heading_pattern))
            iscorrect = False
        elif linenumber > 1:
            iscorrect &= self.check_line(linenumber, line)
        else:
            pass
        return iscorrect

    # def __parse(self, linenumber, line):
    #     tokenizedLine = line.split(" ")
    #     if len(line) == 0:
    #         pass
    #     elif line[0] == "&":
    #         if len(self.tokens) > 0:
    #             self.write2file()
    #         self.__reset__()
    #         firstword = tokenizedLine[0].lstrip("&")
    #         self.outputFilename = firstword
    #     elif line[0] == "@":
    #         # @(obverse[\?]?|reverse[\?]?|top[\?]?|bottom[\?]?|left[\?]?|right[\?]?|seal\s([A-Z]{1}|[0-9]+)?|surface [a-zA-Z0-9]+|face [a-zA-Z0-9]+)
    #         firstword = tokenizedLine[0].lstrip("@")
    #         if firstword == "obverse":
    #             self.surfaceMode = "o"
    #         elif firstword == "reverse":
    #             self.surfaceMode = "r"
    #         elif firstword == "top":
    #             self.surfaceMode = "t"
    #         elif firstword == "bottom":
    #             self.surfaceMode = "b"
    #         elif firstword == "left":
    #             self.surfaceMode = "l"
    #         elif firstword == "right":
    #             self.surfaceMode = "r"
    #         elif firstword == "surface" or firstword == "face":
    #             self.surfaceMode = tokenizedLine[-1]
    #         elif firstword == "seal":
    #             self.surfaceMode = "s" + tokenizedLine[-1]
    #             self.inEnvelope = ''
    #         elif firstword == "envelope":
    #             self.inEnvelope = 'e'
    #         elif firstword == "column":
    #             self.column = 'col' + tokenizedLine[-1]
    #         elif firstword == 'tablet' or firstword == 'object':
    #             if self.verbose:
    #                 pass
    #                 # click.echo('File {0}, Linenumber {1} : Found a tablet or object in {2}'.format(self.inputFileName,linenumber, line))
    #         else:
    #             if self.verbose:
    #                 click.echo(
    #                     'Warning: File {0}, Linenumber {1} : Unrecognized @ in {2}'.format(self.inputFileName,
    #                                                                                        linenumber, line))
    #     elif line[0] != "#" and is_number(line[0]):
    #         linenumber = tokenizedLine[0].rstrip(".")
    #         tokensToProcess = tokenizedLine[1:]
    #         for i in range(len(tokensToProcess)):
    #             prefix = self.inEnvelope + self.surfaceMode
    #             if self.column == '':
    #                 IDlist = [prefix, linenumber, str(i + 1)]
    #             else:
    #                 IDlist = [prefix, self.column, linenumber, str(i + 1)]
    #             ID = ".".join(IDlist)
    #             form = tokensToProcess[i]
    #             form_clean = form.replace('#', '').replace('[', '').replace(']', '')
    #             self.tokens.append((ID, form_clean))
