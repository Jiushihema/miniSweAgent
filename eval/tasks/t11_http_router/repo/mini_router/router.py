from typing import Any


class Router:
    def __init__(self):
        self.routes: list[tuple[str, list[str], Any]] = []

    def add(self, method: str, path: str, handler: Any) -> None:
        segs = [s for s in path.split("/") if s]
        self.routes.append((method.upper(), segs, handler))

    def resolve(self, method: str, path: str) -> tuple[int, Any, dict[str, str]]:
        target = [s for s in path.split("/") if s]
        for r_method, r_segs, handler in self.routes:
            if r_method != method.upper() or len(r_segs) != len(target):
                continue
            params: dict[str, str] = {}
            matched = True
            for rs, ts in zip(r_segs, target):
                if rs.startswith(":"):
                    params[rs[1:]] = ts
                elif rs != ts:
                    matched = False
                    break
            if matched:
                return 200, handler, params
        return 404, None, {}
