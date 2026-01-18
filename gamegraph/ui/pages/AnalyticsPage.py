from ui.components.header import create_header
from nicegui import ui
from database.queries import GameQueries

def analytic_page():
    create_header()

    with ui.column().classes('w-full max-w-7xl mx-auto p-8 gap-8 items-center'):
        stats = GameQueries.get_db_stats()
        ui.label('Database stats:').classes('text-h4 mt-2')

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
