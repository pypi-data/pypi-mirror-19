import tbparser.exceptions as tberror


class TracebackInfo(dict):
    def __init__(self, dic=None):
        super(self.__class__, self).__init__()
        if isinstance(dic, dict):
            if "exception" in dic.keys() and "trace" in dic.keys():
                self.update(dic)
            else:
                raise tberror.InvalidTracebackError
        elif dic is None:
            pass
        else:
            raise tberror.InvalidTracebackError

    # TODO(kde713): Extend TracebackInfo
