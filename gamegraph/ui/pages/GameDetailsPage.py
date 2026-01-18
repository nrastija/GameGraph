from nicegui import ui

from database import RecommenderQueries, GameQueries
from ui.components.header import create_header


def game_details_page(game_id: int):
    create_header()

    game = GameQueries.get_game_details_with_relationships(game_id)

    if not game:
        with ui.column().classes('w-full max-w-7xl mx-auto p-8'):
            with ui.card().classes('w-full p-12 text-center'):
                ui.icon('error_outline', size='xl').classes('text-red-500 mb-4')
                ui.label('Game Not Found').classes('text-h4 mb-4')
                ui.label(f'Game with ID {game_id} does not exist').classes('text-gray-600 mb-6')
                ui.button('Back to Home', on_click=lambda: ui.navigate.to('/')).props('color=primary')
        return

    with ui.column().classes('w-full max-w-7xl mx-auto p-8 gap-6'):


        with ui.card().classes('w-full'):
            with ui.row().classes('w-full gap-6'):
                if game.get('image'):
                    ui.image(game['image']).classes('w-80 h-64 object-cover rounded-lg')
                else:
                    with ui.element('div').classes('w-80 h-64 bg-gray-300 rounded-lg flex items-center justify-center'):
                        ui.icon('videogame_asset', size='xl').classes('text-gray-400')

                with ui.column().classes('flex-grow gap-4'):
                    ui.label(game['name']).classes('text-h3 font-bold')

                    with ui.row().classes('items-center gap-4'):
                        if game.get('rating'):
                            with ui.card().classes('bg-yellow-50 px-4 py-2'):
                                with ui.row().classes('items-center gap-2'):
                                    ui.icon('star', size='md').classes('text-yellow-500')
                                    ui.label(f"{game['rating']:.2f}").classes('text-h5 font-bold text-yellow-700')
                                    ui.label('/ 5.0').classes('text-sm text-gray-600')

                        if game.get('metacritic'):
                            with ui.card().classes('bg-green-50 px-4 py-2'):
                                ui.label('Metacritic').classes('text-xs text-gray-600')
                                ui.label(str(game['metacritic'])).classes('text-h5 font-bold text-green-700')

                    if game.get('released'):
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('calendar_today', size='sm').classes('text-gray-500')
                            ui.label(f"Released: {game['released']}").classes('text-lg text-gray-700')

                    if game.get('playtime') and game['playtime'] > 0:
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('schedule', size='sm').classes('text-gray-500')
                            ui.label(f"Average playtime: {game['playtime']} hours").classes('text-lg text-gray-700')


        if game.get('genres'):
            with ui.card().classes('w-full'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('category', size='md').classes('text-purple-600')
                    ui.label('Genres').classes('text-h5 font-bold')

                with ui.row().classes('gap-2 flex-wrap'):
                    for genre in game['genres']:
                        ui.chip(genre, icon='category').props('color=purple')

        if game.get('platforms'):
            with ui.card().classes('w-full'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('devices', size='md').classes('text-blue-600')
                    ui.label('Available On').classes('text-h5 font-bold')

                with ui.row().classes('gap-2 flex-wrap'):
                    for platform in game['platforms']:
                        ui.chip(platform, icon='devices').props('color=blue')

        with ui.row().classes('w-full gap-4'):
            if game.get('developers'):
                with ui.card().classes('flex-1'):
                    with ui.row().classes('items-center gap-2 mb-3'):
                        ui.icon('code', size='md').classes('text-green-600')
                        ui.label('Developers').classes('text-h6 font-bold')

                    with ui.column().classes('gap-1'):
                        for dev in game['developers']:
                            ui.label(dev).classes('text-gray-700')

            if game.get('publishers'):
                with ui.card().classes('flex-1'):
                    with ui.row().classes('items-center gap-2 mb-3'):
                        ui.icon('business', size='md').classes('text-orange-600')
                        ui.label('Publishers').classes('text-h6 font-bold')

                    with ui.column().classes('gap-1'):
                        for pub in game['publishers']:
                            ui.label(pub).classes('text-gray-700')

        if game.get('tags'):
            with ui.card().classes('w-full'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('label', size='md').classes('text-pink-600')
                    ui.label('Tags').classes('text-h5 font-bold')

                with ui.row().classes('gap-2 flex-wrap'):
                    for tag in game['tags'][:20]:  # Limit to first 20 tags
                        ui.chip(tag).props('size=sm outline')