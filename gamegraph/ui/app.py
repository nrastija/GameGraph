from pathlib import Path

from nicegui import ui, App, app


class UIApp(App):
    def __init__(self):
        self.app_name = "GameGraph"
        self.app_description = "Project: Video Game Discovery Through Neo4J Graph Database"
        self.primary_color = '#1976D2'
        self.secondary_color = '#424242'
        self.setup_routes()
        self.setup_static_files()


    def setup_routes(self):
        from ui.pages import (
            HomePage,
            BrowsePage,
            SearchPage,
            RecommendationsPage,
            AnalyticsPage,
            InfoPage
        )

        @ui.page('/')
        def root_page():
            HomePage.home_page()

        @ui.page('/browse')
        def browse_page():
            BrowsePage.browse_page()

        @ui.page('/search')
        def search_page():
            SearchPage.search_page()

        @ui.page('/recommendations')
        def recommendations_page():
            RecommendationsPage.reccomendation_page()

        @ui.page('/analytics')
        def analytics_page():
            AnalyticsPage.analytic_page()

        @ui.page('/info')
        def info_page():
            InfoPage.info_page()

    def setup_static_files(self):
        static_dir = Path(__file__).parent.parent.parent / 'static'
        app.add_static_files('/static', static_dir)

    def RunGUI(self):
        ui.run(
            title=self.app_name,
            port=8080,
            host='0.0.0.0',
            reload=True,
            show=True,
            favicon='🎮' # emoji
        )
