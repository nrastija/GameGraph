"""
Game card component for displaying game information
"""

from nicegui import ui
from typing import Dict, Any


def create_game_card(game: Dict[str, Any], show_similarity: bool = False):
    with ui.card().classes('w-64 h-96 cursor-pointer hover:shadow-lg transition-shadow'):
        if game.get('image'):
            ui.image(game['image']).classes('w-full h-36 object-cover')
        else:
            with ui.element('div').classes('w-full h-36 bg-gray-300 flex items-center justify-center'):
                ui.label('No Image').classes('text-gray-600')

        with ui.card_section():
            ui.label(game.get('name', 'Unknown')).classes('text-lg font-bold line-clamp-2')

            rating = game.get('rating', 0)
            with ui.row().classes('items-center gap-2 mt-2'):
                ui.label(f"⭐ {rating:.2f}").classes('text-yellow-600 font-semibold')

                if game.get('metacritic'):
                    ui.label(f"MC: {game['metacritic']}").classes('text-sm text-gray-600')


            if game.get('released'):
                ui.label(f"Released: {game['released']}").classes('text-sm text-gray-600 mt-1')
            else:
                ui.label(f"Release date not specified").classes('text-sm text-gray-600 mt-1')

            if show_similarity:
                if game.get('similarity_percentage'):
                    percentage = game['similarity_percentage']
                    ui.label(f"{percentage}% Match").classes('text-sm text-green-600 font-semibold mt-2')

                match_details = []

                if game.get('shared_genre_count') and game['shared_genre_count'] > 0:
                    count = game['shared_genre_count']
                    match_details.append(f"{count} shared genre{'s' if count > 1 else ''}")

                if game.get('shared_tag_count') and game['shared_tag_count'] > 0:
                    count = game['shared_tag_count']
                    match_details.append(f"{count} shared tag{'s' if count > 1 else ''}")

                if game.get('same_dev') and game['same_dev'] == 1:
                    match_details.append("same developer")

                if game.get('is_franchise') and game['is_franchise'] == 1:
                    match_details.append("same franchise")

                if match_details:
                    for detail in match_details:
                        ui.label(f"• {detail}").classes('text-xs text-gray-500')

        with ui.card_actions().classes('mt-auto'):
            ui.button('View Details',
                      on_click=lambda g=game: ui.navigate.to(f'/game/{g["id"]}')).classes('w-full')