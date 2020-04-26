import math

def get_full_rtm(arg):
    code = ([int(y) for x in arg[0] for y in x] if isinstance(arg, list)
                                                else [int(x) for x in arg if x.isdigit()])
    assert len(code) == 13
    odds = sum(code[::-2]) * 3
    evens = sum(code[-2::-2])
    summa = odds + evens
    if summa % 10:
        r = int(math.ceil(summa / 10.0)) * 10 - summa
    else:
        r = 0
    return ''.join(map(str, code)) + str(r)
    #print(args,code)
if __name__ == '__main__':
    import sys
    print(get_full_rtm('142117 16 00738'))
    #print(get_full_rtm(sys.argv[1:]))
