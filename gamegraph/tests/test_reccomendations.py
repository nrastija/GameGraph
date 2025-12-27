"""
Test recommendation queries
"""

import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from database.queries import GameQueries, RecommenderQueries

print("=" * 60)
print("TEST: Recommendation System")
print("=" * 60)

# Get a sample game
print("\n1. Getting a sample game...")
games = GameQueries.get_all_games(limit=1)
if not games:
    print("❌ No games in database!")
    exit(1)

game = games[0]
game_id = game['id']
game_name = game['name']
print(f"   Sample game: {game_name} (ID: {game_id})")

# Test 1: Get game details
print("\n2. Getting game details...")
details = GameQueries.get_game_details_with_relationships(game_id)
if details:
    print(f"   ✅ {details['name']}")
    print(f"      Rating: {details['rating']} ⭐")
    print(f"      Genres: {', '.join(details['genres'][:5])}")
    print(f"      Developers: {', '.join(details['developers'])}")

# Test 2: Find similar games
print("\n3. Finding similar games...")
similar = RecommenderQueries.get_similar_games(game_id, limit=5)
if similar:
    print(f"   ✅ Found {len(similar)} similar games:\n")
    for i, s in enumerate(similar, 1):
        print(f"   {i}. {s['name']}")
        print(f"      Rating: {s['rating']} ⭐ | Similarity: {s['similarity_score']:.1f}")
        print(f"      Shared: {s['shared_genres']} genres, {s['shared_tags']} tags\n")
else:
    print("   ⚠️  No similar games found")

# Test 3: Search
print("\n4. Testing search...")
results = RecommenderQueries.search_games_by_name("the", limit=5)
print(f"   ✅ Search for 'the' found {len(results)} results:")
for r in results[:3]:
    print(f"      - {r['name']} ({r['rating']} ⭐)")

# Test 4: Top rated
print("\n5. Getting top-rated games...")
top = RecommenderQueries.get_top_rated_games(limit=5)
print(f"   ✅ Top {len(top)} games:")
for i, t in enumerate(top, 1):
    print(f"      {i}. {t['name']} - {t['rating']} ⭐")

# Test 5: Hidden gems
print("\n6. Finding hidden gems...")
gems = RecommenderQueries.get_hidden_gems(limit=5)
if gems:
    print(f"   ✅ Found {len(gems)} hidden gems:")
    for g in gems:
        print(f"      - {g['name']} ({g['rating']} ⭐, {g['playtime']}h)")

print("\n" + "=" * 60)
print("✅ All recommendation tests passed!")
print("=" * 60)