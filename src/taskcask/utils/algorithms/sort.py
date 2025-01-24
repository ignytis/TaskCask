class CircularReferenceException(Exception):
    def __init__(self, stack: list[str], *args):
        super().__init__(*args)
        self.stack = stack


def sort_topological(graph: dict[str, list[str]]):
    """
    Topological sort.
    Accepts a dicionary where each string key is parent (dependent)
    and value is a list of strings (dependencies).
    Returns a sorted list where parent elements are followed by children.
    """

    # Dictionary to keep track of visited status: 0 - not visited, 1 - visiting, 2 - visited
    visited = {}
    stack = []

    def dfs(node):
        if visited.get(node) == 1:
            raise CircularReferenceException([node])

        # If node has not been visited before, mark it as visiting
        if visited.get(node) == 0:
            visited[node] = 1  # Mark as visiting
            for neighbor in graph[node]:
                try:
                    dfs(neighbor)
                except CircularReferenceException as e:
                    raise CircularReferenceException([node] + e.stack)
            visited[node] = 2  # Mark as visited
            stack.append(node)

    # Initialize all nodes as not visited
    for node in graph:
        visited[node] = 0

    # Perform DFS for all nodes not yet visited
    for node in graph:
        if visited[node] == 0:
            dfs(node)

    return stack
