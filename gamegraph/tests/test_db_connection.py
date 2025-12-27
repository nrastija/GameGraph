from database.connection import db

print("=" * 60)
print("TEST 1: Neo4j Connection")
print("=" * 60)

print("\n1. Testing connection...")
if db.verify_connectivity():
    print("   ✅ Connection successful!")
else:
    print("   ❌ Connection failed!")
    exit(1)

print("\n2. Getting database stats...")
stats = db.get_database_info()
print(f"   Nodes: {stats['nodes']}")
print(f"   Relationships: {stats['relationships']}")

print("\n3. Testing simple query...")
result = db.execute_query("RETURN 'Hello Neo4j!' as message, 42 as number")
print(f"   Result: {result}")

print("\n" + "=" * 60)
print("✅ All connection tests passed!")
print("=" * 60)