import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()        # un grafo semplice e pesato
        self._idMap = {}
        self._constructors = []

    # PUNTO 1 ----------------------------------------------------------
    def getYears(self):
        return DAO.getAllYears()
    # FINE PUNTO 1 ------------------------------------------------------

    # PUNTO 2a e 2b ----------------------------------------------------------
    def buildGraph(self, y1, y2):
        self._graph.clear()
        self._constructors = DAO.getAllNodes(y1, y2)
        for c in self._constructors:
            self._idMap[c.constructorId] = c

        self._graph.add_nodes_from(self._constructors)

        self._edges = DAO.getAllEdges(y1, y2)
        for a1, a2, w in self._edges:
            self._graph.add_edge(self._idMap[a1], self._idMap[a2], weight=w)

    # FINE PUNTO 2a e 2b -----------------------------------------------------


    # PUNTO 3 ----------------------------------------------------------
    #  Si visualizzino i 3 archi con peso maggiore.
    def get_top_3_archi(self):
        lista_archi = list(self._graph.edges(data=True))
        lista_archi.sort(key=lambda x: x[2]["weight"], reverse=True)

        return lista_archi[0:3]

    # identificare la componente connessa di dimensione maggiore, e stamparne tutti i nodi, ordinati in senso
    # decrescente secondo il grado dei nodi
    def getConnectedComponents(self):
        componenti = list(nx.connected_components(self._graph))
        componente_max = max(componenti, key = len)

        subgraph = self._graph.subgraph(componente_max).copy()
        orderedNodes = sorted(subgraph.nodes(), key=lambda n: self._graph.degree(n), reverse=True)
        details = [(n, self._graph.degree(n)) for n in orderedNodes]

        return len(componenti), componente_max, details
    # FINE PUNTO 3 ----------------------------------------------------------

    def getNumNodes(self):
        return len(self._graph.nodes())

    def getNumEdges(self):
        return len(self._graph.edges())

