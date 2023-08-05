
def insertionSort(xs, beg, end):
    for i in xrange(beg, end):
        k = i
        x = xs[i]
        for j in xrange(i + 1, end):
            y = xs[j]
            if y < x:
                k = j
                x = y
        if k != i:
            t = xs[i]
            xs[i] = x
            xs[k] = t

def radixSort(xs, bits=None):
    """in place integer radix sort."""
    if bits is None:
        bits = xs.itemsize*8

    stk = []
    msk = 1 << (bits - 1)
    stk.append((msk, 0, len(xs)))
    while len(stk):
        (msk, st, en) = stk.pop()
        a = st
        b = en
        while a < b:
            x = xs[a]
            while a < b and not x & msk:
                a += 1
                if a < b:
                    x = xs[a]
            y = xs[b-1]
            while a < b and y & msk:
                b -= 1
                if a < b:
                    y = xs[b-1]

            if a < b:
                xs[b-1] = x
                xs[a] = y

                a += 1
                b -= 1

        r = a - st
        if r > 16:
            stk.append((msk >> 1, st, a))
        else:
            insertionSort(xs, st, a)

        r = en - a
        if r > 16:
            stk.append((msk >> 1, a, en))
        else:
            insertionSort(xs, a, en)

def partition(xs, st, en):
    piv = xs[en-1]
    i = st
    for j in xrange(st, en):
        if xs[j] < piv:
            t = xs[i]
            xs[i] = xs[j]
            xs[j] = t
            i += 1
    t = xs[i]
    xs[i] = xs[en-1]
    xs[en-1] = t
    return i


def quickSort(xs):
    """in place integer quicksort."""
    stk = []
    stk.append((0, len(xs)))
    while len(stk):
        (st, en) = stk.pop()
        i = partition(xs, st, en)

        r = i - st
        if r > 16:
            stk.append((st, i))
        else:
            insertionSort(xs, st, i)

        r = en - i
        if r > 16:
            stk.append((i, en))
        else:
            insertionSort(xs, i, en)

def swap(xs, i, j):
    t = xs[i]
    xs[i] = xs[j]
    xs[j] = t

def upheap(xs, i):
    p = i // 2
    while p >= 1:
        if xs[i - 1] > xs[p - 1]:
            #swap(xs, i - 1, p - 1)
            t = xs[i - 1]
            xs[i - 1] = xs[p - 1]
            xs[p - 1] = t
            i = p
            p = i // 2
        else:
            break

def downheap(xs, z, p):
    c = 2*p
    while c <= z:
        if c < z and xs[c] > xs[c - 1]:
            c += 1
        if xs[c - 1] > xs[p - 1]:
            #swap(xs, c - 1, p - 1)
            t = xs[c - 1]
            xs[c - 1] = xs[p - 1]
            xs[p - 1] = t
            p = c
            c = 2*p
        else:
            break

def heapify(xs):
    z = len(xs) + 1
    for i in xrange(1, z):
        upheap(xs, i)

def heapSort(xs):
    """in place integer heapsort."""
    
    heapify(xs)
    z = len(xs)
    for i in xrange(1, z):
        x = xs[0]
        xs[0] = xs[z - i]
        xs[z - i] = x
        downheap(xs, z - i, 1)

def radixCount(xs, st, en, s):
    vs = [0 for i in xrange(256)]
    for i in xrange(st, en):
        r = (xs[i] >> s) & 255
        vs[r] += 1
    t = 0
    for i in xrange(256):
        v = vs[i]
        vs[i] = t
        t += v
    return vs

def flagSwap(xs, st, en, vs, s):
    ns = [v for v in vs]
    i = st
    c = 0
    print ns
    while c < len(vs) - 1:
        if i >= st + vs[c+1]:
            c += 1
            continue
        r = (xs[i] >> s) & 255
        if r == c:
            i += 1
            continue
        j = ns[r]
        xs[i], xs[j] = xs[j], xs[i]
        ns[r] += 1

def sort(xs):
    d = xs.itemsize - 1
    stk = []
    stk.append((d, 0, len(xs)))
    while len(stk):
        (d, st, en) = stk.pop()

        if en - st < 32:
            insertionSort(xs, st, en)
            continue
        
        vs = radixCount(xs, st, en, 8*d)
        flagSwap(xs, st, en, vs, 8*d)
        p = 0
        for v in vs:
            l = v - p
            if l > 16:
                stk.append((d - 1, st + p, st + v))
            elif l > 1:
                insertionSort(xs, st + p, st + v)
            p = v

