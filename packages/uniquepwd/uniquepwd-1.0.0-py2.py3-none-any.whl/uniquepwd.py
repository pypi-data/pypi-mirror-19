import os
import sys

def uniquePrefix(x, y):
    if len(x) > len(y):
        y += "a"
    r = ""
    for xc, yc in zip(x, y):
        r += xc
        if xc != yc:
            break
    return r

def uniquePrefixMulti(x, ys):
    ys.append("")
    ps = map(lambda y: uniquePrefix(x, y), ys)
    return max(ps, key=lambda z: len(z))

def uniqueListTree(xs, yss):
    assert len(xs) == len(yss)
    return list(map(uniquePrefixMulti, xs, yss))

def uniquepwd(path):
    curpath = os.path.abspath(path)
    upper, cur = os.path.split(curpath)
    assert os.path.exists(curpath)
    if upper == curpath:
        return [curpath]
    else:
        curdirs = [p
                   for p in os.listdir(upper)
                   if os.path.isdir(os.path.join(upper, p)) and
                   p != cur]
        curPrefix = uniquePrefixMulti(cur, curdirs)
    return uniquepwd(upper) + [curPrefix]

def main():
    print(os.path.join(*uniquepwd(sys.argv[1])) + "\\")

if __name__ == '__main__':
    main()
