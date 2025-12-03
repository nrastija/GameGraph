"""
RAWG API Client for fetching game data
"""
from pathlib import Path

import requests
from typing import Dict, Optional, Any
import os
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / '.env.py'
load_dotenv(dotenv_path=env_path)


class RAWGClient:
    """
    Client for interacting with RAWG Video Games Database API
    Documentation: https://api.rawg.io/docs/
    """

    def __init__(self, api_key: str):
        """
        Initialize RAWG API client

        Args:
            api_key: RAWG API key
        """
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



rawg_client = RAWGClient(
    api_key=os.getenv("RAWG_API_KEY", "")
)