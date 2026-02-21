
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from collections import defaultdict
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# ✅ CORS (Allow frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Models
# -----------------------------

class Pipeline(BaseModel):
    nodes: List[Dict]
    edges: List[Dict]

# -----------------------------
# DAG Check Function (FINAL)
# -----------------------------

def is_dag(nodes, edges):
    node_ids = {node["id"] for node in nodes}

    graph = defaultdict(list)
    indegree = {node_id: 0 for node_id in node_ids}

    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")

        # Only consider valid node-to-node edges
        if source in node_ids and target in node_ids:
            graph[source].append(target)
            indegree[target] += 1

    # Kahn's Algorithm
    queue = [node for node in indegree if indegree[node] == 0]
    visited = 0

    while queue:
        current = queue.pop(0)
        visited += 1

        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return visited == len(node_ids)

# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def read_root():
    return {"Ping": "Pong"}

@app.post("/pipelines/parse")
def parse_pipeline(pipeline: Pipeline):

    print("=== NODES ===")
    for n in pipeline.nodes:
        print(n["id"])

    print("=== EDGES ===")
    for e in pipeline.edges:
        print(e["source"], "→", e["target"])

    return {
        "num_nodes": len(pipeline.nodes),
        "num_edges": len(pipeline.edges),
        "is_dag": is_dag(pipeline.nodes, pipeline.edges),
    }