'''
rooted_tree.py
==============
Rooted Tree Algorithms.  Well, only random selection.  I believe there is
enough material in chapter 13 of [NW1978]_ to implement an enumerated
sequence (interesting challenge).

Members
~~~~~~~
'''

import random as rng

rooted_tree_count = {}
def random(nn):
    '''
    Returns a random rooted tree on nn vertices

    :param nn: number of vertices in the output tree.
    :type nn: int
    :return: a random rooted tree
    :rtype: list

    The returned list is in `Prufer Code <https://en.wikipedia.org/wiki/Pr%C3%BCfer_sequence>`_.
    You can convert the result to an edge list by zipping it with the
    sequence [0,1,..,nn] and discarding the initial entry, which is always (0,0).


    >>> result = rooted_tree.random(7)
    >>> edge_list = list(zip(result, range(len(result))))[1:]

    '''
    def tc(n):
        if n not in rooted_tree_count:
            if n <= 2:
                rooted_tree_count[n] = 1
            else:
                sum = 0
                for m in range(1,n):
                    inner = 0
                    term = tc(n-m)
                    for d in range(1,m+1):
                        if m % d == 0:
                            inner += d * tc(d)
                    sum += term * inner
                rooted_tree_count[n] = sum / (n-1)
        return rooted_tree_count[n]

    def select_jd(n):
        tn = tc(n)
        rho = rng.random()
        sum = 0
        for j in range(1,n+1):
            for d in range(1,n+1):
                if n - j*d > 0:
                    prob = float(d)*tc(n-j*d)*tc(d)/((n-1)*tn)
                    sum += prob
                    if sum > rho:
                        return j,d

    # begin random rooted tree
    stack = []
    tree = []
    t = 0
    tm1 = -1
    k = 0
    r = 0
    n = nn

    done = False
    while not done:
        if n <= 2:
            tm1 = t
            t = len(tree)
            for i in range(0,n):
                tree.append(t)
            k += n
        else:
            j,d = select_jd(n)
            stack.append((j,d))
            n = n - j*d
            continue
        while len(stack) > 0:
            j,d = stack.pop()
            if d > 0:
                stack.append((j,0))
                n = d
                break
            else:
                lt = len(tree)
                for i in range(0,j-1):
                    save = tree[t]
                    for j in range(t,lt):
                        if tree[j] != save:
                            k += 1
                        tree.append(k)
                for j in range(t,len(tree)):
                    if tree[j] == j:
                        tree[j] = tm1
                t = tm1
                if tm1 > 0:
                    tm1 -= 1
                while tm1 > 0 and tree[tm1] != tm1:
                    tm1 -= 1
                done = len(stack) == 0
    return tree
