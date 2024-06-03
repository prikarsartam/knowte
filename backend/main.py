from fastapi import FastAPI, HTTPException
from typing import List
from .models import Node, NoteCreate, NoteResponse
from .database import Neo4jHandler

app = FastAPI()
db_handler = Neo4jHandler("bolt://localhost:7687", "neo4j", "password")

@app.post("/notes/", response_model=NoteResponse)
def create_note_graph(note: NoteCreate):
    db_handler.add_note_graph(note.title, note.nodes)
    return NoteResponse(title=note.title, nodes=note.nodes, edges=[])

@app.get("/notes/{title}", response_model=NoteResponse)
def get_note_graph(title: str):
    result = db_handler.get_note_graph(title)
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteResponse(title=result["title"], nodes=result["nodes"], edges=[])

@app.get("/notes/", response_model=List[NoteResponse])
def get_all_notes():
    notes = db_handler.get_all_notes()
    return [NoteResponse(title=note['title'], nodes=note['nodes'], edges=[]) for note in notes]

@app.post("/notes/{title}/nodes", response_model=Node)
def add_node_to_graph(title: str, node: Node):
    db_handler.add_node_to_graph(title, node.label)
    return node



