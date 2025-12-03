"""
Test file with integration tests for testing connection to RAWG API in api/rawg_client.py
"""

from api.rawg_client import rawg_client
import json

def test_api_connection():
    print("=" * 60)
    print("Testing connection to RAWG API")
    print("=" * 60)

    _fetchedGenres = rawg_client.get_genres()

    if not _fetchedGenres:
        print("Error: No genres found")
        return {}
    else:
        print("Genres found: ", {len(_fetchedGenres)})
        for i, genre in enumerate(_fetchedGenres):
            print(f"Genre: {i}. {genre['name']}")
        return _fetchedGenres

def test_main():
    print("=" * 60)
    print("RAWG API All Tests Running")
    print("=" * 60)

if __name__ == "__main__":
    test_api_connection()
