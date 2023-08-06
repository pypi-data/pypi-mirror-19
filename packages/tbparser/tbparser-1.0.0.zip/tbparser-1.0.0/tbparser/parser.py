import traceback
import re
import tbparser.models as tbmodel
import tbparser.exceptions as tberror

TB_TITLE = 'Traceback (most recent call last):'
RE_TB_ERRPOINT = re.compile(r'File "(.+?)", line (\d+), in (.+)')
TB_MORETAG = 'During handling of the above exception, another exception occured:'


def parse(tb=None, queit=False, reverse=False):
    try:
        if not tb:
            tb = traceback.format_exc()
        if not queit:
            printtb(tb)
        tb = tb.splitlines()
        parsed_tb = []
        i = 0
        while i < len(tb):
            if tb[i] == TB_TITLE:
                traceset = []
                traceflag = True
                i += 1
                while traceflag:
                    regex_result = RE_TB_ERRPOINT.findall(tb[i].replace("  ", ""))
                    if len(regex_result) > 0 and len(regex_result[0]) == 3:
                        traceset.append({
                            'file': regex_result[0][0],
                            'line': regex_result[0][1],
                            'in': regex_result[0][2],
                            'code': tb[i + 1].strip()
                        })
                        i += 2
                    else:
                        traceflag = False
                if reverse:
                    traceset.reverse()
                parsed_tb.append(tbmodel.TracebackInfo({'exception': tb[i], 'trace': traceset}))
            elif tb[i] == "" and tb[i+1] == TB_MORETAG:
                i += 3
            else:
                i += 1
        return parsed_tb
    except:
        traceback.print_exc()
        raise tberror.InvalidTracebackError


def printtb(tb):
    # TODO(kde713): customize printing
    print(tb)
