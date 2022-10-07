
def get_next_node(tentative_distances, visited):
    for node in sorted(tentative_distances.items(), key=lambda x: x[1]): ## FIXME: this is likely bad for performance
        if node[0] not in visited:
            return node[0]




def find_path(source, target, min_weight, edge_labels, edges):
    # we keep track of the nodes we have visited, and the tentative distance from source to each node
    visited = set()
    tentative_distances = { source : 0 }
    current = source
    while target not in visited and current is not None:
        for edge in edges:
            to = edge['to']
            if edge['from'] == current and edge['edge_weight'] >= min_weight and edge['edge_label'] in edge_labels:
                if to in tentative_distances:
                    tentative_distances[to] = min(tentative_distances[to], tentative_distances[current] + 1)
                else:
                    tentative_distances[to] = tentative_distances[current] + 1
        visited.add(current)

        current = get_next_node(tentative_distances, visited)

    # Returns None if no path found
    return tentative_distances.get(target)
