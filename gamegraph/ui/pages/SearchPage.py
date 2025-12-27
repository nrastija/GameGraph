from nicegui import ui
from ui.components.header import create_header

def search_page():
    create_header()

    with ui.column().classes('w-full max-w-7xl mx-auto p-8 gap-8'):

        with ui.card().classes('w-full max-w-7xl mx-auto p-8 gap-8'):
            ui.label('Find Your Game').classes('text-h5 mb-4')

            # Search input
            search_container = ui.column().classes('w-full')

            with search_container:
                search_input = ui.input(
                    placeholder='Search by game name (e.g., "Witcher", "Portal")...',
                ).classes('w-full').props('clearable')

                # Search button
                ui.button('Search',
                          on_click=lambda: perform_search(search_input.value, search_results)
                          ).classes('mt-2')

                # Search results
                search_results = ui.column().classes('w-full mt-4')

    with ui.footer().classes('bg-gray-800 text-white p-4'):
        with ui.row().classes('w-full max-w-7xl mx-auto justify-between items-center'):
            ui.label('GameGraph - © Niko Rastija 2025.').classes('text-sm')

            with ui.row().classes('gap-4'):
                ui.link('Neo4j Docs', 'https://neo4j.com/docs/', new_tab=True).classes('text-blue-300 text-sm')
                ui.link('NiceGUI', 'https://nicegui.io/', new_tab=True).classes('text-blue-300 text-sm')
                ui.link('RAWG API docs', 'https://api.rawg.io/docs/', new_tab=True).classes('text-blue-300 text-sm')

    def perform_search(query: str):
        pass