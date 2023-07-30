from pathlib import Path
import os


class INVALID_TARGET(Exception):
    ErrorMessage = ""

    def __init__(self, LineID, TargetName):
        self.ErrorMessage = 'Invalid file target name "{}" in line {}'.format(TargetName, LineID)


class MISSING_LINKAGE(Exception):
    ErrorMessage = ""

    def __init__(self, LineID, FileName):
        self.ErrorMessage = 'Missing file while linking {} in line {}'.format(FileName, LineID)


def WriteContentToFile(Content, FileName):
    DestinationLinkage = os.open(FileName, os.O_WRONLY | os.O_APPEND)
    os.write(DestinationLinkage, Content)
    os.close(DestinationLinkage)


class FileManager:
    LineID = 0
    TargetName = ""

    def __init__(self):
        pass

    def CreateHeader(self, FileName):
        if os.path.exists(FileName):
            os.remove(FileName)
        DestinationLinkage = os.open(FileName, os.O_CREAT)
        os.close(DestinationLinkage)

    def TargetFile(self, FileName):
        if not os.path.exists(FileName):
            raise INVALID_TARGET(self.LineID, FileName)
        self.TargetName = FileName

    def LinkFile(self, FileName):
        if not os.path.exists(FileName):
            raise MISSING_LINKAGE(self.LineID, FileName)

        if self.TargetName == "":
            raise INVALID_TARGET(self.LineID, "$EMPTY$")

        Linkage = os.open(FileName, os.O_RDONLY)
        Data = os.read(Linkage, os.path.getsize(Linkage))
        os.close(Linkage)

        WriteContentToFile(Data, self.TargetName)

    def LinkText(self, Text):
        if self.TargetName == "":
            raise INVALID_TARGET(self.LineID, "$EMPTY$")

        WriteContentToFile((Text + '\n').encode(), self.TargetName)
