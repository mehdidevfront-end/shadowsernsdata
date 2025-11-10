// CSV format expected: from_id,from_label,to_id,to_label,rel_type,rel_props_json
// Place the CSV in Neo4j import dir and run:
// cypher-shell -u <user> -p <pass> -f import_dependencies.cypher

USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///dependencies.csv' AS row
WITH row,
     apoc.convert.fromJsonMap(row.rel_props_json) AS rel_props
MERGE (a:Service {id: row.from_id})
SET a += apoc.convert.fromJsonMap(row.from_props_json)
MERGE (b:Service {id: row.to_id})
SET b += apoc.convert.fromJsonMap(row.to_props_json)
MERGE (a)-[r:DEPENDS_ON]->(b)
SET r += rel_props
