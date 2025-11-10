// Create constraints and sample schema for assets graph
CREATE CONSTRAINT IF NOT EXISTS ON (s:Service) ASSERT s.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS ON (i:Infra) ASSERT i.id IS UNIQUE;

// Example indexes
CREATE INDEX IF NOT EXISTS FOR (n:Service) ON (n.type);
CREATE INDEX IF NOT EXISTS FOR (n:Infra) ON (n.type);

// Sample nodes
MERGE (a:Service {id: 'service-a', name: 'Service A', type: 'service', criticite: 'high'});
MERGE (b:Service {id: 'service-b', name: 'Service B', type: 'service', criticite: 'medium'});
MERGE (db:Infra {id: 'infra-db', name: 'Postgres DB', type: 'database', criticite: 'high'});

// Sample relations
MERGE (a)-[:DEPENDS_ON {weight: 1}]->(b);
MERGE (a)-[:DEPENDS_ON {weight: 2}]->(db);
