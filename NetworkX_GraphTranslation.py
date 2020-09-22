import heapq

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from structural_functions import getKeyByValue


def CreateVertices(TrajectoryPoints, Graph):
    """Add Vertex one by one in object."""
    setOfNodes = NodesSetCreate(TrajectoryPoints)
    nodes = dict()
    for index, point in enumerate(setOfNodes):
        Graph.add_node(index)
        nodes[point] = index
    return Graph, nodes


def NodesSetCreate(TrajectoryPoints):
    """Take the set of all duplicate points in trajectory object."""
    listOfNodes = []
    for dictChord in TrajectoryPoints:
        for node in dictChord.values():
            listOfNodes.append(node)
    setOfNodes = list(set(listOfNodes))
    return setOfNodes


def EdgesSetCreate(TrajectoryEdges):
    """Take the set of all duplicate points in trajectory object."""
    listOfEdges = []
    for edgesList in TrajectoryEdges:
        for edge in edgesList:
            listOfEdges.append(edge)
    setOfEdges = list(set(listOfEdges))
    return setOfEdges, listOfEdges


def EdgeWeights(setOfEdges, multiSetOfEdges):
    """Add weights on edges based on multiplicity."""
    weights = dict()
    for edge in setOfEdges:
        weights[edge] = multiSetOfEdges.count(edge)
    # a way to normalize edge weights
    # edgeWeights = map((1 / max(list(weights.values()))), weights.values())
    return weights


def CreateEdges(Nodes, Edges, Graph):
    """Take the set of all duplicate points in trajectory object."""
    setOfEdges, multiSetOfEdges = EdgesSetCreate(Edges)
    weights = EdgeWeights(setOfEdges, multiSetOfEdges)
    for edge in setOfEdges:
        if (edge[0] in Nodes) and (edge[1] in Nodes):
            Graph.add_edge(Nodes[edge[0]], Nodes[edge[1]],
                           weight=weights[edge])
    return Graph

# ------------- ALGORITHMS FOR GRAPH SIMILARITY -------------------


def select_k(spectrum, minimum_energy=0.9):
    """Select k : graph spectrum -> 90% eigenvalues.

    Take a graph spectrum and return the eigenvalues that describe the 90%
    of the graph.
    """
    running_total = 0.0
    total = sum(spectrum)
    if total == 0.0:
        return len(spectrum)
    # Find the eigen values that describe the minimum enery % of the piece
    for i in range(len(spectrum)):
        running_total += spectrum[i]
        if running_total / total >= minimum_energy:
            return i + 1
    return len(spectrum)


def CompareGraphsSpectrum(graph1, graph2):
    """Compare the spectrum of 2 graphs.

    The similarity coeficient in this method compares the minimum
    amount of eigen vectors that describe the 90 % of the graph.
    It yields a possitive number between 0 and infinity.
    Note that closest to zero means higher similarity.
    """
    laplacian1 = nx.spectrum.laplacian_spectrum(graph1)
    laplacian2 = nx.spectrum.laplacian_spectrum(graph2)
    k1 = select_k(laplacian1)
    k2 = select_k(laplacian2)
    # take the fewer dimensions to describe the result
    k = min(k1, k2)
    # the similarity is the sum of the eukleidian distance of the most
    # important nodes
    similarity = sum((laplacian1[:k] - laplacian2[:k])**2)
    return similarity


def graphSimilarity(graphDict):
    """Compute the eigenvalue similarity of graphs."""
    similarityDict = dict()
    for g1 in graphDict.values():
        for g2 in graphDict.values():
            if g1 != g2:
                key1 = getKeyByValue(graphDict, g1)
                key2 = getKeyByValue(graphDict, g2)
                if (key2, key1) not in similarityDict.keys():
                    similarityDict[(key1, key2)
                                   ] = CompareGraphsSpectrum(g1, g2)
    return sorted(similarityDict.items(), key=lambda kv: kv[1])


def CreateGraph(Points, Edges):
    """Create an networkX graph."""
    G = nx.Graph()
    newG, Nodes = CreateVertices(Points, G)
    Graph = CreateEdges(Nodes, Edges, newG)
    return Graph


def GlobalClusteringCoefficient(graph):
    """Compute the Global clustering coefficient.

    The coefficient is the mean of all the trinagles divided by the number
    of nodes.
    """
    coef = np.mean(list(nx.clustering(graph).values()))
    return coef


def ClusteringTransitivity(graph):
    """Compute the clustering trasitivity coefficient."""
    transitivity = nx.transitivity(graph)
    return transitivity


def SquareClusteringCoefficient(graph):
    """Compute the square clustering coefficient."""
    coef = np.mean(list(nx.square_clustering(graph).values()))
    return coef


def PlotCentralities(graph):
    """Plot all centralities for one graph."""
    c_degree = nx.degree_centrality(graph)
    c_degree = list(c_degree.values())

    c_eigenvector = nx.katz_centrality(graph)
    c_eigenvector = list(c_eigenvector.values())

    c_harmonic = nx.harmonic_centrality(graph)
    c_harmonic = list(c_harmonic.values())

    c_betweenness = nx.betweenness_centrality(graph)
    c_betweenness = list(c_betweenness.values())

    plt.figure(figsize=(18, 12))
    f, axarr = plt.subplots(2, 2, num=1)
    plt.sca(axarr[0, 0])
    nx.draw(
        graph,
        cmap=plt.get_cmap('inferno'),
        node_color=c_degree,
        node_size=300,
        with_labels=True)
    axarr[0, 0].set_title('Degree Centrality', size=16)

    plt.sca(axarr[0, 1])
    nx.draw(
        graph,
        cmap=plt.get_cmap('inferno'),
        node_color=c_eigenvector,
        node_size=300,
        with_labels=True)
    axarr[0, 1].set_title('Eigenvalue Centrality (Katz)', size=16)

    plt.sca(axarr[1, 0])
    nx.draw(
        graph,
        cmap=plt.get_cmap('inferno'),
        node_color=c_harmonic,
        node_size=300,
        with_labels=True)
    axarr[1, 0].set_title('harmonic_centrality Centrality', size=16)

    plt.sca(axarr[1, 1])
    nx.draw(
        graph,
        cmap=plt.get_cmap('inferno'),
        node_color=c_betweenness,
        node_size=300,
        with_labels=True)
    axarr[1, 1].set_title('Betweenness Centrality', size=16)


def CentralityPoint2D(graph, numberOfPoints, typePlot):
    """Plot 3D centrality based on type."""
    points = dict()

    c_eigenvector = nx.katz_centrality(graph)
    c_eigenvector = heapq.nlargest(
        numberOfPoints, list(
            c_eigenvector.values()))
    max_eigenvector = max(c_eigenvector)
    points['Eigenvalues'] = c_eigenvector

    c_betweenness = nx.betweenness_centrality(graph)
    c_betweenness = heapq.nlargest(
        numberOfPoints, list(
            c_betweenness.values()))
    max_betweenness = max(c_betweenness)
    points['Betweenness'] = c_betweenness

    c_closeness = nx.closeness_centrality(graph)
    c_closeness = heapq.nlargest(numberOfPoints, list(c_closeness.values()))
    max_closeness = max(c_closeness)
    points['Closeness'] = c_closeness

    c_harmonic = nx.harmonic_centrality(graph)
    c_harmonic = heapq.nlargest(numberOfPoints, list(c_harmonic.values()))
    max_harmonic = max(c_harmonic)
    points['Harmonic'] = c_harmonic

    glCoe = GlobalClusteringCoefficient(graph)

    points['Mix'] = (max_eigenvector, max_harmonic, max_betweenness)
    points['Mix2'] = (max_eigenvector, glCoe, max_closeness)
    points['Mix3'] = (max_eigenvector, glCoe, max_harmonic)
    points['Mix4'] = (
        max_eigenvector,
        glCoe,
        SquareClusteringCoefficient(graph))

    return points[typePlot]


def kaltzCentrality(graph, numberOfPoints):
    """Compute the largest kalz centralities coefficients of a graph.

    You can specify the number of points to output.
    """
    c_eigenvector = nx.katz_centrality(graph)
    c_eigenvector = heapq.nlargest(
        numberOfPoints, list(
            c_eigenvector.values()))
    return c_eigenvector


def betweennessCentrality(graph, numberOfPoints):
    """Compute the largest betweenness centralities coefficients of a graph.

    You can specify the number of points to output.
    """
    c_betweenness = nx.betweenness_centrality(graph)
    c_betweenness = heapq.nlargest(
        numberOfPoints, list(
            c_betweenness.values()))
    return c_betweenness


def closenessCentrality(graph, numberOfPoints):
    """Compute the largest closeness centralities coefficients of a graph.

    You can specify the number of points to output.
    """
    c_closeness = nx.closeness_centrality(graph)
    c_closeness = heapq.nlargest(numberOfPoints, list(c_closeness.values()))
    return c_closeness


def harmonicCentrality(graph, numberOfPoints):
    """Compute the largest harmonic centralities coefficients of a graph.

    You can specify the number of points to output.
    """
    c_harmonic = nx.harmonic_centrality(graph)
    c_harmonic = heapq.nlargest(numberOfPoints, list(c_harmonic.values()))
    return c_harmonic


def degreeCentrality(graph, numberOfPoints):
    """Compute the largest degree centralities coefficients of a graph.

    You can specify the number of points to output.
    """
    c_degree = nx.degree_centrality(graph)
    c_degree = heapq.nlargest(numberOfPoints, list(c_degree.values()))
    return c_degree


def chooseCentrality(graph, numberOfPoints, typePlot):
    """Choose the Centrality you want to compute.

    You can specify the number of points to output.
    """
    if typePlot == 'kaltz':
        return kaltzCentrality(graph, numberOfPoints)
    elif typePlot == 'betweenness':
        return betweennessCentrality(graph, numberOfPoints)
    elif typePlot == 'closeness':
        return closenessCentrality(graph, numberOfPoints)
    elif typePlot == 'harmonic':
        return harmonicCentrality(graph, numberOfPoints)
    elif typePlot == 'degree':
        return degreeCentrality(graph, numberOfPoints)
    else:
        raise KeyError()
