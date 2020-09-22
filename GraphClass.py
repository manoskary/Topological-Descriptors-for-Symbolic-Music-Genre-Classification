from networkx import nx

from numpy import mean


class GraphClass:
    """Graph Object contains Trajectory, MidiInfo, Centralities, FileName..."""

    def __init__(self, trajectory):
        """Initialization function, build an empty nx.graph."""
        self.trajectory = trajectory
        self.vertices = []
        self.edges = []
        self.graph = nx.Graph()
        # self.name = None
        self.style = None
        self.composer = None
        self.harmony = None

    def addVertex(self, index, point):
        """Add a new vertex to the graph.

        Note that vertices are enumerations. That means that
        a vertex has an id of an integer value.
        """
        self.vertices.append(point)
        self.graph.add_node(index)

    def addEdge(self, edge, weight):
        """Add a new edge to the graph.

        Note that edges are enumerations. That means that
        an edge has an id of an integer value.
        """
        self.edges.append(edge)
        self.graph.add_edge(edge[0], edge[1])

    def addCentralities(self):
        """Add centrality coeficients for the final version of the graph.

        Centralities include : Kalz centrality, global clustering,
        square clustering, closeness centrality, harmonic centrality,
        betweenness centrality.
        From all centralities we choose the max or the mean. More about
        these centralities can be found in networkX algorithms.
        """
        self.kalz_coef = max(list(nx.katz_centrality(self.graph).values()))
        self.glob_clust_coef = mean(list(nx.clustering(self.graph).values()))
        self.square_clustering_coef = mean(
            list(nx.square_clustering(self.graph).values()))
        self.harmonic_coef = max(
            list(nx.harmonic_centrality(self.graph).values()))
        self.betweenness_coef = max(
            list(nx.betweenness_centrality(self.graph).values()))
        self.closeness_coef = max(
            list(nx.closeness_centrality(self.graph).values()))

    def addName(self, name):
        """Add the name of the file."""
        self.name = name

    def addStyle(self, style_label):
        """Add the style of the piece.

        For example: classical, pop, rock, baroque, etc.
        """
        self.style = style_label

    def addHarmonyStyle(self, harmony_label):
        """Add the harmony style of the piece.

        For example : chromatic, classic, modal, atonal, etc.
        """
        self.harmony = harmony_label

    def addComposer(self, composer):
        """Add the Composer of the piece.

        For example : beethoven, queen, madonna, etc.
        """
        self.composer = composer
