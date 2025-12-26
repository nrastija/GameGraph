import os
from pathlib import Path
from typing import List, Optional, Dict, Any

from dotenv import load_dotenv
from neo4j import GraphDatabase

env_path = Path(__file__).parent.parent / '.env.py'
load_dotenv(dotenv_path=env_path)

class Neo4JConnection:
    """
    Low level connection to Neo4j database
    HOW to interact with db
    """
    def __init__(self, uri: str, username: str, password: str):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = None

        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(username, password)
            )
            print(f"Connected to Neo4j database at {self.uri}")
        except Exception as e:
            print(f"Failed to connect to Neo4j database: {e}")
            raise

    def close(self):
        if self.driver is not None:
            self.driver.close()
            print(f"Disconnected from Neo4j database.")

    def execute_query(self, query: str, parameters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [dict(record) for record in result]
        except Exception as e:
            print(f"Query execution failed: {e}")
            raise

    def execute_write(self, query: str, parameters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        try:
            with self.driver.session() as session:
                session.run(query, parameters or {})
        except Exception as e:
            print(f"Query execution failed: {e}")
            raise

    def clear_database(self):
        try:
            with self.driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
                print(f"Cleared NEO4J database.")
        except Exception as e:
            print(f"Error while clearing NEO4J database: {e}")
            raise

    def get_database_info(self) -> Dict[str, Any]:
        try:
            with self.driver.session() as session:
                node_result = session.run("MATCH (n) RETURN count(n) as count")
                node_count = node_result.single()["count"]

                relationship_result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
                relationship_count = relationship_result.single()["count"]

                return {
                    "nodes": node_count,
                    "relationships": relationship_count
                }
        except Exception as e:
            print(f"Error while getting database info: {e}")
            return {"nodes": 0, "relationships": 0}

db = Neo4JConnection(
    uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    username=os.getenv("NEO4J_USERNAME", "neo4j"),
    password=os.getenv("NEO4J_PASSWORD", "password")
)