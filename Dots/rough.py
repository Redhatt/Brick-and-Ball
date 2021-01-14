def st(a, b, c):
    print(a, b, c)

def finc(fun):
    def w(*args):
        print('done')
        return fun(args)
    return w

v = finc(st)
print(v)
