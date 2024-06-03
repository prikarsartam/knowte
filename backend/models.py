from pydantic import BaseModel
from typing import List, Dict

class Node(BaseModel):
    label: str

class NoteCreate(BaseModel):
    title: str
    nodes: List[Node] = []

class NoteResponse(BaseModel):
    title: str
    nodes: List[Dict[str, str]]
    edges: List[Dict[str, str]]
