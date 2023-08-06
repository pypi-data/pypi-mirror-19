'''
utility.py
==========
These are some useful utility functions.

Members
~~~~~~~
'''

from functools import reduce

def listify(a):
    '''
    Takes an iterable and makes a sorted list of it and all iterable members.  Creates a nice display.

    :param a: the input list (elements may also be lists)
    :type a: list
    :return: a printable string representing the input list
    :rtype: string
    '''

    if a and hasattr(a, '__iter__'):
        return sorted([listify(list(a)[0])] + listify(list(a)[1:]))
    else:
        return a

def is_tree(num_vert, edge_list):
    '''
    Determines if `edge_list` describes a tree with `num_vert` vertices.

    :param num_vert: the number of vertices in the tree
    :type num_vert: int
    :param edge_list: a list of edges (pairs of vertices)
    :type edge_list: list of (int,int) tuples
    :return: True if the input represents a tree, False otherwise
    '''
    def make_adj_matrix2(num_vert, edge_list):
        array = [[False for x in range(num_vert)] for x in range(num_vert)]
        for v1,v2 in edge_list:
            array[v1][v2] = True
            array[v2][v1] = True
        return array

    def get_adjacent_vertices2(adj_matrix, v):
        return reduce(lambda x,y: (x[0]+[x[1]],x[1]+1) if y else (x[0],x[1]+1), adj_matrix[v], ([],0))[0]

    adj_matrix = make_adj_matrix2(num_vert, edge_list)
    stack = []
    visited = {}
    current = 0
    while len(visited) < num_vert:
        if current not in visited:
            visited[current] = True
            nbhd = get_adjacent_vertices2(adj_matrix, current)
            for x in visited:
                if x in nbhd:
                    nbhd.remove(x)
            if len(nbhd) > 0:
                stack.append(nbhd)
            current = -1
        else:
            return False
        if current == -1:
            while len(stack) > 0 and current == -1:
                nbhd = stack.pop()
                if len(nbhd) > 0:
                    current = nbhd.pop()
                    stack.append(nbhd)
    return len(visited) == num_vert
      
      
    
  
