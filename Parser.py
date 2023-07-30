from pathlib import Path
from enum import Enum

DEFAULT_FILE_CONTENT_VALUE = ""
DEFAULT_CURRENT_LINE_CONTENT_VALUE = []
PARAMETER_OPEN = "<"
PARAMETER_CLOSE = ">"
START_KEYWORD = "$"

KEYWORDS_TABLE = \
    (
        "$CREATE_FILE",
        "$LINK",
        "$FILE",
        "$TEXT",
        "$TARGET"
    )


class KEYWORDS_ENUM(Enum):
    CREATE_FILE = 0
    LINK = 1
    FILE = 2
    TEXT = 3
    TARGET = 4


class INVALID_KEYWORD(Exception):
    ErrorMessage = ""

    def __init__(self, LineID, Keyword):
        self.ErrorMessage = 'Invalid keyword "{}" in line {}'.format(Keyword, LineID)


class MISSING_SYNTAX(Exception):
    ErrorMessage = ""

    def __init__(self, LineID, Syntax):
        self.ErrorMessage = 'Missing "{}" in line {}'.format(Syntax, LineID)


class INVALID_ARGUMENT(Exception):
    ErrorMessage = ""

    def __init__(self, LineID, Argument):
        self.ErrorMessage = 'Invalid argument "{}" in line {}'.format(Argument, LineID)


class INVALID_SYNTAX(Exception):
    ErrorMessage = ""

    def __init__(self, LineID, Syntax):
        self.ErrorMessage = 'Invalid syntax "{}" in line {}'.format(Syntax, LineID)


def CheckIsKeyword(Word, LineID):
    if Word[0] != START_KEYWORD:
        raise MISSING_SYNTAX(LineID, START_KEYWORD)

    i = 0
    for Keyword in KEYWORDS_TABLE:
        if Word == Keyword:
            return KEYWORDS_ENUM(i)
        i += 1

    raise INVALID_KEYWORD(LineID, Word)


def CheckParameterCorrectness(Parameter, LineID, MinimumLength):
    if len(Parameter) < MinimumLength:
        raise INVALID_ARGUMENT(LineID, Parameter)
    if Parameter[0] != PARAMETER_OPEN:
        raise MISSING_SYNTAX(LineID, PARAMETER_OPEN)
    elif Parameter[len(Parameter) - 1] != PARAMETER_CLOSE:
        raise MISSING_SYNTAX(LineID, PARAMETER_CLOSE)


def ReadParameter(Parameter):
    Argument = Parameter[1: len(Parameter) - 1]
    return Argument


class Parser:
    FileContent = DEFAULT_FILE_CONTENT_VALUE
    CurrentLine = DEFAULT_CURRENT_LINE_CONTENT_VALUE
    CurrentLineID = 0
    CurrentSeek = 0
    OpenedScope = False

    def __init__(self, File):
        self.FileContent = Path(File).read_text()

    def ReadLine(self):
        self.CurrentLine.clear()
        LocalLine = ""
        for i in range(self.CurrentSeek, len(self.FileContent)):
            if self.FileContent[i] == '\n':
                self.CurrentLineID = self.CurrentLineID + 1
                i += 1
                LocalLine = self.FileContent[self.CurrentSeek: i]
                self.CurrentSeek = i
                break
        if not len(LocalLine):
            return False

        FirstWordCharacter = 0
        for i in range(FirstWordCharacter, len(LocalLine)):
            if LocalLine[i] == PARAMETER_OPEN:
                self.OpenedScope = True
            elif LocalLine[i] == PARAMETER_CLOSE:
                self.OpenedScope = False
            if self.OpenedScope:
                continue
            if LocalLine[i] == ' ' or LocalLine[i] == '\n':
                LocalWord = LocalLine[FirstWordCharacter: i]
                LocalWord.replace('\n', '')
                LocalWord.replace(' ', '')
                if len(LocalWord) >= 1:
                    self.CurrentLine.append(LocalWord)
                i += 1
                FirstWordCharacter = i
        return True

    def ControlBadSyntax(self, RangeEnd, Threshold):
        EndOfRange = RangeEnd if RangeEnd < len(self.CurrentLine) and RangeEnd != 0 else len(self.CurrentLine)
        if len(self.CurrentLine) > Threshold:
            CollectedSyntax = ""
            for i in range(Threshold, EndOfRange):
                CollectedSyntax += self.CurrentLine[i]

            raise INVALID_SYNTAX(self.CurrentLineID, CollectedSyntax)

    def InterpretLine(self):
        Command = []
        if len(self.CurrentLine) <= 1:
            return Command
        elif self.CurrentLine[0][0] == "#":
            return Command
        Keyword = CheckIsKeyword(self.CurrentLine[0], self.CurrentLineID)
        Command.append(Keyword)
        if Keyword == KEYWORDS_ENUM.CREATE_FILE:
            CheckParameterCorrectness(self.CurrentLine[1], self.CurrentLineID, 3)
            Command.append(ReadParameter(self.CurrentLine[1]))
            self.ControlBadSyntax(0, 2)
        elif Keyword == KEYWORDS_ENUM.TARGET:
            CheckParameterCorrectness(self.CurrentLine[1], self.CurrentLineID, 3)
            Command.append(ReadParameter(self.CurrentLine[1]))
            self.ControlBadSyntax(0, 2)
        elif Keyword == KEYWORDS_ENUM.LINK:
            LKeyword = CheckIsKeyword(self.CurrentLine[1], self.CurrentLineID)
            Command.append(LKeyword)
            if LKeyword == KEYWORDS_ENUM.FILE:
                CheckParameterCorrectness(self.CurrentLine[2], self.CurrentLineID, 3)
                Command.append(ReadParameter(self.CurrentLine[2]))
            elif LKeyword == KEYWORDS_ENUM.TEXT:
                CheckParameterCorrectness(self.CurrentLine[2], self.CurrentLineID, 2)
                Command.append(ReadParameter(self.CurrentLine[2]))
            self.ControlBadSyntax(0, 3)

        return Command
