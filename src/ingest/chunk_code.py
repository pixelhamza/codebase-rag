import ast
from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import sys, json
from dataclasses import asdict

@dataclass
class CodeChunk:
    id: str
    file_path: str
    qualified_name: str
    kind: str
    start_line: int
    end_line: int
    docstring: Optional[str]
    source: str

class ChunkVisitor(ast.NodeVisitor):
    def __init__(self,file_lines: list[str], file_path: str):
        self.class_stack = []
        self.file_lines = file_lines
        self.file_path = file_path
        self.chunks = [] #collect chunked objects here


    def visit_ClassDef(self, node):
        self.class_stack.append(node.name) #pushing node name onto stack
        self.generic_visit(node)  #recursively visit node
        self.class_stack.pop() #pop it when done 

    def visit_FunctionDef(self, node):
        kind = "method" if self.class_stack else "function"
        qualified_name = ".".join(self.class_stack + [node.name])

        source = "\n".join(
        self.file_lines[node.lineno - 1 : node.end_lineno]
        )
        docstring = ast.get_docstring(node)

        chunk = CodeChunk(
        id=f"{self.file_path}::{qualified_name}",
        file_path=self.file_path,
        qualified_name=qualified_name,
        kind=kind,
        start_line=node.lineno,
        end_line=node.end_lineno,
        docstring=docstring,
        source=source,
        )

        self.chunks.append(chunk)

        self.generic_visit(node);


    def visit_AsyncFunctionDef(self, node):
        # separate node type from FunctionDef as async def doesnt trigger the other one
        kind = "async_method" if self.class_stack else "async_function"
        qualified_name = ".".join(self.class_stack + [node.name])

        source = "\n".join(
        self.file_lines[node.lineno - 1 : node.end_lineno]
        )
        docstring = ast.get_docstring(node)

        chunk = CodeChunk(
        id=f"{self.file_path}::{qualified_name}",
        file_path=self.file_path,
        qualified_name=qualified_name,
        kind=kind,
        start_line=node.lineno,
        end_line=node.end_lineno,
        docstring=docstring,
        source=source,
        )
        
        self.chunks.append(chunk)

        self.generic_visit(node);



EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "venv"}

def chunk_repo(repo_root: Path) -> list[CodeChunk]:
    all_chunks = []

    for path in repo_root.rglob("*.py"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue

        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)

        file_lines = text.splitlines()
        relative_path = str(path.relative_to(repo_root))

        visitor = ChunkVisitor(file_lines, relative_path)
        visitor.visit(tree)

        all_chunks.extend(visitor.chunks)

    return all_chunks


if __name__ == "__main__":
    repo_root = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    chunks = chunk_repo(repo_root)

    with open(output_path, "w") as f:
        for chunk in chunks:
            f.write(json.dumps(asdict(chunk)) + "\n")

    print(f"Wrote {len(chunks)} chunks to {output_path}")