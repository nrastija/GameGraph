from nicegui import ui

def RootPage(lat: float, lon: float):
    ui.label('MAIN LABEL')
    ui.link('InfoPage', '/info')