// Current genomic knowledge graph schema
//
// Variant ──AFFECTS──> Gene ──HAS_TRANSCRIPT──> Transcript
//
// AFFECTS relationship properties:
//   - impact
//   - consequence

CREATE INDEX variant_position IF NOT EXISTS
FOR (v:Variant)
ON (v.chrom, v.pos);

CREATE INDEX gene_symbol IF NOT EXISTS
FOR (g:Gene)
ON (g.symbol);