
from nicegui import ui

from database import GameQueries, RecommenderQueries, db
from ui.components.game_card import create_game_card
from ui.components.header import create_header

def home_page():
    create_header()

    with ui.column().classes('w-full max-w-7xl mx-auto p-8 gap-8'):
        with ui.card().classes('w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white p-8 items-center'):
             ui.image('/static/Logo.png').classes('h-64 w-64 rounded')
             ui.label('Discover Your Next Favorite Game').classes('text-h3 mt-2')

    with ui.column().classes('w-full max-w-7xl mx-auto p-8 gap-8 items-center'):
        stats = GameQueries.get_db_stats()
        ui.label('Database stats:').classes('text-h6 mt-2')

        with ui.row().classes('gap-8 mt-6'):
            with ui.column().classes('items-center'):
                ui.label(str(stats.get('game_count', 0))).classes('text-h4 font-bold')
                ui.label('Games').classes('text-subtitle2 opacity-80')

            with ui.column().classes('items-center'):
                ui.label(str(stats.get('genre_count', 0))).classes('text-h4 font-bold')
                ui.label('Genres').classes('text-subtitle2 opacity-80')

            with ui.column().classes('items-center'):
                ui.label(str(stats.get('dev_count', 0))).classes('text-h4 font-bold')
                ui.label('Developers').classes('text-subtitle2 opacity-80')

            with ui.column().classes('items-center'):
                ui.label(str(stats.get('pub_count', 0))).classes('text-h4 font-bold')
                ui.label('Publishers').classes('text-subtitle2 opacity-80')

            with ui.column().classes('items-center'):
                ui.label(str(stats.get('platform_count', 0))).classes('text-h4 font-bold')
                ui.label('Platforms').classes('text-subtitle2 opacity-80')

            with ui.column().classes('items-center'):
                ui.label(str(stats.get('tag_count', 0))).classes('text-h4 font-bold')
                ui.label('Tags').classes('text-subtitle2 opacity-80')

        ui.button(
            'Open Neo4j Browser',
            on_click=lambda: ui.run_javascript('window.open("http://localhost:7474/browser/", "_blank")'),
            icon='open_in_new'
        ).props('size=xl color=primary').classes('px-8 py-4')

    with ui.card().classes('w-full max-w-7xl mx-auto p-8 gap-8'):

        with ui.column().classes('w-full'):
            with ui.row().classes('items-center justify-between w-full mb-4'):
                ui.label('Top Rated Games').classes('text-h5')
                ui.button('View All', on_click=lambda: ui.navigate.to('/browse')).props('flat color=primary')

            top_games = RecommenderQueries.get_top_rated_games(limit=8)

            if top_games:
                with ui.row().classes('gap-4 flex-wrap'):
                    for game in top_games:
                        create_game_card(game)
            else:
                ui.label('No games found').classes('text-gray-500')

    with ui.card().classes('w-full max-w-7xl mx-auto p-8 gap-8'):

        with ui.column().classes('w-full'):
            ui.label('Browse by Genre').classes('text-h5 mb-4')

            genres = GameQueries.get_games_by_genders()

            if genres:
                with ui.row().classes('gap-3 flex-wrap'):
                    for genre_data in genres:
                        genre_name = genre_data['genre']
                        count = genre_data['game_count']

                        # Genre card
                        with ui.card().classes('cursor-pointer hover:shadow-lg transition-shadow'):
                            with ui.card_section().classes('text-center p-4'):
                                ui.label(genre_name).classes('text-lg font-bold')
                                ui.label(f'{count} games').classes('text-sm text-gray-600')

                            # Click handler
                            ui.button('Explore',
                                      on_click=lambda g=genre_name: ui.navigate.to(f'/browse?genre={g}')
                                      ).classes('w-full').props('flat')
        with ui.card().classes('w-full bg-gray-50'):
            ui.label('Ready to discover more?').classes('text-h6 mb-4')

            with ui.row().classes('gap-4'):
                ui.button('Browse All Games',
                          on_click=lambda: ui.navigate.to('/browse'),
                          icon='grid_view'
                          ).props('size=lg color=primary')

                ui.button('Get Recommendations',
                          on_click=lambda: ui.navigate.to('/recommendations'),
                          icon='stars'
                          ).props('size=lg color=secondary')

                ui.button('View Analytics',
                          on_click=lambda: ui.navigate.to('/analytics'),
                          icon='analytics'
                          ).props('size=lg')

    with ui.footer().classes('bg-gray-800 text-white p-4'):
        with ui.row().classes('w-full max-w-7xl mx-auto justify-between items-center'):
            ui.label('GameGraph - © Niko Rastija 2025.').classes('text-sm')

            with ui.row().classes('gap-4'):
                ui.link('Neo4j Docs', 'https://neo4j.com/docs/', new_tab=True).classes('text-blue-300 text-sm')
                ui.link('NiceGUI', 'https://nicegui.io/', new_tab=True).classes('text-blue-300 text-sm')
                ui.link('RAWG API docs', 'https://api.rawg.io/docs/', new_tab=True).classes('text-blue-300 text-sm')

