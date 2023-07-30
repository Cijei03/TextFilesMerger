class BadSyntax(Exception):
    def __init__(self, UserMessage):
        self.UserMessage = "SYNTAX ERROR: " + UserMessage