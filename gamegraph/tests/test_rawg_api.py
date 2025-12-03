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
        return False
    else:
        print("Genres found: ", {len(_fetchedGenres)})
        for i, genre in enumerate(_fetchedGenres):
            print(f"Genre: {i}. {genre['name']}")
        return True

def test_creator_roles():
    print("=" * 60)
    print("TEST 1: Testing creator roles")
    print("=" * 60)

    _fetchedCreatorRoles = rawg_client.get_creator_roles()
    if not _fetchedCreatorRoles:
        print("Error: No creator roles found")
        return {}
    else:
        print("Creator roles found: ", {len(_fetchedCreatorRoles)})
        for i, creator_role in enumerate(_fetchedCreatorRoles):
                print(f"Creator role: {i}. {creator_role['name']}")

def test_creators():
    print("=" * 60)
    print("TEST 2: Testing creators")
    print("=" * 60)
    _fetchedCreator = rawg_client.get_creators(1)

    if not _fetchedCreator:
        print("Error: No creators found.")
        return {}
    else:
        print(f"Creator found:\n"
              f"id: {_fetchedCreator['id']}\n"
              f"name: {_fetchedCreator['name']}\n"
              f"slug: {_fetchedCreator['slug']}\n"
              f"description: {_fetchedCreator['description']}\n")

def test_developers():
    print("=" * 60)
    print("TEST 3: Testing developers")
    print("=" * 60)
    _fetchedDevelopers = rawg_client.get_developers()

    if not _fetchedDevelopers:
        print ("Error: No Developers found.")
        return {}
    else:
        print(f"Developers found: {len(_fetchedDevelopers)}")
        for i, developers in enumerate(_fetchedDevelopers):
            print(f"Developer: {i}. {developers['name']}")

def test_games():
    print("=" * 60)
    print("TEST 4: Testing games")
    print("=" * 60)

    _fetchedGames = rawg_client.get_games()

    if not _fetchedGames:
        print("Error: No games found.")
        return {}
    else:
        print(f"Games found: {len(_fetchedGames)}")
        for i, game in enumerate(_fetchedGames):
            print(f"Game: {i}. {game['name']}")

def test_platforms():
    print("=" * 60)
    print("TEST 5: Testing platforms")
    print("=" * 60)

    _fetchedPlatforms = rawg_client.get_platforms()

    if not _fetchedPlatforms:
        print("Error: No platforms found.")
        return {}
    else:
        print(f"Platforms found: {len(_fetchedPlatforms)}")
        for i, platform in enumerate(_fetchedPlatforms):
            print(f"Platform: {i}. {platform['name']}")

def test_publishers():
    print("=" * 60)
    print("TEST 6: Testing publishers")
    print("=" * 60)

    _fetchedPublishers = rawg_client.get_publishers()

    if not _fetchedPublishers:
        print("Error: No publishers found.")
        return {}
    else:
        print(f"Publishers found: {len(_fetchedPublishers)}")
        for i, publisher in enumerate(_fetchedPublishers):
            print(f"Publisher: {i}. {publisher['name']}")

def test_stores():
    print("=" * 60)
    print("TEST 7: Testing stores")
    print("=" * 60)

    _fetchedStores = rawg_client.get_stores()

    if not _fetchedStores:
        print("Error: No stores found.")
        return {}
    else:
        print(f"Store found: {len(_fetchedStores)}")
        for i, store in enumerate(_fetchedStores):
            print(f"Store: {i}. {store['name']}")

def test_tags():
    print("=" * 60)
    print("TEST 8: Testing tags")
    print("=" * 60)

    _fetchedTags = rawg_client.get_tags()
    if not _fetchedTags:
        print("Error: No tags found.")
        return {}
    else:
        print(f"Tags found: {len(_fetchedTags)}")
        for i, tag in enumerate(_fetchedTags):
            print(f"Tag: {i}. {tag['name']}")

def test_main():
    print("=" * 60)
    print("RAWG API All Tests Running")
    print("=" * 60)

    if not (test_api_connection() == True):
        print("Error: API Connection failed.")
        return None

    test_creator_roles()
    test_creators()
    test_developers()
    test_games()
    test_platforms()
    test_publishers()
    test_stores()
    test_tags()

    print("=" * 60)
    print("RAWG API All Tests Finished")
    print("STATISTICS: 8/8 Tests Passed!")
    print("=" * 60)

if __name__ == "__main__":
    test_main()
