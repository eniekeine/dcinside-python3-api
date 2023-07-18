import itertools
import re
from datetime import datetime
def unquote(encoded):
    """
    JSON 파일에서 유니코드 문자를 이스케이프 시킨 `\\uxxxx` 혹은 `\\uxx`를 해독한다.

    Args:
       encoded (str) : JSON 문자열

    Returns:
       str : 복구된 문자열.

    Examples:
        In [32]: unquote('\\u21\\u61\\uAC00')
        Out[32]: '!a가'

    References:
        https://www.ietf.org/rfc/rfc4627.txt
        The representation of strings is similar to conventions used 
        in the C family of programming languages. A string begins and 
        ends with quotation marks. All Unicode characters may be placed 
        within the quotation marks except for the characters that must be 
        escaped: quotation mark, reverse solidus, and the control characters (U+0000 through U+001F).
        Any character may be escaped.
    """
    return re.sub(r'\\u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: chr(int(m.group(1), 16)), encoded)
def quote(decoded):
    """
    유니코드 캐릭터를 포함한 문자열을 URL 인코딩 한다.
    URL 인코딩은 각 문자를 `%숫자`로 변환한다.
    유니코드에 속한 경우 `%u숫자`로 변환한다.

    Args:
        decoded (str) : URL 인코딩 할 문장. 특수기호와 유니코드를 포함할 수 있다.
    
    Example:
        In [9]: quote("가나다라")
        Out[9]: '%uAC00%uB098%uB2E4%uB77C'

        In [10]: quote("!@#$%^&*()_+")
        Out[10]: '%21%40%23%24%25%5E%26%2A%28%29%5F%2B'

        In [11]: quote("/\\`';,.<>[]")
        Out[11]: '%2F%5C%60%27%3B%2C%2E%3C%3E%5B%5D'

        In [12]: quote("1234567890-=")
        Out[12]: '%31%32%33%34%35%36%37%38%39%30%2D%3D'
    """
    arr = []
    for c in decoded:
        t = hex(ord(c))[2:].upper() 
        if len(t) >= 4:
            arr.append("%u" + t)
        else:
            arr.append("%" + t)
    return "".join(arr)
def peek(iterable):
    """
    이터레이터의 다음 아이템을 훔쳐보기. `next()`와는 달리 이터레이터를 진행시키지는 않는다.
    """
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain((first,), iterable)
def parse_time(time): 
        """
        시간을 나타내는 문자열을 파싱하여 datetime.time 객체로 변환한다.

        Args:
            time (str): 8 가지 형식의 날짜 문자열을 파싱할 수 있다.
                - "10:40"               (10시 40분)
                - "7.1"                 (7월 1일)
                - "7.1 10:40"           (7월 1일 10시 40분)
                - "2022.7.1"            (2022년 7월 1일)
                - "2022.7.1 10:40"      (2022년 7월 1일 10시 40분)
                - "7.1 10:40:22"        (7월 1일 10시 40분 22초)
                - "2022.7.1 10:40:22"   (2022년 7월 1일 10시 40분 22초)
                - "2022-7-1 10:40:22"   (2022년 7월 1일 10시 40분 22초)
            문자열에서 누락된 정보는 현재 날짜와 시간으로 대체된다.

        Returns:
            datetime.time: 입력된 문자열을 파싱한 결과 얻은 시간을 나타내는 객체.
        """
        today = datetime.now()
        if len(time) <= 5: 
            if time.find(":") > 0:
                return datetime.strptime(time, "%H:%M").replace(year=today.year, month=today.month, day=today.day)
            else:
                return datetime.strptime(time, "%m.%d").replace(year=today.year, hour=23, minute=59, second=59)
        elif len(time) <= 11:
            if time.find(":") > 0:
                return datetime.strptime(time, "%m.%d %H:%M").replace(year=today.year)
            else:
                return datetime.strptime(time, "%y.%m.%d").replace(year=today.year, hour=23, minute=59, second=59)
        elif len(time) <= 16:
            if time.count(".") >= 2:
                return datetime.strptime(time, "%Y.%m.%d %H:%M")
            else:
                return datetime.strptime(time, "%m.%d %H:%M:%S").replace(year=today.year)
        else:
            if "." in time:
                return datetime.strptime(time, "%Y.%m.%d %H:%M:%S")
            else:
                return datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
