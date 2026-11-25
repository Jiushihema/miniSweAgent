def schedule(deps: dict[str, list[str]]) -> list[str]:
    visited: set[str] = set()
    order: list[str] = []

    def dfs(node: str) -> None:
        if node in visited:
            return
        visited.add(node)
        for pre in deps.get(node, []):
            dfs(pre)
        order.append(node)

    for task in deps:
        dfs(task)
    return order
