from nicegui import ui

def InfoPage(lat: float, lon: float):
    ui.leaflet(center=(lat, lon), zoom=10)
    ui.link('Back to table', '/')