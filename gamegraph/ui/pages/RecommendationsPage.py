
from nicegui import ui

from database import RecommenderQueries
from ui.components.game_card import create_game_card
from ui.components.header import create_header

def reccomendation_page():
    create_header()

    selected_game = {'value': None}

    with ui.column().classes('w-full max-w-7xl mx-auto p-8 gap-8'):
        with ui.card().classes('w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white p-8 items-center'):
            ui.label('Recommender system for your next game!').classes('text-h3 mt-2')

        # Method 1
        with ui.card().classes('w-full'):
            with ui.row().classes('w-full items-center gap-4 mb-4 p-4 bg-blue-50 rounded'):
                ui.icon('search', size='lg').classes('text-blue-600')
                ui.label('Method 1: Find Similar Games').classes('text-h5 font-bold')

            ui.label('Type a game name to search and find similar recommendations').classes('text-gray-600 mb-4')

            autocomplete_options = {'value': []}

            search_input = ui.input(
                placeholder='Start typing a game name (e.g., "Witcher", "Portal", "Zelda")...',
            ).classes('w-full').props('clearable outlined')

            autocomplete_container = ui.column().classes('w-full mt-2')

            selected_game_container = ui.column().classes('w-full mt-6')

            similar_games_container = ui.column().classes('w-full mt-8')

            search_input.on('update:model-value',
                            lambda e: handle_autocomplete_search(
                                search_input.value,
                                autocomplete_container,
                                selected_game,
                                selected_game_container,
                                similar_games_container
                            )
                            )

        # Method 2
        with ui.card().classes('w-full'):
            with ui.row().classes('w-full items-center gap-4 mb-4 p-4 bg-green-50 rounded'):
                ui.icon('library_add', size='lg').classes('text-green-600')
                ui.label('Method 2: Multiple Games').classes('text-h5 font-bold')

            ui.label('Select 2-5 games you enjoyed, then get personalized recommendations').classes(
                'text-gray-600 mb-4')

            selected_games_list = []

            search_input_2 = ui.input(
                placeholder='Search to add games...',
            ).classes('w-full mb-4').props('clearable outlined')

            with ui.card().classes('w-full bg-blue-50 p-4 mb-4'):
                ui.label('Selected Games (2-5):').classes('font-semibold mb-2')
                selected_display_2 = ui.row().classes('gap-2 flex-wrap')

                with selected_display_2:
                    ui.label('No games selected yet').classes('text-gray-500 italic')

            search_results_2 = ui.column().classes('w-full mb-4')

            recommend_button_2 = ui.button(
                'Get Recommendations',
                on_click=lambda: show_multi_game_recommendations(
                    selected_games_list,
                    recommendations_container_2
                ),
                icon='stars'
            ).props('color=primary size=lg').classes('w-full')

            recommendations_container_2 = ui.column().classes('w-full mt-6')

            search_input_2.on('update:model-value',
                              lambda: handle_multi_search(
                                  search_input_2.value,
                                  search_results_2,
                                  selected_games_list,
                                  selected_display_2,
                                  recommend_button_2,
                                  search_input_2
                              )
                              )

        # Method 3
        with ui.card().classes('w-full'):
            with ui.row().classes('w-full items-center gap-4 mb-4 p-4 rounded'):
                ui.label('Method 3: Genre-Based!').classes('text-h5 font-bold')


# Method 1

def handle_autocomplete_search(query, dropdown_container, selected_game, selected_container, similar_container):

    dropdown_container.clear()

    if not query or len(query) < 2:
        return

    games = RecommenderQueries.search_games_by_name(query, limit=10)

    with dropdown_container:
        if games:
            with ui.card().classes('w-full border shadow-lg'):
                ui.label(f'{len(games)} results:').classes('text-sm font-semibold p-2 bg-gray-50')

                for game in games:
                    with ui.row().classes('w-full items-center p-3 hover:bg-blue-50 cursor-pointer').on('click',
                                                                                                        lambda g=game: select_game(
                                                                                                            g,
                                                                                                            selected_game,
                                                                                                            selected_container,
                                                                                                            similar_container,
                                                                                                            dropdown_container
                                                                                                            )
                                                                                                        ):
                        if game.get('image'):
                            ui.image(game['image']).classes('w-16 h-16 object-cover rounded')
                        else:
                            with ui.element('div').classes(
                                    'w-16 h-16 bg-gray-200 rounded flex items-center justify-center'):
                                ui.icon('videogame_asset').classes('text-gray-400')

                        with ui.column().classes('flex-grow ml-4'):
                            ui.label(game['name']).classes('font-semibold')

                            with ui.row().classes('items-center gap-2'):
                                ui.label(f"⭐ {game.get('rating', 0):.2f}").classes('text-yellow-600 text-sm')

                                if game.get('released'):
                                    ui.label(f"• {game['released'][:4]}").classes('text-gray-600 text-sm')

                                if game.get('metacritic'):
                                    ui.label(f"• MC: {game['metacritic']}").classes('text-gray-600 text-sm')

                        ui.icon('chevron_right').classes('text-gray-400')

                    ui.separator()
        else:
            with ui.card().classes('w-full border p-4'):
                ui.label('No games found').classes('text-gray-500 text-center')
                ui.label(f'Try a different search term').classes('text-sm text-gray-400 text-center')


def select_game(game, selected_game_state, selected_container, similar_container, dropdown_container):
    dropdown_container.clear()

    selected_game_state['value'] = game

    show_selected_game(game, selected_container, selected_game_state, similar_container)

    show_similar_games(game, similar_container)


def show_selected_game(game, container, selected_game_state, similar_container):
    container.clear()

    with container:
        ui.separator().classes('my-6')

        with ui.card().classes('w-full bg-blue-50 p-6'):
            with ui.row().classes('w-full items-center justify-between'):
                with ui.row().classes('items-center gap-4'):
                    ui.icon('check_circle', size='lg').classes('text-green-600')

                    with ui.column():
                        ui.label('Selected Game:').classes('text-sm text-gray-600')
                        ui.label(game['name']).classes('text-h5 font-bold')

                        with ui.row().classes('items-center gap-2 mt-2'):
                            ui.label(f"⭐ {game.get('rating', 0):.2f}").classes('text-yellow-600 font-semibold')

                            if game.get('metacritic'):
                                ui.label(f"MC: {game['metacritic']}").classes('text-gray-600')

                            if game.get('released'):
                                ui.label(f"Released: {game['released']}").classes('text-gray-600')

                # Change selection button
                ui.button(
                    'Change Selection',
                    on_click=lambda: clear_selection(selected_game_state, container, similar_container),
                    icon='refresh'
                ).props('outline')


def clear_selection(selected_game_state, selected_container, similar_container):
    selected_game_state['value'] = None
    selected_container.clear()
    similar_container.clear()

    ui.notify('Selection cleared', type='info')


def show_similar_games(game, container):

    container.clear()

    with container:
        ui.separator().classes('my-6')

        with ui.card().classes('w-full bg-gradient-to-r from-green-600 to-blue-600 text-white p-6'):
            ui.icon('stars', size='lg').classes('mb-2')
            ui.label(f'Games Similar to: {game["name"]}').classes('text-h5 font-bold')
            ui.label('Based on shared genres, tags, and developers').classes('text-subtitle1 mt-2 opacity-90')


        similar_games = RecommenderQueries.get_similar_games(game['id'], limit=20)

        container.clear()

        with container:
            ui.separator().classes('my-6')

            with ui.card().classes('w-full bg-gradient-to-r from-green-600 to-blue-600 text-white p-6'):
                ui.label(f'Games Similar to: {game["name"]}').classes('text-h5 font-bold')
                ui.label('Based on Jaccard similarity - measures overlap relative to total unique features').classes('text-xs text-gray-500 italic mb-4')

            if similar_games:
                ui.label(f'Found {len(similar_games)} similar games').classes('text-lg font-semibold mt-6 mb-4')

                with ui.row().classes('gap-4 flex-wrap'):
                    for sim_game in similar_games:
                        sim_game_with_score = sim_game.copy()

                        create_game_card(sim_game_with_score, show_similarity=True)
            else:
                with ui.column().classes('w-full items-center p-12 gap-4'):
                    ui.icon('search_off', size='xl').classes('text-gray-400')
                    ui.label('No similar games found').classes('text-h6 text-gray-600')
                    ui.label('This game might be very unique!').classes('text-sm text-gray-500')

# Method 2

def handle_multi_search(query, results_container, selected_list, display_container, button, search_input):
    results_container.clear()

    if not query or len(query) < 2:
        return

    games = RecommenderQueries.search_games_by_name(query, limit=10)

    with results_container:
        if games:
            with ui.card().classes('w-full border shadow-lg'):
                ui.label(f'{len(games)} results - Click to add:').classes('text-sm font-semibold p-2 bg-gray-50')

                for game in games:
                    already_selected = any(g['id'] == game['id'] for g in selected_list)

                    if already_selected:
                        with ui.row().classes('w-full items-center p-3 bg-gray-100 opacity-50'):
                            if game.get('image'):
                                ui.image(game['image']).classes('w-12 h-12 object-cover rounded')
                            else:
                                with ui.element('div').classes(
                                        'w-12 h-12 bg-gray-200 rounded flex items-center justify-center'):
                                    ui.icon('videogame_asset').classes('text-gray-400')

                            with ui.column().classes('flex-grow ml-4'):
                                ui.label(game['name']).classes('text-sm text-gray-600')
                                ui.label('Already selected').classes('text-xs text-gray-500 italic')
                    else:
                        with ui.row().classes('w-full items-center p-3 hover:bg-green-50 cursor-pointer').on('click',
                                                                                                             lambda g=game: add_game_to_selection(
                                                                                                                 g,
                                                                                                                 selected_list,
                                                                                                                 display_container,
                                                                                                                 button,
                                                                                                                 results_container,
                                                                                                                 search_input
                                                                                                             )
                                                                                                             ):
                            if game.get('image'):
                                ui.image(game['image']).classes('w-12 h-12 object-cover rounded')
                            else:
                                with ui.element('div').classes(
                                        'w-12 h-12 bg-gray-200 rounded flex items-center justify-center'):
                                    ui.icon('videogame_asset').classes('text-gray-400')

                            with ui.column().classes('flex-grow ml-4'):
                                ui.label(game['name']).classes('font-semibold text-sm')

                                with ui.row().classes('items-center gap-2'):
                                    ui.label(f"⭐ {game.get('rating', 0):.2f}").classes('text-yellow-600 text-xs')

                                    if game.get('released'):
                                        ui.label(f"• {game['released'][:4]}").classes('text-gray-600 text-xs')

                            ui.icon('add_circle', size='sm').classes('text-green-600')

                    ui.separator()


def add_game_to_selection(game, selected_list, display_container, button, results_container, search_input):
    if len(selected_list) >= 5:
        ui.notify('Maximum 5 games allowed', type='warning')
        return

    selected_list.append(game)

    update_selected_display(selected_list, display_container, button)

    search_input.value = ''
    results_container.clear()

    ui.notify(f'✓ Added: {game["name"]}', type='positive')


def update_selected_display(selected_list, display_container, button):
    display_container.clear()

    with display_container:
        if not selected_list:
            ui.label('No games selected yet').classes('text-gray-500 italic')
        else:
            for game in selected_list:
                with ui.card().classes('p-2 bg-white hover:shadow-md transition-shadow'):
                    with ui.row().classes('items-center gap-2'):
                        if game.get('image'):
                            ui.image(game['image']).classes('w-10 h-10 object-cover rounded')
                        else:
                            with ui.element('div').classes(
                                    'w-10 h-10 bg-gray-200 rounded flex items-center justify-center'):
                                ui.icon('videogame_asset', size='sm').classes('text-gray-400')

                        with ui.column().classes('flex-grow'):
                            ui.label(game['name']).classes('text-sm font-semibold')
                            ui.label(f"⭐ {game.get('rating', 0):.2f}").classes('text-xs text-yellow-600')

                        ui.button(
                            icon='close',
                            on_click=lambda g=game: remove_from_selection(g, selected_list, display_container, button)
                        ).props('flat dense round size=sm color=red')

    button.set_enabled(len(selected_list) >= 2)


def remove_from_selection(game, selected_list, display_container, button):
    selected_list.remove(game)
    update_selected_display(selected_list, display_container, button)
    ui.notify(f'Removed: {game["name"]}', type='info')


def show_multi_game_recommendations(selected_games, recommendations_container):

    recommendations_container.clear()

    if len(selected_games) < 2:
        with recommendations_container:
            ui.label('Please select at least 2 games').classes('text-gray-500')
        return

    game_ids = [g['id'] for g in selected_games]

    with recommendations_container:
        ui.separator().classes('my-6')

        with ui.card().classes('w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6'):
            ui.label(f' Recommendations Based on {len(selected_games)} Games').classes('text-h5 font-bold')

            with ui.row().classes('gap-2 flex-wrap mt-3'):
                for game in selected_games:
                    with ui.chip(game['name']).props('color=blue text-color=primary'):
                        pass

    recommendations = RecommenderQueries.get_recommendations_for_multiple_games(game_ids, limit=20)

    recommendations_container.clear()

    with recommendations_container:
        ui.separator().classes('my-6')

        with ui.card().classes('w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6'):
            ui.label(f'🎯 Recommendations Based on {len(selected_games)} Games').classes('text-h5 font-bold')

            with ui.row().classes('gap-2 flex-wrap mt-3'):
                for game in selected_games:
                    with ui.chip(game['name'], icon='check').props('color=white text-color=primary'):
                        pass

        if recommendations:
            ui.label(f'Found {len(recommendations)} recommended games').classes('text-lg font-semibold mt-6 mb-4')

            with ui.row().classes('gap-4 flex-wrap'):
                for rec_game in recommendations:
                    create_game_card(rec_game, show_similarity=True)
        else:
            with ui.column().classes('w-full items-center p-12 gap-4'):
                ui.icon('search_off', size='xl').classes('text-gray-400')
                ui.label('No recommendations found').classes('text-h6 text-gray-600')
                ui.label('Try selecting different games').classes('text-sm text-gray-500')




