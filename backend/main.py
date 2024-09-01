from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import networkx as nx

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

class Node(BaseModel):
    id: str
    type: str

class Edge(BaseModel):
    id: str
    source: str
    target: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
async def parse_pipeline(pipeline: Pipeline):
    try:
        print("hello")
        num_nodes = len(pipeline.nodes)
        num_edges = len(pipeline.edges)

        G = nx.DiGraph()

        for node in pipeline.nodes:
            G.add_node(node.id)

        for edge in pipeline.edges:
            G.add_edge(edge.source, edge.target)

        is_dag = nx.is_directed_acyclic_graph(G)

        return {
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'is_dag': is_dag
        }
    except Exception as e:
        return {'error': str(e)}