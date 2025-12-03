from nicegui import ui, App
from ui.pages.RootPage import RootPage
from ui.pages.InfoPage import InfoPage

class UIApp(App):
    app_name = 'GameGraph'

    def setup_routes(self):
        @ui.page('/')
        def root_page():
            RootPage(200, 100)

        @ui.page('/info')
        def info_page():
            InfoPage(200, 100)

    def RunGUI(self):
        self.setup_routes()
        ui.run(
            title=self.app_name,
            port=8080,
            show=True
        )
