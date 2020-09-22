from numpy import zeros


def createList(r1, r2):
    """Create a list from a range."""
    return list(range(r1, r2 + 1))


def squarematrixcreate(maxWidth, minWidth, maxHeight, minHeight, points):
    """Create a square matrix of zeros."""
    width = maxWidth - minWidth
    height = maxHeight - minHeight
    matrix = zeros((width, height))
    nlist = list(map(lambda x: x + (maxWidth, maxHeight), points))
    for (x, y) in nlist:
        matrix[x, y] = 1
    return matrix


print(squarematrixcreate(5, -5, 5, -5, [(-5,-5), (-5, -4), (-3, -2), (-2, 3), (3, -2), (5, 5)]))




def ccp(data):
    """Connecting Component Labeling on a 2D square matrix."""
    linked = []
    labels = structure with dimensions of data, initialized with the value of Background
  
    # First pass 
    for row in data:
        for column in row:
            if data[row][column]Background then
  
                neighbors = connected elements with the current element's value
  
                if neighbors is empty then
                    linked[NextLabel] = set containing NextLabel
                    labels[row][column] = NextLabel
                    NextLabel += 1
  
                else
  
                    Find the smallest label
  
                    L = neighbors labels
                    labels[row][column] = min(L)
                    for label in L do
                        linked[label] = union(linked[label], L)
  
    # Second pass
  
    for row in data do
        for column in row do
            if data[row][column] is not Background then
                labels[row][column] = find(labels[row][column])
  
    return labels