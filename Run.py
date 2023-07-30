import sys
import simple_colors
import os

# Import initialization checker.
from Core import HeaderList
from Core import CONSTANT_HEADER_FILE_NAME

# Import parser data.
from Parser import Parser
from Parser import KEYWORDS_ENUM
from Parser import INVALID_KEYWORD
from Parser import MISSING_SYNTAX
from Parser import INVALID_ARGUMENT
from Parser import INVALID_SYNTAX

# Import file manager.
from FileManager import FileManager
from FileManager import INVALID_TARGET
from FileManager import MISSING_LINKAGE


def PrintError(Msg):
    print(simple_colors.red(Msg) + ".")


def PrintCriticalError(Msg):
    print(simple_colors.red(Msg) + ".")
    exit(0)


def PrintSuccess(Msg):
    print(simple_colors.green(Msg) + ".")


# Check file exists. If no, then exit.
if len(sys.argv) > 1:
    HL = HeaderList(sys.argv[1])
    if not HL.CheckOnlyPath():
        PrintCriticalError(HL.OutputMessage)
    if HL.CheckExists():
        PrintSuccess(HL.OutputMessage)
        os.chdir(HL.OnlyPath[0 : len(HL.OnlyPath) - 1])
    else:
        PrintCriticalError(HL.OutputMessage)
else:
    HL = HeaderList("")
    if HL.CheckExists():
        PrintSuccess(HL.OutputMessage)
        ListPath = HL.CompletePath
    else:
        PrintCriticalError(HL.OutputMessage)

ListParser = Parser(CONSTANT_HEADER_FILE_NAME)
FM = FileManager()
while ListParser.ReadLine():
    try:
        Command = ListParser.InterpretLine()
        if len(Command) == 0:
            continue
        FM.LineID = ListParser.CurrentLineID
        if Command[0] == KEYWORDS_ENUM.CREATE_FILE:
            FM.CreateHeader(Command[1])
        elif Command[0] == KEYWORDS_ENUM.TARGET:
            FM.TargetFile(Command[1])
        elif Command[0] == KEYWORDS_ENUM.LINK:
            if Command[1] == KEYWORDS_ENUM.FILE:
                FM.LinkFile(Command[2])
            elif Command[1] == KEYWORDS_ENUM.TEXT:
                FM.LinkText(Command[2])
    except INVALID_KEYWORD as Error:
        PrintCriticalError(Error.ErrorMessage)
    except MISSING_SYNTAX as Error:
        PrintCriticalError(Error.ErrorMessage)
    except INVALID_ARGUMENT as Error:
        PrintCriticalError(Error.ErrorMessage)
    except INVALID_SYNTAX as Error:
        PrintCriticalError(Error.ErrorMessage)
    except MISSING_LINKAGE as Error:
        PrintCriticalError(Error.ErrorMessage)
    except INVALID_TARGET as Error:
        PrintCriticalError(Error.ErrorMessage)