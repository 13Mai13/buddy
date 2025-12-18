from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

@dataclass
class CodeUnit:
    id: int
    file_path: str
    unit_type: str          # "file" | "class" | "function" | "method" | "block"
    name: str               # "authenticate_user", "LoginService", etc.
    signature: str          # for funcs/methods, e.g. "authenticate_user(self, username, password)"
    docstring: str
    code_body: str
    parent_unit_id: Optional[int]
    metadata: Dict[str, Any]  # language, lineno, etc.

def create_syntax_aware_units(content: str, file_path: str = "") -> List[CodeUnit]:
    """
    Parse Python code and return syntax-aware units (classes, functions, methods)
    suitable for inserting into code_units_structural.
    """
    tree = ast.parse(content)
    lines = content.splitlines()
    units: List[CodeUnit] = []
    id_counter = 1
    parent_stack: List[Optional[int]] = []

    def get_source_segment(node: ast.AST) -> str:
        # Prefer lineno/end_lineno when available (Py3.8+)
        if hasattr(node, "lineno") and hasattr(node, "end_lineno") and getattr(node, "end_lineno") is not None:
            start = node.lineno - 1
            end = node.end_lineno
            return "\n".join(lines[start:end])
        try:
            return ast.get_source_segment(content, node) or ""
        except Exception:
            return ""

    def build_signature(node: ast.AST) -> str:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return ""
        args = []

        # positional args
        for arg in node.args.args:
            args.append(arg.arg)

        # *args
        if node.args.vararg:
            args.append("*" + node.args.vararg.arg)

        # kw-only args (we don't recover types/defaults here – keep it simple)
        for kw in node.args.kwonlyargs:
            args.append(kw.arg + "=...")

        # **kwargs
        if node.args.kwarg:
            args.append("**" + node.args.kwarg.arg)

        arglist = ", ".join(args)
        return f"{node.name}({arglist})"

    class Visitor(ast.NodeVisitor):
        def visit_ClassDef(self, node: ast.ClassDef):
            nonlocal id_counter
            unit_id = id_counter
            id_counter += 1

            parent_id = parent_stack[-1] if parent_stack else None
            doc = ast.get_docstring(node) or ""
            body_src = get_source_segment(node)

            units.append(
                CodeUnit(
                    id=unit_id,
                    file_path=file_path,
                    unit_type="class",
                    name=node.name,
                    signature=node.name,
                    docstring=doc,
                    code_body=body_src,
                    parent_unit_id=parent_id,
                    metadata={
                        "language": "python",
                        "lineno": getattr(node, "lineno", None),
                        "end_lineno": getattr(node, "end_lineno", None),
                    },
                )
            )

            # Methods inside this class will have parent_unit_id = this class
            parent_stack.append(unit_id)
            self.generic_visit(node)
            parent_stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef):
            nonlocal id_counter
            unit_id = id_counter
            id_counter += 1

            parent_id = parent_stack[-1] if parent_stack else None
            doc = ast.get_docstring(node) or ""
            body_src = get_source_segment(node)

            units.append(
                CodeUnit(
                    id=unit_id,
                    file_path=file_path,
                    unit_type="method" if parent_stack else "function",
                    name=node.name,
                    signature=build_signature(node),
                    docstring=doc,
                    code_body=body_src,
                    parent_unit_id=parent_id,
                    metadata={
                        "language": "python",
                        "lineno": getattr(node, "lineno", None),
                        "end_lineno": getattr(node, "end_lineno", None),
                        "is_async": False,
                    },
                )
            )

            parent_stack.append(unit_id)
            self.generic_visit(node)
            parent_stack.pop()

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            nonlocal id_counter
            unit_id = id_counter
            id_counter += 1

            parent_id = parent_stack[-1] if parent_stack else None
            doc = ast.get_docstring(node) or ""
            body_src = get_source_segment(node)

            units.append(
                CodeUnit(
                    id=unit_id,
                    file_path=file_path,
                    unit_type="method" if parent_stack else "function",
                    name=node.name,
                    signature="async " + build_signature(node),
                    docstring=doc,
                    code_body=body_src,
                    parent_unit_id=parent_id,
                    metadata={
                        "language": "python",
                        "lineno": getattr(node, "lineno", None),
                        "end_lineno": getattr(node, "end_lineno", None),
                        "is_async": True,
                    },
                )
            )

            parent_stack.append(unit_id)
            self.generic_visit(node)
            parent_stack.pop()

    Visitor().visit(tree)
    return units