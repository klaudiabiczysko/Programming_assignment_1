class Digraph:
    def __init__(self, edges=None, vertices=None):
        self._edges = edges if edges is not None else []
        self._vertices = vertices if vertices is not None else []

    def vertices(self):
        for edge in self._edges:
            for vertex in edge:
                if vertex not in self._vertices:
                    self._vertices.append(vertex)
        return self._vertices

    def edges(self):
        return self._edges

    def add_edge(self, source, dest):
        edge_tuple = (source, dest)
        self._edges.append(edge_tuple)

    def remove_vertex(self, vertex):
        if vertex in self._vertices:
            self._vertices.remove(vertex)

        for edge in self._edges.copy():
            if vertex in edge:
                self._edges.remove(edge)

    def is_transitive(self):
        for i, j in self._edges:
            for k, l in self._edges:
                if j == k and (i, l) not in self._edges:
                    return False
        return True


#d = Digraph(edges=[(1, 2), (1, 3), (2, 3), (3, 3)], vertices=[4])

#for source, dest in d.edges():
#    if source == dest:
#        print(f'Detected loop from {source} to {dest}')

#print(d.vertices())
#d.add_edge(5, 4)
#print(d.edges())
#d1.remove_vertex(6)
#print(d.vertices())
#print(d.is_transitive())


