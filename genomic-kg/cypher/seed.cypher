// Verify Variants
MATCH (v:Variant)
RETURN v
LIMIT 10;


// Verify Genes
MATCH (g:Gene)
RETURN g
LIMIT 10;


// Verify Transcripts
MATCH (t:Transcript)
RETURN t
LIMIT 10;


// Verify Variant → Gene relationships
MATCH (v:Variant)-[r:AFFECTS]->(g:Gene)
RETURN v, r, g
LIMIT 20;


// Verify complete genomic path
MATCH (v:Variant)-[:AFFECTS]->(g:Gene)-[:HAS_TRANSCRIPT]->(t:Transcript)
RETURN
    v.id AS variant,
    g.symbol AS gene,
    t.id AS transcript
LIMIT 20;