from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from typing import Dict

# routers
from .routers import assets as assets_router
from .routers import risks as risks_router
from .storage import list_assets, list_risks
from .routers import qa as qa_router
from .routers import auth as auth_router
from .routers import stats as stats_router
from .graphql_schema import schema
try:
    from strawberry.fastapi import GraphQLRouter
except Exception:
    GraphQLRouter = None
from pydantic import BaseModel
from typing import List, Optional
from os import getenv

from neo4j import GraphDatabase

app = FastAPI(title="Security Platform API")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Allow CORS from frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(assets_router.router)
app.include_router(risks_router.router)
app.include_router(qa_router.router)


@app.get('/compliance')
async def compliance_kpis():
    # Simple KPI calculation sample
    assets = list_assets()
    risks = list_risks()
    total_assets = len(assets)
    total_risks = len(risks)
    high_risks = sum(1 for r in risks if r.get('severity') == 'high')
    return {
        'total_assets': total_assets,
        'total_risks': total_risks,
        'high_risks': high_risks,
        'rgpd_coverage': 0.85,  # placeholder
    }


@app.get('/finops')
async def finops_kpis():
    # Placeholder FinOps metrics
    return {
        'monthly_cloud_cost': 12345.67,
        'orphaned_assets_count': 7,
        'top_cost_services': [
            {'service': 'db-prod', 'cost': 4000},
            {'service': 'kafka', 'cost': 2500},
        ]
    }


# Include auth and stats routers
app.include_router(auth_router.router)
app.include_router(stats_router.router)

# mount GraphQL if available
if GraphQLRouter is not None and schema is not None:
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix='/graphql')

# Neo4j driver (configure via env: NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
NEO4J_URI = getenv('NEO4J_URI', 'bolt://neo4j:7687')
NEO4J_USER = getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = getenv('NEO4J_PASSWORD', '')
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


class LogItem(BaseModel):
    timestamp: str
    source: str
    level: str
    message: str


@app.post('/logs')
async def ingest_log(item: LogItem):
    # TODO: push to Kafka / store in OpenSearch
    return {"status": "accepted", "received": item}


@app.get('/logs')
async def list_logs(q: Optional[str] = None):
    # Placeholder: return empty list
    return []


@app.get('/graph/{asset}')
async def graph_asset(
    asset: str,
    type: Optional[str] = None,
    criticite: Optional[str] = None,
    bu: Optional[str] = None,
    env: Optional[str] = None,
):
    """
    Return incoming and outgoing DEPENDS_ON relations for an asset.
    Optional query params: type, criticite, bu, env to filter neighbour nodes.
    """
    results = {"asset": asset, "incoming": [], "outgoing": []}

    # Build filter clauses for outgoing (b) and incoming (c) nodes
    out_conds = []
    in_conds = []
    params = {"asset": asset}
    if type:
        out_conds.append("b.type = $type")
        in_conds.append("c.type = $type")
        params['type'] = type
    if criticite:
        out_conds.append("b.criticite = $criticite")
        in_conds.append("c.criticite = $criticite")
        params['criticite'] = criticite
    if bu:
        out_conds.append("b.bu = $bu")
        in_conds.append("c.bu = $bu")
        params['bu'] = bu
    if env:
        out_conds.append("b.env = $env")
        in_conds.append("c.env = $env")
        params['env'] = env

    q_out = "MATCH (a {id:$asset})-[r:DEPENDS_ON]->(b)"
    if out_conds:
        q_out += " WHERE " + " AND ".join(out_conds)
    q_out += " RETURN b.id as id, labels(b) as labels, b.type as type, b.criticite as criticite, r as rel"

    q_in = "MATCH (c)-[r:DEPENDS_ON]->(a {id:$asset})"
    if in_conds:
        q_in += " WHERE " + " AND ".join(in_conds)
    q_in += " RETURN c.id as id, labels(c) as labels, c.type as type, c.criticite as criticite, r as rel"

    try:
        with driver.session() as sess:
            for rec in sess.run(q_out, **params):
                rel_obj = {}
                if rec['rel'] is not None:
                    try:
                        rel_obj = dict(rec['rel'])
                    except Exception:
                        # fallback if rec['rel'] is already a mapping-like
                        rel_obj = rec['rel']
                results['outgoing'].append({
                    'id': rec['id'],
                    'labels': rec['labels'],
                    'type': rec.get('type'),
                    'criticite': rec.get('criticite'),
                    'rel': rel_obj,
                })
            for rec in sess.run(q_in, **params):
                rel_obj = {}
                if rec['rel'] is not None:
                    try:
                        rel_obj = dict(rec['rel'])
                    except Exception:
                        rel_obj = rec['rel']
                results['incoming'].append({
                    'id': rec['id'],
                    'labels': rec['labels'],
                    'type': rec.get('type'),
                    'criticite': rec.get('criticite'),
                    'rel': rel_obj,
                })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return results


@app.get('/assets')
async def list_assets():
    return []


@app.post('/predict')
async def predict_dummy(data: dict):
    # Placeholder for model inference
    return {"anomaly_score": 0.0}
