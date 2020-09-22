import os

import matplotlib.pyplot as plt
from NetworkX_GraphTranslation import CentralityPoint2D, chooseCentrality


def getCentrCoord(dictOfGraphs, typePlot):
    """Get the coordinates of a certain plot Type."""
    points = []
    coordDict = dict()
    for key, graph in dictOfGraphs.items():
        point = CentralityPoint2D(graph, 3, typePlot)
        points.append(point)
        coordDict[key] = point
    return zip(*points)


def CentralitiesScatterPlot(
        dictOfGraphs1,
        dictOfGraphs2,
        dictOfGraphs3,
        typePlot='Mix',
        imageDirectory="Graphs",
        label1="first_input",
        label2="second_input",
        label3="third_input"):
    """Return a Scatter Plot of Centralities for 3 different labels."""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    x1, y1, z1 = getCentrCoord(dictOfGraphs1, typePlot)
    x2, y2, z2 = getCentrCoord(dictOfGraphs2, typePlot)
    x3, y3, z3 = getCentrCoord(dictOfGraphs3, typePlot)

    ax.scatter(
        x1,
        y1,
        z1,
        alpha=0.5,
        c='b',
        edgecolors='none',
        s=30,
        label=label1)
    ax.scatter(
        x2,
        y2,
        z2,
        alpha=0.5,
        c='r',
        edgecolors='none',
        s=30,
        label=label2)
    ax.scatter(
        x3,
        y3,
        z3,
        alpha=0.5,
        c='g',
        edgecolors='none',
        s=30,
        label=label3)

    if typePlot == 'Mix':
        ax.set_xlabel('Eigenvalues')
        ax.set_ylabel('Harmonic')
        ax.set_zlabel('Betweenness')
    if typePlot == 'Mix2':
        ax.set_xlabel('Eigenvalues')
        ax.set_ylabel('Glob.Clustering')
        ax.set_zlabel('Closeness')
    if typePlot == 'Mix3':
        ax.set_xlabel('Eigenvalues')
        ax.set_ylabel('Glob.Clustering')
        ax.set_zlabel('Harmonic')
    if typePlot == 'Mix4':
        ax.set_xlabel('Eigenvalues')
        ax.set_ylabel('Glob.Clustering')
        ax.set_zlabel('Square Clustering ')
    else:
        ax.set_xlabel(typePlot)

    plt.title('3D plotting ' + typePlot + ' method')
    plt.legend(loc=2)
    completeName = imageDirectory + "/" + label1 + "_" + \
        label2 + "_" + label3 + "_" + typePlot + ".png"
    fig.savefig(completeName)   # save the figure to file
    plt.close(fig)


def Centralities2DPlot(dictOfGraphs1, dictOfGraphs2, dictOfGraphs3):
    """Return a Scatter Plot of Centralities for 2 different labels."""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    x1, y1, z1 = getCentrCoord(dictOfGraphs1, 'Mix')
    x2, y2, z2 = getCentrCoord(dictOfGraphs2, 'Mix')
    x3, y3, z3 = getCentrCoord(dictOfGraphs3, 'Mix')

    ax.scatter(
        x1,
        z1,
        alpha=0.5,
        c='b',
        edgecolors='none',
        s=30,
        label='first input')
    ax.scatter(
        x2,
        z2,
        alpha=0.5,
        c='r',
        edgecolors='none',
        s=30,
        label='first input')
    ax.scatter(
        x3,
        z3,
        alpha=0.5,
        c='g',
        edgecolors='none',
        s=30,
        label='first input')

    ax.set_xlabel('Eigen')
    ax.set_ylabel('Harmonic')

    plt.title('Centralities 2D Plot 3 gengre')
    plt.legend(loc=2)
    plt.show()


def plotCentrality(
        dictOfGraphs,
        numberOfPoints=3,
        typeOfCentrality='kaltz',
        directory='Graphs',
        name='test',
        fileIndex=0):
    """Return a Scatter Plot of Centralities for a single label."""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    # ax = fig.gca(projection='3d')

    points = []

    for graph in dictOfGraphs.values():
        point = chooseCentrality(graph, numberOfPoints, typeOfCentrality)
        points.append(point)

    x, y, z = zip(*points)

    ax.scatter(x, y, z, alpha=0.5, c='b', edgecolors='none', s=30)

    ax.set_xlabel(typeOfCentrality)

    completeName = directory + "/" + name + str(fileIndex) + ".png"
    fig.savefig(completeName)   # save the figure to file
    plt.close(fig)


def plotAllCentralities3D(dictOfGraphs):
    """Return a Scatter Plot of every Centrality."""
    centralities = ['kaltz', 'betweenness', 'closeness', 'harmonic', 'degree']
    directory = input("Enter the directory of your files : ")
    isDirectory = os.path.isdir(directory)
    while not isDirectory:
        directory = input(
            "The directory wasn't valid enter another directory : ")
        isDirectory = os.path.isdir(directory)

    name = input("Enter the name of your files")
    for centrality in centralities:
        index = "_" + centrality + "_centrality"
        plotCentrality(dictOfGraphs, 3, centrality, directory, name, index)
