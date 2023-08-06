class InvalidTracebackError(Exception):
    def __init__(self, linenum=-1):
        self.linenum = linenum
        super(self.__class__, self).__init__()

    def __str__(self):
        details = ": at line %d" % self.linenum if self.linenum > 0 else ""
        return "InvalidTracebackError" + details
