from nicegui import ui

def create_header():
    with ui.header().classes('items-center justify-between bg-blue-700'):
        with ui.row().classes('items-center gap-4'):
            ui.image('/static/Logo.png').classes('h-12 w-12 rounded')
            ui.label('GameGraph').classes('text-h5 text-white font-bold')

        with ui.row().classes('gap-2'):
            ui.link('Home', '/').classes('text-white hover:text-blue-200')
            ui.link('Browse', '/browse').classes('text-white hover:text-blue-200')
            ui.link('Search', '/search').classes('text-white hover:text-blue-200')
            ui.link('Recommendations', '/recommendations').classes('text-white hover:text-blue-200')
            ui.link('Analytics', '/analytics').classes('text-white hover:text-blue-200')
            ui.link('Info', '/info').classes('text-white hover:text-blue-200')