import os
from pathlib import Path


class Settings:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

    RAWG_API_KEY = os.getenv("RAWG_API_KEY", "")
    RAWG_BASE_URL = "https://api.rawg.io/api"

    APP_TITLE = "GameGraph"
    APP_DESCRIPTION = "Video Game Discovery and Editing System Through a Graph Database"
    PRIMARY_COLOR = "#1976D2"
    SECONDARY_COLOR = "#424242"

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    def __repr__(self):
        return f"<Settings app={self.APP_TITLE} debug={self.DEBUG}>"

    def ConfigDebugTest(self):
        print("=" * 50)
        print("SETTINGS TEST")
        print("=" * 50)

        print(f"App Title: {settings.APP_TITLE}")
        print(f"Debug Mode: {settings.DEBUG}")
        print(f"Base Directory: {settings.BASE_DIR}")
        print(f"Neo4j URI: {settings.NEO4J_URI}")
        print(f"Neo4j Username: {settings.NEO4J_USERNAME}")
        print(f"Neo4j Password: {'*' * len(settings.NEO4J_PASSWORD)}")  # Hide password
        print(f"RAWG API Key: {settings.RAWG_API_KEY[:10]}..." if settings.RAWG_API_KEY else "Not set")
        print(f"Log Level: {settings.LOG_LEVEL}")

        print("=" * 50)
        print("✅ Settings loaded successfully!")
        print(settings)

settings = Settings()

