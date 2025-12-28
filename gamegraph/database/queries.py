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
        SET g.name = $name,
            g.slug = $slug,
            g.released = $released,
            g.rating = $rating,
            g.rating_top = $rating_top,
            g.metacritic = $metacritic,
            g.playtime = $playtime,
            g.background_image = $background_image,
            g.updated = datetime()
        """

        params = {
            'game_id': game_data.get('id'),
            'name': game_data.get('name', 'Unknown'),
            'slug': game_data.get('slug', ''),
            'released': game_data.get('released'),
            'rating': game_data.get('rating', 0.0),
            'rating_top': game_data.get('rating_top', 0),
            'metacritic': game_data.get('metacritic'),
            'playtime': game_data.get('playtime', 0),
            'background_image': game_data.get('background_image', None)
        }

        db.execute_write(query, params)

    @staticmethod
    def link_game_to_genres(game_id: int, genres: List[Dict[str, Any]]) -> None:
        for genre in genres:
            query = """
            MATCH (g:Game {id: $game_id})
            MERGE (gen:Genre {id: $genre_id})
            ON CREATE SET gen.name = $genre_name, gen.slug = $genre_slug
            MERGE (g)-[:HAS_GENRE]->(gen)
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
        for i, platform_data in enumerate(platforms):

            platform = platform_data.get('platform', {})

            query = """
            MATCH (g:Game {id: $game_id})
            MERGE (pl:Platform {id: $platform_id})
            ON CREATE SET pl.name = $platform_name, pl.slug = $platform_slug
            MERGE (g)-[:AVAILABLE_ON]->(pl)
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
            MATCH (g:Game {id: $game_id})
            MERGE (dev:Developer {id: $developer_id})
            ON CREATE SET dev.name = $developer_name, dev.slug = $developer_slug
            MERGE (g)-[:DEVELOPED_BY]->(dev)
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
            MERGE (g)-[:PUBLISHED_BY]->(p)
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
            MATCH (g:Game {id: $game_id})
            MERGE (t:Tag {id: $tag_id})
            ON CREATE SET t.name = $tag_name, t.slug = $tag_slug
            MERGE (g)-[:HAS_TAG]->(t)
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
        result = db.execute_query(query, {"game_id": game_id})
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

        return db.execute_query(query, {"limit": limit, "skip": skip})

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

    @staticmethod
    def get_game_details_with_relationships(game_id: int) -> Optional[Dict[str, Any]]:
        query = """
            MATCH (g:Game {id: $game_id})

            OPTIONAL MATCH (g)-[:HAS_GENRE]->(genre:Genre)
            OPTIONAL MATCH (g)-[:AVAILABLE_ON]->(platform:Platform)
            OPTIONAL MATCH (g)-[:DEVELOPED_BY]->(dev:Developer)
            OPTIONAL MATCH (g)-[:PUBLISHED_BY]->(pub:Publisher)
            OPTIONAL MATCH (g)-[:HAS_TAG]->(tag:Tag)

            RETURN g.id as id,
                   g.name as name,
                   g.slug as slug,
                   g.rating as rating,
                   g.rating_top as rating_top,
                   g.released as released,
                   g.metacritic as metacritic,
                   g.playtime as playtime,
                   g.background_image as image,
                   collect(DISTINCT genre.name) as genres,
                   collect(DISTINCT platform.name) as platforms,
                   collect(DISTINCT dev.name) as developers,
                   collect(DISTINCT pub.name) as publishers,
                   collect(DISTINCT tag.name) as tags
            """

        result = db.execute_query(query, {"game_id": game_id})
        return result[0] if result else None

    @staticmethod
    def get_games_by_genders():
        genres_query = """
                    MATCH (g:Genre)<-[:HAS_GENRE]-(game:Game)
                    WITH g.name as genre, COUNT(game) as game_count
                    WHERE game_count > 0
                    RETURN genre, game_count
                    ORDER BY game_count DESC
                    LIMIT 12
                    """

        genres = db.execute_query(genres_query)
        return genres

class DeveloperQueries:
    """Queries specific to developers"""

    @staticmethod
    def get_developer_games(developer_name: str):
        query = """
        MATCH (d:Developer {name: $name})<-[:DEVELOPED_BY]-(g:Game)
        RETURN g.id, g.name, g.rating
        ORDER BY g.rating DESC
        """
        return db.execute_query(query, {"name": developer_name})

    @staticmethod
    def get_top_developers(limit: int = 20):
        query = """
        MATCH (d:Developer)<-[:DEVELOPED_BY]-(g:Game)
        WITH d, COUNT(g) as game_count
        RETURN d.name, game_count
        ORDER BY game_count DESC
        LIMIT $limit
        """
        return db.execute_query(query, {"limit": limit})

class RecommenderQueries:
    """Queries for game recommendation system"""

    @staticmethod
    def get_similar_games(game_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        query = """
        MATCH (source:Game {id: $game_id})

        OPTIONAL MATCH (source)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (source)-[:HAS_TAG]->(t:Tag)
        WITH source, 
             source.name as source_name,
             collect(DISTINCT id(g)) as source_genres,
             collect(DISTINCT id(t)) as source_tags

        MATCH (similar:Game)
        WHERE similar <> source

        OPTIONAL MATCH (similar)-[:HAS_GENRE]->(sg:Genre)
        OPTIONAL MATCH (similar)-[:HAS_TAG]->(st:Tag)
        WITH source_name, similar,
             source_genres, source_tags,
             collect(DISTINCT id(sg)) as similar_genres,
             collect(DISTINCT id(st)) as similar_tags

        WITH source_name, similar,
             source_genres, source_tags,
             similar_genres, similar_tags,
             size([g IN source_genres WHERE g IN similar_genres]) as shared_genre_count,
             size([t IN source_tags WHERE t IN similar_tags]) as shared_tag_count

        // Jaccard similarity
        WITH source_name, similar,
             shared_genre_count,
             shared_tag_count,
             CASE 
                WHEN size(source_genres) = 0 OR size(similar_genres) = 0 THEN 0.0
                ELSE toFloat(shared_genre_count) / 
                     toFloat(size(source_genres + [g IN similar_genres WHERE NOT g IN source_genres]))
             END as genre_jaccard,
             CASE 
                WHEN size(source_tags) = 0 OR size(similar_tags) = 0 THEN 0.0
                ELSE toFloat(shared_tag_count) / 
                     toFloat(size(source_tags + [t IN similar_tags WHERE NOT t IN source_tags]))
             END as tag_jaccard

        OPTIONAL MATCH (source:Game {id: $game_id})-[:DEVELOPED_BY]->(dev:Developer)<-[:DEVELOPED_BY]-(similar)

        WITH similar,
             shared_genre_count,
             shared_tag_count,
             genre_jaccard,
             tag_jaccard,
             CASE WHEN dev IS NOT NULL THEN 1 ELSE 0 END as same_dev,
             CASE 
                WHEN toLower(similar.name) CONTAINS toLower(split(source_name, ':')[0])
                THEN 1 ELSE 0
             END as is_franchise

        WITH similar,
             shared_genre_count,
             shared_tag_count,
             genre_jaccard,
             tag_jaccard,
             same_dev,
             is_franchise,
             CASE 
                WHEN is_franchise = 1 
                THEN 0.95
                ELSE (genre_jaccard * 0.5 + tag_jaccard * 0.3 + same_dev * 0.2)
             END as similarity

        WHERE similarity > 0.1

        RETURN similar.id as id,
               similar.name as name,
               similar.rating as rating,
               similar.released as released,
               similar.background_image as image,
               similar.metacritic as metacritic,
               shared_genre_count,  // ✅ Return counts
               shared_tag_count,    // ✅ Return counts
               same_dev,
               is_franchise,
               ROUND(similarity * 100) as similarity_percentage
        ORDER BY similarity DESC, similar.rating DESC
        LIMIT $limit
        """

        return db.execute_query(query, {"game_id": game_id, "limit": limit})

    @staticmethod
    def get_recommendations_for_multiple_games(game_ids: List[int], limit: int = 10) -> List[Dict[str, Any]]:
        query = """
        MATCH (liked:Game) WHERE liked.id IN $game_ids
        OPTIONAL MATCH (liked)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (liked)-[:HAS_TAG]->(t:Tag)
        WITH collect(DISTINCT id(g)) as liked_genres,
             collect(DISTINCT id(t)) as liked_tags,
             collect(DISTINCT liked) as liked_games

        MATCH (recommended:Game)
        WHERE NOT recommended.id IN $game_ids

        OPTIONAL MATCH (recommended)-[:HAS_GENRE]->(rg:Genre)
        OPTIONAL MATCH (recommended)-[:HAS_TAG]->(rt:Tag)
        WITH recommended,
             liked_genres,
             liked_tags,
             collect(DISTINCT id(rg)) as rec_genres,
             collect(DISTINCT id(rt)) as rec_tags

        WITH recommended,
             size([g IN liked_genres WHERE g IN rec_genres]) as shared_genre_count,
             size([t IN liked_tags WHERE t IN rec_tags]) as shared_tag_count,
             liked_genres,
             liked_tags,
             rec_genres,
             rec_tags

        // Jaccard similarity
        WITH recommended,
             shared_genre_count,
             shared_tag_count,
             CASE 
                WHEN size(liked_genres) = 0 OR size(rec_genres) = 0 THEN 0.0
                ELSE toFloat(shared_genre_count) / 
                     toFloat(size(liked_genres + [g IN rec_genres WHERE NOT g IN liked_genres]))
             END as genre_jaccard,
             CASE 
                WHEN size(liked_tags) = 0 OR size(rec_tags) = 0 THEN 0.0
                ELSE toFloat(shared_tag_count) / 
                     toFloat(size(liked_tags + [t IN rec_tags WHERE NOT t IN liked_tags]))
             END as tag_jaccard

        WITH recommended,
             shared_genre_count,
             shared_tag_count,
             genre_jaccard,
             tag_jaccard,
             (genre_jaccard * 0.6 + tag_jaccard * 0.4) as similarity

        WHERE similarity > 0.15

        RETURN recommended.id as id,
               recommended.name as name,
               recommended.rating as rating,
               recommended.released as released,
               recommended.background_image as image,
               recommended.metacritic as metacritic,
               shared_genre_count,
               shared_tag_count,
               ROUND(similarity * 100) as similarity_percentage
        ORDER BY similarity DESC, recommended.rating DESC
        LIMIT $limit
        """

        return db.execute_query(query, {"game_ids": game_ids, "limit": limit})

    @staticmethod
    def get_top_rated_games(limit: int = 20, min_rating: float = 4.0) -> List[Dict[str, Any]]:
        query = """
            MATCH (g:Game)
            WHERE g.rating >= $min_rating

            RETURN g.id as id,
                   g.name as name,
                   g.rating as rating,
                   g.released as released,
                   g.background_image as image,
                   g.metacritic as metacritic
            ORDER BY g.rating DESC, g.metacritic DESC
            LIMIT $limit
            """

        return db.execute_query(query, {
            "min_rating": min_rating,
            "limit": limit
        })

    @staticmethod
    def search_games_by_name(search_query: str, limit: int = 20) -> List[Dict[str, Any]]:
        query = """
            MATCH (g:Game)
            WHERE toLower(g.name) CONTAINS toLower($search_query)

            RETURN g.id as id,
                   g.name as name,
                   g.rating as rating,
                   g.released as released,
                   g.background_image as image,
                   g.metacritic as metacritic
            ORDER BY g.rating DESC
            LIMIT $limit
            """

        return db.execute_query(query, {
            "search_query": search_query,
            "limit": limit
        })

    @staticmethod
    def get_trending_games(days: int = 365, limit: int = 20) -> List[Dict[str, Any]]:
        query = """
            MATCH (g:Game)
            WHERE g.released IS NOT NULL 
              AND g.rating >= 4.0
              AND date(g.released) >= date() - duration({days: $days})

            RETURN g.id as id,
                   g.name as name,
                   g.rating as rating,
                   g.released as released,
                   g.background_image as image,
                   g.metacritic as metacritic
            ORDER BY g.released DESC, g.rating DESC
            LIMIT $limit
            """

        return db.execute_query(query, {
            "days": days,
            "limit": limit
        })

    @staticmethod
    def get_hidden_gems(max_playtime: int = 20, min_rating: float = 4.2, limit: int = 20) -> List[Dict[str, Any]]:
        #  highly rated games with shorter playtime

        query = """
            MATCH (g:Game)
            WHERE g.playtime <= $max_playtime
              AND g.rating >= $min_rating
              AND g.playtime > 0

            RETURN g.id as id,
                   g.name as name,
                   g.rating as rating,
                   g.playtime as playtime,
                   g.released as released,
                   g.background_image as image,
                   g.metacritic as metacritic
            ORDER BY g.rating DESC, g.playtime ASC
            LIMIT $limit
            """

        return db.execute_query(query, {
            "max_playtime": max_playtime,
            "min_rating": min_rating,
            "limit": limit
        })