"""
RAWG API Client for fetching game data
"""
from pathlib import Path

import requests
from typing import Dict, Optional, Any, List
import os
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / '.env.py'
load_dotenv(dotenv_path=env_path)


class RAWGClient:

    def __init__(self, api_key: str):

        self.api_key = api_key
        self.base_url = "https://api.rawg.io/api"
        self.session = requests.Session()

        if not self.api_key:
            raise ValueError("RAWG_API_KEY not found in environment variables")

        print(f"✅ RAWG API client initialized")

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        params = params or {}
        params["key"] = self.api_key

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return {}

    def get_creator_roles(self) -> List[Dict[str, Any]]:
        data = self._make_request("creators")
        return data.get("results", [])

    def get_creators(self, _creatorID) -> List[Dict[str, Any]]:
        data = self._make_request(f"creators/{_creatorID}")
        return data.get("results", [])

    def get_developers(self) -> List[Dict[str, Any]]:
        data = self._make_request("developers")
        return data.get("results", [])

    def get_games(self) -> List[Dict[str, Any]]:
        data = self._make_request("games")
        return data.get("results", [])

    def get_genres(self) -> List[Dict[str, Any]]:
        data = self._make_request("genres")
        return data.get("results", [])

    def get_platforms(self) -> List[Dict[str, Any]]:
        data = self._make_request("platforms")
        return data.get("results", [])

    def get_publishers(self) -> List[Dict[str, Any]]:
        data = self._make_request("publishers")
        return data.get("results", [])

    def get_stores(self) -> List[Dict[str, Any]]:
        data = self._make_request("stores")
        return data.get("results", [])

    def get_tags(self) -> List[Dict[str, Any]]:
        data = self._make_request("tags")
        return data.get("results", [])

rawg_client = RAWGClient(
    api_key=os.getenv("RAWG_API_KEY", "")
)