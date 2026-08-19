import os
import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def create_constraints(tx):
    queries = [
        """
        CREATE CONSTRAINT variant_id_unique IF NOT EXISTS
        FOR (v:Variant)
        REQUIRE v.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT gene_id_unique IF NOT EXISTS
        FOR (g:Gene)
        REQUIRE g.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT transcript_id_unique IF NOT EXISTS
        FOR (t:Transcript)
        REQUIRE t.id IS UNIQUE
        """
    ]

    for query in queries:
        tx.run(query)


def load_genes(tx, rows):
    for row in rows:
        tx.run(
            """
            MERGE (g:Gene {id: $gene_id})
            SET
                g.symbol = $gene_symbol,
                g.biotype = $biotype
            """,
            gene_id=row["gene_id"],
            gene_symbol=row["gene_symbol"],
            biotype=row["biotype"]
        )


def load_variants(tx, rows):
    for row in rows:
        tx.run(
            """
            MERGE (v:Variant {id: $variant_id})
            SET
                v.chrom = $chrom,
                v.pos = toInteger($pos),
                v.ref = $ref,
                v.alt = $alt,
                v.assembly = $assembly
            """,
            variant_id=row["variant_id"],
            chrom=row["chrom"],
            pos=row["pos"],
            ref=row["ref"],
            alt=row["alt"],
            assembly=row["assembly"]
        )


def load_variant_gene(tx, rows):
    for row in rows:
        tx.run(
            """
            MATCH (v:Variant {id: $variant_id})
            MATCH (g:Gene {id: $gene_id})

            MERGE (v)-[r:AFFECTS]->(g)

            SET
                r.impact = $impact,
                r.consequence = $consequence
            """,
            variant_id=row["variant_id"],
            gene_id=row["gene_id"],
            impact=row["impact"],
            consequence=row["consequence"]
        )


def load_transcripts(tx, rows):
    for row in rows:
        tx.run(
            """
            MERGE (t:Transcript {id: $transcript_id})
            SET
                t.biotype = $biotype

            WITH t
            MATCH (g:Gene {id: $gene_id})

            MERGE (g)-[:HAS_TRANSCRIPT]->(t)
            """,
            transcript_id=row["transcript_id"],
            gene_id=row["gene_id"],
            biotype=row["biotype"]
        )


def main():

    data_path = "data"

    variants = pd.read_csv(f"{data_path}/variants.csv")
    genes = pd.read_csv(f"{data_path}/genes.csv")
    variant_gene = pd.read_csv(f"{data_path}/variant_gene.csv")
    transcripts = pd.read_csv(f"{data_path}/transcripts.csv")

    with driver.session(database=DATABASE) as session:

        session.execute_write(create_constraints)

        session.execute_write(
            load_genes,
            genes.to_dict("records")
        )

        session.execute_write(
            load_variants,
            variants.to_dict("records")
        )

        session.execute_write(
            load_variant_gene,
            variant_gene.to_dict("records")
        )

        session.execute_write(
            load_transcripts,
            transcripts.to_dict("records")
        )

    print("Knowledge Graph created successfully.")


if __name__ == "__main__":
    main()
    driver.close()