// Unique identifiers for genomic entities

CREATE CONSTRAINT variant_id_unique IF NOT EXISTS
FOR (v:Variant)
REQUIRE v.id IS UNIQUE;

CREATE CONSTRAINT gene_id_unique IF NOT EXISTS
FOR (g:Gene)
REQUIRE g.id IS UNIQUE;

CREATE CONSTRAINT transcript_id_unique IF NOT EXISTS
FOR (t:Transcript)
REQUIRE t.id IS UNIQUE;