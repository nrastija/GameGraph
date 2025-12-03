
from config.settings import settings

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