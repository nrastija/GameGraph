"""
Import game data from RAWG API into Neo4j database
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.rawg_client import rawg_client
from database.queries import GameQueries
from database.connection import db
import time
from datetime import datetime
import json


class GameImporter:
    """Import games from RAWG API to Neo4j"""

    def __init__(self):
        self.imported_games = set()
        self.skipped_games = set()
        self.failed_games = set()
        self.api_calls = 0
        self.start_time = None

        self.cache_dir = project_root / "data" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cached_game(self, game_id: int) -> dict:
        cache_file = self.cache_dir / f"game_{game_id}.json"

        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)

        return None

    def _cache_game(self, game_id: int, game_data: dict):
        cache_file = self.cache_dir / f"game_{game_id}.json"

        with open(cache_file, 'w') as f:
            json.dump(game_data, f, indent=2)

    def import_game(self, game_id: int, use_cache: bool = True) -> bool:
        if GameQueries.game_exists(game_id):
            self.skipped_games.add(game_id)
            return False

        try:
            game_data = None
            if use_cache:
                game_data = self._get_cached_game(game_id)
                if game_data:
                    print(f"[cached]", end=" ")

            if not game_data:
                game_data = rawg_client.get_game(game_id)
                self.api_calls += 1

                if game_data:
                    self._cache_game(game_id, game_data)

                time.sleep(1.5)

            if not game_data or 'id' not in game_data:
                print(f"No data")
                self.failed_games.add(game_id)
                return False

            GameQueries.create_or_update_game(game_data)

            if game_data.get('genres'):
                GameQueries.link_game_to_genres(game_id, game_data['genres'])

            if game_data.get('platforms'):
                GameQueries.link_game_to_platforms(game_id, game_data['platforms'])

            if game_data.get('developers'):
                GameQueries.link_game_to_developers(game_id, game_data['developers'])

            if game_data.get('publishers'):
                GameQueries.link_game_to_publishers(game_id, game_data['publishers'])

            if game_data.get('tags'):
                GameQueries.link_game_to_tags(game_id, game_data['tags'])

            self.imported_games.add(game_id)
            return True

        except Exception as e:
            print(f"Error: {e}")
            self.failed_games.add(game_id)
            return False

    def import_top_games(self, count: int = 500, ordering: str = "-rating"):
        print(f"\n{'=' * 60}")
        print(f"📥 IMPORTING TOP {count} GAMES (ordered by {ordering})")
        print(f"{'=' * 60}\n")

        self.start_time = datetime.now()

        page = 1
        page_size = 40
        imported = 0

        while imported < count:
            print(f"\nPage {page}: Fetching games...", end=" ")

            try:
                response = rawg_client.get_games(
                    page=page,
                    page_size=page_size,
                    ordering=ordering
                )

                self.api_calls += 1

                if not response or 'results' not in response:
                    print("Error: no response for games.")
                    break

                games = response['results']

                if not games:
                    print("Error: no games fetched.")
                    break

                print(f"({len(games)} games)")

            except Exception as e:
                print(f"Error: {e}")
                break

            for game_data in games:
                if imported >= count:
                    break

                game_id = game_data['id']
                game_name = game_data.get('name', 'Unknown')

                if GameQueries.game_exists(game_id):
                    print(f"  ⏭️  {imported + 1}/{count}: {game_name} (exists)")
                    self.skipped_games.add(game_id)
                    continue

                print(f" {imported + 1}/{count}: {game_name}...", end=" ")

                if self.import_game(game_id):
                    imported += 1
                    print("✅")
                else:
                    print("⏭️")

                if imported > 0 and imported % 50 == 0:
                    self._print_progress(imported, count)

            page += 1
            time.sleep(0.5)

        self._print_summary(imported)

    def _print_progress(self, current: int, total: int):
        elapsed = (datetime.now() - self.start_time).total_seconds()
        rate = current / elapsed if elapsed > 0 else 0
        remaining = (total - current) / rate if rate > 0 else 0

        print(f"\n{'=' * 60}")
        print(f"📊 PROGRESS UPDATE")
        print(f"{'=' * 60}")
        print(f"Imported:  {current}/{total} ({current / total * 100:.1f}%)")
        print(f"API Calls: {self.api_calls}")
        print(f"Rate:      {rate:.1f} games/second")
        print(f"Est. time remaining: {remaining / 60:.1f} minutes")
        print(f"{'=' * 60}\n")

    def _print_summary(self, imported: int):
        elapsed = (datetime.now() - self.start_time).total_seconds()

        print(f"\n{'=' * 60}")
        print(f"✅ IMPORT COMPLETE")
        print(f"{'=' * 60}")
        print(f"Successfully imported: {len(self.imported_games)} games")
        print(f"Skipped (existing):    {len(self.skipped_games)} games")
        print(f"Failed:                {len(self.failed_games)} games")
        print(f"API calls used:        {self.api_calls}")
        print(f"Total time:            {elapsed / 60:.1f} minutes")
        if self.imported_games:
            print(f"Average rate:          {len(self.imported_games) / elapsed:.2f} games/sec")
        print(f"{'=' * 60}\n")

        stats = GameQueries.get_db_stats()

        print(f"{'=' * 60}")
        print(f"📊 DATABASE STATISTICS")
        print(f"{'=' * 60}")
        print(f"Total Games:      {stats.get('game_count', 0)}")
        print(f"Total Developers: {stats.get('dev_count', 0)}")
        print(f"Total Publishers: {stats.get('pub_count', 0)}")
        print(f"Total Genres:     {stats.get('genre_count', 0)}")
        print(f"Total Platforms:  {stats.get('platform_count', 0)}")
        print(f"Total Tags:       {stats.get('tag_count', 0)}")

        db_stats = db.get_database_info()
        print(f"\nTotal Nodes:         {db_stats.get('nodes', 0)}")
        print(f"Total Relationships: {db_stats.get('relationships', 0)}")
        print(f"{'=' * 60}\n")


def main():
    print("\n" + "=" * 60)
    print("🎮 GAMEGRAPH - DATA IMPORT")
    print("=" * 60)
    print("Source: RAWG Video Games Database API")
    print("Target: Neo4j Graph Database")
    print("=" * 60 + "\n")

    print("Verifying connections...")

    if not db.verify_connectivity():
        print("Cannot connect to Neo4j!")
        return

    print("Neo4j connection OK")

    if not rawg_client.api_key:
        print("RAWG API key not found!")
        return

    print(" RAWG API key OK\n")

    print("How many games would you like to import?")
    print("  1. Small dataset (100 games) - ~5 minutes")
    print("  2. Medium dataset (500 games) - ~15 minutes")
    print("  3. Large dataset (1000 games) - ~30 minutes")
    print("  4. Custom amount")

    choice = input("\nChoice (1-4): ").strip()

    counts = {
        '1': 100,
        '2': 500,
        '3': 1000
    }

    if choice in counts:
        count = counts[choice]
    elif choice == '4':
        try:
            count = int(input("Enter number of games: ").strip())
        except ValueError:
            print("Invalid number, using 100")
            count = 100
    else:
        print("Invalid choice, using 100")
        count = 100

    print(f"\n About to import {count} games")
    print(f"This will use approximately {count + count // 40 + 6} API requests")
    print(f"Estimated time: {count * 2 / 60:.0f} minutes")

    confirm = input("\nProceed? (yes/no): ").strip().lower()

    if confirm != 'yes':
        print("Import cancelled")
        return

    importer = GameImporter()
    importer.import_top_games(count=count, ordering="-rating")

    print("\n All done!")
    print("- View in Neo4j Browser: http://localhost:7474")

if __name__ == "__main__":
    try:
        main()
    finally:
        db.close()