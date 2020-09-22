"""A script that takes a trajectory object and builds a graph object.

A script that takes a trajectory object and builds a graph object
as defined in Graph Class.
"""

from itertools import product

from GraphClass import GraphClass
import networkx as nx
import grakel


def TrajectoryNoteEdges(trajectory):
    """From trajectory build edges based on cartesian product."""
    TotalEdges = []
    dist = [-1, 0, 1]
    for dicts in trajectory.chordPositions:
        chordEdges = []
        cartl = list(product(dicts.values(), dicts.values()))
        for couple in cartl:
            (x1, y1), (x2, y2) = couple
            if (x1 - x2) in dist and (y1 - y2) in dist:
                if not (((x1 - x2) == 1 and (y1 - y2) == -1) or
                        ((x1 - x2) == -1 and (y1 - y2) == 1)):
                    chordEdges.append(couple)
        TotalEdges.append(chordEdges)
    return TotalEdges


def CreateVertices(graph):
    """Add Vertex one by one in object."""
    setOfNodes = NodesSetCreate(graph)
    nodes = dict()
    for index, point in enumerate(setOfNodes):
        graph.addVertex(index, point)
        nodes[point] = index
    return nodes


def NodesSetCreate(graph):
    """Take the set of all duplicate points in trajectory object."""
    listOfNodes = []
    for dictChord in graph.trajectory.chordPositions:
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
    # weights_norm = dict()
    for edge in setOfEdges:
        weights[edge] = multiSetOfEdges.count(edge)
    # Use the following to normalize edge weights
    # maximum = max(list(weights.values()))
    # for edge in setOfEdges:
    #     weights_norm[edge] = weights[edge] / maximum
    # # norm = map((1 / max(list(weights.values()))), weights.values())
    return weights


def CreateEdges(graph, Nodes, Edges):
    """Take the set of all duplicate points in trajectory object."""
    setOfEdges, multiSetOfEdges = EdgesSetCreate(Edges)
    weights = EdgeWeights(setOfEdges, multiSetOfEdges)
    for edge in setOfEdges:
        if (edge[0] in Nodes) and (edge[1] in Nodes):
            graph.addEdge(edge, weight=weights[edge])
            # new order added for graph kernels
            # graph.edge['weight'] = weights[edge]
            # Changed how weight is added
            # graph.addEdge(edge, weights[edge])


def CreateGraph(trajectory):
    """Create the object by encapsulating all functions."""
    graph = GraphClass(trajectory)
    edges = TrajectoryNoteEdges(trajectory)
    nodes = CreateVertices(graph)
    CreateEdges(graph, nodes, edges)
    graph.addCentralities()
    return graph


# def CreateGrakel(trajectory):
#     Edges = TrajectoryNoteEdges(trajectory)
#     setOfEdges, multiSetOfEdges = EdgesSetCreate(Edges)
#     weights = EdgeWeights(setOfEdges, multiSetOfEdges)
#     nodes = []
#     for edge in setOfEdges:
#         nodes.append((edge[0], edge[1], weights[edge]))
#     graph = grakel.Graph(nodes)
#     return graph

def createGrakel(trajectory):
    node_isnotenum = dict()
    edges_with_weights = dict()
    for dicts in trajectory.chordPositions:
        for k, v in dicts.items():
            node_isnotenum[v] = k
    trajectoryEdges = TrajectoryNoteEdges(trajectory)
    setOfEdges, multiSetOfEdges = EdgesSetCreate(trajectoryEdges)
    edges_with_weights = EdgeWeights(setOfEdges, multiSetOfEdges)
    return grakel.Graph(edges_with_weights, node_labels=node_isnotenum)


def createNX(trajectory):
    G = nx.Graph()
    node_isnotenum = dict()
    edges_with_weights = list()
    for dicts in trajectory.chordPositions:
        for k, v in dicts.items():
            node_isnotenum[v] = k
    for node, label in node_isnotenum.items():
        G.add_node(node, note=label)
    trajectoryEdges = TrajectoryNoteEdges(trajectory)
    setOfEdges, multiSetOfEdges = EdgesSetCreate(trajectoryEdges)
    for edge, weight in EdgeWeights(setOfEdges, multiSetOfEdges).items():
        edges_with_weights.append((edge[0], edge[1], weight))
    G.add_weighted_edges_from(edges_with_weights)
    return G


