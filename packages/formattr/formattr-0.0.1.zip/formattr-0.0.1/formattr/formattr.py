#
#   FORMATTR - Format corrector for Python 3.X and 2.X
#      Extremely recommended use on Python 3.6
#              @vmesel - me@vmesel.com

class LenError(BaseException):
    def __init__(self, message):
        self.message = message


def find_strs(string_list):
    pos_list = []
    for i in range(len(string_list)):
        if string_list[i] == '{{}}':
            pos_list.append(i)
    return pos_list


def fmt(sentence, *args):
    if len(args) == 0:
        raise LenError("There are no arguments on formattr.fmt()")
        exit()
    correct_sentence = []
    count = 0
    a = sentence.split(" ")
    indx = find_strs(a)
    if len(args) != len(indx):
        raise LenError("The number of args and items to replace found are different.")
    for ix in indx:
        a[ix] = str(args[indx.index(ix)])
    print(" ".join(a))
