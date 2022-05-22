import enum
from globals import TokenType


class StateType(enum.Enum):
    START = 0,
    INASSIGN = 1,
    INCOMMENT = 2,
    INNUM = 3,
    INID = 4,
    DONE = 5


reservedWords = {

    {"class", TokenType.CLASS}, {"inherits", TokenType.INHERITS},
    {"if", TokenType.IF}, {"then", TokenType.THEN}, {"else", TokenType.ELSE}, {"fi", TokenType.FI},
    {"while", TokenType.WHILE}, {"loop", TokenType.LOOP}, {"pool", TokenType.POOL},
    {"let", TokenType.LET}, {"in", TokenType.IN},
    {"case", TokenType.CASE}, {"of", TokenType.OF}, {"esac", TokenType.ESAC},
    {"new", TokenType.NEW}, {"isvoid", TokenType.ISVOID}, {"not", TokenType.NOT},
    {"true", TokenType.TRUE}, {"false", TokenType.FALSE}

}

BUFLEN = 256

lineBuf = [];  # holds the current line
linepos = 0  # current position in LineBuf
bufsize = 0  # current size of buffer string
EOF_flag = False  # corrects ungetNextChar behavior on EOF


def get_next_char():
    lune =
    if ()


static int
getNextChar(void)
{ if (!(linepos < bufsize))
{lineno + +;
if (fgets(lineBuf, BUFLEN - 1, source))
{ if (EchoSource)
fprintf(listing, "%4d: %s", lineno, lineBuf);
bufsize = strlen(lineBuf);
linepos = 0;
return lineBuf[linepos + +];
}
else
{EOF_flag = TRUE;
return EOF;
}
}
else return lineBuf[linepos + +];
}