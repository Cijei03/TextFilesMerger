import os
from pathlib import Path

CONSTANT_HEADER_FILE_NAME = "HeaderList.txt"


class HeaderList:
    OutputMessage = ""
    OnlyPath = ""
    CompletePath = ""

    def __init__(self, UserPath):
        if (len(UserPath)):
            self.OnlyPath = UserPath + "/"
        self.CompletePath = self.OnlyPath + CONSTANT_HEADER_FILE_NAME

    def CheckOnlyPath(self):
        LocalPath = self.OnlyPath[0: len(self.OnlyPath) - 1]
        if Path(LocalPath).exists():
            return True

        self.OutputMessage = "Entered path '{}' is invalid".format(self.OnlyPath)
        return False

    def CheckExists(self):
        LocalPath = Path(self.CompletePath)
        if LocalPath.exists():
            self.OutputMessage = "Successfully found {}".format(CONSTANT_HEADER_FILE_NAME)
            return True
        self.OutputMessage = "Couldn't find {}".format(CONSTANT_HEADER_FILE_NAME)
        return False
