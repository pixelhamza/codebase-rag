import ast
from dataclasses import dataclass
from typing import Optional

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


with open("scratch_test.py") as f:
    text = f.read()

tree = ast.parse(text)
file_lines = text.splitlines()
visitor = ChunkVisitor(file_lines, "scratch_test.py")
visitor.visit(tree)   

for chunk in visitor.chunks:
    print(chunk)