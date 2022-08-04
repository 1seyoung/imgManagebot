from telegram.ext.conversationhandler import ConversationHandler

END = ConversationHandler.END

#subscribe select
ID= map(chr,range(2))

ANSWER = map(chr,range(3,4))

EXISTING  = map(chr, range(4,5))

NOT_NUMBER = map(chr, range(5,6))
CALL_Y = map(chr, range(6,7))

INSERT,REVISE = map(chr, range(7,9))

NAME,AGE,GENDER = map(chr, range(9,12))

SELECT = map(chr, range(12,13))

INSERT_TWO,TYPING,INSERT_THREE = map(chr, range(13,16))

T_A = map(chr, range(16,17))

LEN = map(chr, range(17,18))

BACK = map(chr, range(18,19))

QNUMBER = map(chr, range(19,20))

RESTART = map(chr, range(20,21))

STIME , ETIME= map(chr,range(21,23))