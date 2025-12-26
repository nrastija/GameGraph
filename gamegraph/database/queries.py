from typing import List, Dict, Any, Optional
from database.connection import db

class GameQueries:
    """
    Business logic for querying neo4j database
    WHAT to do to interact with db
    """
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

        db.execute_query(query, params)

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

            db.execute_query(query, params)


