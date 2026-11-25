from .lexer import tokenize


class Parser:
    def __init__(self, tokens: list[tuple[str, str]]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> str | None:
        return self.tokens[self.pos][0] if self.pos < len(self.tokens) else None

    def consume(self) -> tuple[str, str]:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self) -> float:
        val = self.expr()
        if self.pos != len(self.tokens):
            raise ValueError("Unexpected trailing tokens")
        return val

    def expr(self) -> float:
        left = self.term()
        while self.peek() in ("+", "-"):
            op = self.consume()[0]
            right = self.term()
            left = left + right if op == "+" else left - right
        return left

    def term(self) -> float:
        left = self.unary()
        while self.peek() in ("*", "/"):
            op = self.consume()[0]
            right = self.unary()
            left = left * right if op == "*" else left / right
        return left

    def unary(self) -> float:
        if self.peek() == "-":
            self.consume()
            return -self.unary()
        return self.primary()

    def primary(self) -> float:
        tok_type, tok_val = self.consume()
        if tok_type == "NUM":
            return float(tok_val) if "." in tok_val else int(tok_val)
        if tok_type == "(":
            val = self.expr()
            if self.peek() != ")":
                raise ValueError("Missing closing paren")
            self.consume()
            return val
        raise ValueError(f"Unexpected token: {tok_type}")


def evaluate(text: str) -> float:
    return Parser(tokenize(text)).parse()
