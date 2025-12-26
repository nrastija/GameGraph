from typing import List, Dict, Any, Optional
from database.connection import db

class GameQueries:
    """
    Business logic for querying neo4j database
    WHAT to do to interact with db
    """

    @staticmethod
    def create_or_update_game(game_data: Dict[str, Any]) -> None:
        query = """
        MERGE (g:Game {id: $game_id})
        SET g.name = $name
            g.slug = $slug
            g.released = $released
            g.rating = $rating
            g.rating_top = $rating_top
            g.metacritic = $metacritic
            g.playtime = $playtime
            g.background_image = $background_image
            g.updated = datetime()
        RETURN 
        """

        params = {
            'id': game_data.get('id'),
            'name': game_data.get('name', 'Unknown'),
            'slug': game_data.get('slug', ''),
            'released': game_data.get('released'),
            'rating': game_data.get('rating', 0.0),
            'rating_top': game_data.get('rating_top', 0),
            'metacritic': game_data.get('metacritic'),
            'playtime': game_data.get('playtime', 0),
            'background_image': game_data.get('background_image', None),
        }

        db.execute_write(query, params)

    @staticmethod
    def link_game_to_genres(game_id: int, genres: List[Dict[str, Any]]) -> None:
        for genre in genres:
            query = """
            MATCH (g:Game {id: game_id})
            MERGE (gen:Genre {id: $genre_id})
            ON CREATE SET gen.name = $genre_name, gen.slug = $genre_slug
            MERGE g-[:HAS GENRE]->(gen)
            """

            params = {
                "game_id": game_id,
                "genre_id": genre.get('id'),
                "genre_name": genre.get('name'),
                "genre_slug": genre.get('slug'),
            }

            db.execute_write(query, params)

    @staticmethod
    def link_game_to_platforms(game_id:int, platforms: List[Dict[str, Any]]) -> None:
        for platform in platforms:
            query = """
            MATCH (g:Game {id: game_id})
            MERGE (pl:Platform {id: $platform_id})
            ON CREATE SET pl.name = $platform_name, pl.slug = $platform_slug
            MERGE pl-[:AVAILABLE ON]->(pl)
            """

            params = {
                "game_id": game_id,
                "platform_id": platform.get('id'),
                "platform_name": platform.get('name'),
                "platform_slug": platform.get('slug'),
            }

            db.execute_write(query, params)

    @staticmethod
    def link_game_to_developers(game_id: int, developers: List[Dict[str, Any]]) -> None:
        for developer in developers:
            query = """
            MATCH (g:Game {id:game_id})
            MERGE (dev:Developer {id: $developer_id})
            ON CREATE SET dev.name = $developer_name, dev.slug = $developer_slug
            MERGE dev-[:DEVELOPED BY]->(dev)
            """

            params = {
                "game_id": game_id,
                "developer_id": developer.get('id'),
                "developer_name": developer.get('name'),
                "developer_slug": developer.get('slug'),
            }

            db.execute_write(query, params)

    @staticmethod
    def link_game_to_publishers(game_id: int, publishers: List[Dict[str, Any]]) -> None:
        for publisher in publishers:
            query = """
            MATCH (g:Game {id: $game_id})
            MERGE (p:Publisher {id: $publisher_id})
            ON CREATE SET p.name = $publisher_name, p.slug = $publisher_slug
            MERGE p-[:PUBLISHED BY]->(p)
            """

            params = {
                "game_id": game_id,
                "publisher_id": publisher.get('id'),
                "publisher_name": publisher.get('name'),
                "publisher_slug": publisher.get('slug'),
            }

            db.execute_write(query, params)

    @staticmethod
    def link_game_to_tags(game_id: int, tags: List[Dict[str,Any]]) -> None:
        for tag in tags:
            query = """
            MATCH (g:Game {id: game_id})
            MERGE (t:Tag {id: $tag_id})
            ON CREATE SET t.name = $tag_name, t.slug = $tag_slug
            MERGE t-[:HAS TAG]->(t)
            """

            params = {
                "game_id": game_id,
                "tag_id": tag.get('id'),
                "tag_name": tag.get('name'),
                "tag_slug": tag.get('slug'),
            }

            db.execute_write(query, params)

    @staticmethod
    def game_exists(game_id: int) -> bool:
        query = "MATCH (g:Game {id: $game_id}) RETURN count(g) AS count"
        result = db.execute_write(query, {"game_id": game_id})
        return result[0]['count'] > 0

    @staticmethod
    def get_all_games(limit: int = 20, skip: int = 0) -> List[Dict[str, Any]]:
        query = """
        MATCH (g:Game)
        RETURN g.id as id, g.name as name, g.rating as rating, g.released as released, g.background_image as image, g.metacritic as metacritic
        ORDER BY g.rating DESC 
        SKIP $skip
        LIMIT $limit
        """

        return db.execute_write(query, {"limit": limit, "skip": skip})

    @staticmethod
    def get_db_stats() -> Dict[str, int]:
        query = """
            MATCH (g:Game) WITH COUNT(g) as game_count
            MATCH (d:Developer) WITH game_count, COUNT(d) as dev_count
            MATCH (gen:Genre) WITH game_count, dev_count, COUNT(gen) as genre_count
            MATCH (pl:Platform) WITH game_count, dev_count, genre_count, COUNT(pl) as platform_count
            MATCH (p:Publisher) WITH game_count, dev_count, genre_count, platform_count, COUNT(p) as pub_count
            MATCH (t:Tag) WITH game_count, dev_count, genre_count, platform_count, pub_count, COUNT(t) as tag_count
            RETURN game_count, dev_count, genre_count, platform_count, pub_count, tag_count
            """
        result = db.execute_query(query)
        if result:
            return result[0]
        return {
            "game_count": 0,
            "dev_count": 0,
            "genre_count": 0,
            "platform_count": 0,
            "pub_count": 0,
            "tag_count": 0
        }