
from nicegui import ui
from ui.components.game_card import create_game_card
from ui.components.header import create_header


def browse_page():
    create_header()

    current_page = {'value': 1}
    items_per_page = 24

    with ui.column().classes('w-full max-w-7xl mx-auto p-8 gap-8'):
        ui.label('Browse Games').classes('text-h4 mb-4')

        with ui.card().classes('w-full mb-6'):
            ui.label('Filters').classes('text-h6 mb-4')

            with ui.row().classes('gap-4 items-center'):
                sort_select = ui.select(
                    label='Sort by',
                    options={
                        '-rating': 'Rating (High to Low)',
                        'rating': 'Rating (Low to High)',
                        'name': 'Name (A-Z)',
                        '-name': 'Name (Z-A)',
                        '-released': 'Newest First',
                        'released': 'Oldest First'
                    },
                    value='-rating'
                ).classes('w-56')

                min_rating_input = ui.number(
                    label='Min Rating',
                    value=0.0,
                    min=0.0,
                    max=5.0,
                    step=0.5
                ).classes('w-32')

                ui.button(
                    'Apply Filters',
                    on_click=lambda: load_games(
                        games_container,
                        pagination_container,
                        current_page,
                        items_per_page,
                        sort_select.value,
                        min_rating_input.value
                    )
                ).props('color=primary')

        games_container = ui.column().classes('w-full')

        pagination_container = ui.row().classes('w-full justify-center items-center gap-4 mt-6')

        load_games(games_container, pagination_container, current_page, items_per_page)


def load_games(
        games_container: ui.column,
        pagination_container: ui.row,
        current_page: dict,
        items_per_page: int,
        sort_by: str = '-rating',
        min_rating: float = 0.0
):
    games_container.clear()
    pagination_container.clear()

    skip = (current_page['value'] - 1) * items_per_page

    total_games_query = f"""
    MATCH (g:Game)
    WHERE g.rating >= {min_rating}
    RETURN count(g) as total
    """
    from database.connection import db
    total_result = db.execute_query(total_games_query)
    total_games = total_result[0]['total'] if total_result else 0

    total_pages = (total_games + items_per_page - 1) // items_per_page

    games = get_games_sorted(skip, items_per_page, sort_by, min_rating)

    with games_container:
        if games:
            start_item = skip + 1
            end_item = min(skip + items_per_page, total_games)
            ui.label(f'Showing {start_item}-{end_item} of {total_games} games').classes('text-sm text-gray-600 mb-4')

            with ui.row().classes('gap-4 flex-wrap'):
                for game in games:
                    create_game_card(game)
        else:
            ui.label('No games found').classes('text-gray-500')

    with pagination_container:
        ui.button(
            'Previous',
            on_click=lambda: change_page(
                games_container,
                pagination_container,
                current_page,
                items_per_page,
                -1,
                sort_by,
                min_rating
            ),
            icon='chevron_left'
        ).props('flat').set_enabled(current_page['value'] > 1)

        # Page info
        ui.label(f'Page {current_page["value"]} of {total_pages}').classes('text-lg font-semibold mx-4')

        # Next button
        ui.button(
            'Next',
            on_click=lambda: change_page(
                games_container,
                pagination_container,
                current_page,
                items_per_page,
                1,
                sort_by,
                min_rating
            ),
            icon='chevron_right'
        ).props('flat icon-right').set_enabled(current_page['value'] < total_pages)

        if total_pages > 1:
            ui.label('Go to:').classes('ml-8')

            page_input = ui.number(
                value=current_page['value'],
                min=1,
                max=total_pages,
                step=1
            ).classes('w-20').props('dense')

            ui.button(
                'Go',
                on_click=lambda: jump_to_page(
                    games_container,
                    pagination_container,
                    current_page,
                    items_per_page,
                    int(page_input.value),
                    sort_by,
                    min_rating
                )
            ).props('size=sm')


def change_page(
        games_container,
        pagination_container,
        current_page,
        items_per_page,
        direction,
        sort_by='-rating',
        min_rating=0.0
):
    current_page['value'] += direction
    load_games(games_container, pagination_container, current_page, items_per_page, sort_by, min_rating)

    ui.run_javascript('window.scrollTo(0, 0)')

def jump_to_page(
        games_container,
        pagination_container,
        current_page,
        items_per_page,
        page_number,
        sort_by='-rating',
        min_rating=0.0
):
    current_page['value'] = page_number
    load_games(games_container, pagination_container, current_page, items_per_page, sort_by, min_rating)

    ui.run_javascript('window.scrollTo(0, 0)')

def get_games_sorted(skip: int, limit: int, sort_by: str, min_rating: float):
    if sort_by.startswith('-'):
        field = sort_by[1:]
        order = 'DESC'
    else:
        field = sort_by
        order = 'ASC'

    query = f"""
    MATCH (g:Game)
    WHERE g.rating >= {min_rating}
    RETURN g.id as id,
           g.name as name,
           g.rating as rating,
           g.released as released,
           g.background_image as image,
           g.metacritic as metacritic
    ORDER BY g.{field} {order}
    SKIP {skip}
    LIMIT {limit}
    """

    from database.connection import db
    return db.execute_query(query)