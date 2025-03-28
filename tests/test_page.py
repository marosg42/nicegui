import asyncio
from uuid import uuid4

from nicegui import Client, background_tasks, ui

from .screen import Screen


def test_page(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    screen.open('/')
    screen.should_contain('NiceGUI')
    screen.should_contain('Hello, world!')


def test_auto_index_page(screen: Screen):
    ui.label('Hello, world!')

    screen.open('/')
    screen.should_contain('NiceGUI')
    screen.should_contain('Hello, world!')


def test_custom_title(screen: Screen):
    @ui.page('/', title='My Custom Title')
    def page():
        ui.label('Hello, world!')

    screen.open('/')
    screen.should_contain('My Custom Title')
    screen.should_contain('Hello, world!')


def test_route_with_custom_path(screen: Screen):
    @ui.page('/test_route')
    def page():
        ui.label('page with custom path')

    screen.open('/test_route')
    screen.should_contain('page with custom path')


def test_auto_index_page_with_link_to_subpage(screen: Screen):
    ui.link('link to subpage', '/subpage')

    @ui.page('/subpage')
    def page():
        ui.label('the subpage')

    screen.open('/')
    screen.click('link to subpage')
    screen.should_contain('the subpage')


def test_link_to_page_by_passing_function(screen: Screen):
    @ui.page('/subpage')
    def page():
        ui.label('the subpage')

    ui.link('link to subpage', page)

    screen.open('/')
    screen.click('link to subpage')
    screen.should_contain('the subpage')


def test_creating_new_page_after_startup(screen: Screen):
    screen.start_server()

    @ui.page('/late_page')
    def page():
        ui.label('page created after startup')

    screen.open('/late_page')
    screen.should_contain('page created after startup')


def test_shared_and_private_pages(screen: Screen):
    @ui.page('/private_page')
    def private_page():
        ui.label(f'private page with uuid {uuid4()}')

    ui.label(f'shared page with uuid {uuid4()}')

    screen.open('/private_page')
    uuid1 = screen.find('private page').text.split()[-1]
    screen.open('/private_page')
    uuid2 = screen.find('private page').text.split()[-1]
    assert uuid1 != uuid2

    screen.open('/')
    uuid1 = screen.find('shared page').text.split()[-1]
    screen.open('/')
    uuid2 = screen.find('shared page').text.split()[-1]
    assert uuid1 == uuid2


def test_wait_for_connected(screen: Screen):
    async def load() -> None:
        label.text = 'loading...'
        # NOTE we can not use asyncio.create_task() here because we are on a different thread than the NiceGUI event loop
        background_tasks.create(takes_a_while())

    async def takes_a_while() -> None:
        await asyncio.sleep(0.1)
        label.text = 'delayed data has been loaded'

    @ui.page('/')
    async def page(client: Client):
        global label
        label = ui.label()
        await client.connected()
        await load()

    screen.open('/')
    screen.should_contain('delayed data has been loaded')


def test_wait_for_disconnect(screen: Screen):
    events = []

    @ui.page('/')
    async def page(client: Client):
        await client.connected()
        events.append('connected')
        await client.disconnected()
        events.append('disconnected')

    screen.open('/')
    screen.wait(0.5)
    screen.open('/')
    screen.wait(0.5)
    assert events == ['connected', 'disconnected', 'connected']


def test_adding_elements_after_connected(screen: Screen):
    @ui.page('/')
    async def page(client: Client):
        ui.label('before')
        await client.connected()
        ui.label('after')

    screen.open('/')
    screen.should_contain('before')
    screen.should_contain('after')


def test_exception(screen: Screen):
    @ui.page('/')
    def page():
        raise Exception('some exception')

    screen.open('/')
    screen.should_contain('500')
    screen.should_contain('Server error')
    screen.assert_py_logger('ERROR', 'some exception')


def test_exception_after_connected(screen: Screen):
    @ui.page('/')
    async def page(client: Client):
        await client.connected()
        ui.label('this is shown')
        raise Exception('some exception')

    screen.open('/')
    screen.should_contain('this is shown')
    screen.assert_py_logger('ERROR', 'some exception')


def test_page_with_args(screen: Screen):
    @ui.page('/page/{id}')
    def page(id: int):
        ui.label(f'Page {id}')

    screen.open('/page/42')
    screen.should_contain('Page 42')


def test_adding_elements_during_onconnect(screen: Screen):
    @ui.page('/')
    def page(client: Client):
        ui.label('Label 1')
        client.on_connect(lambda: ui.label('Label 2'))

    screen.open('/')
    screen.should_contain('Label 2')


def test_async_connect_handler(screen: Screen):
    @ui.page('/')
    def page(client: Client):
        async def run_js():
            result.text = await ui.run_javascript('41 + 1')
        result = ui.label()
        client.on_connect(run_js)

    screen.open('/')
    screen.should_contain('42')


def test_dark_mode(screen: Screen):
    @ui.page('/auto', dark=None)
    def page():
        ui.label('A').classes('text-blue-400 dark:text-red-400')

    @ui.page('/light', dark=False)
    def page():
        ui.label('B').classes('text-blue-400 dark:text-red-400')

    @ui.page('/dark', dark=True)
    def page():
        ui.label('C').classes('text-blue-400 dark:text-red-400')

    blue = 'rgba(96, 165, 250, 1)'
    red = 'rgba(248, 113, 113, 1)'
    white = 'rgba(0, 0, 0, 0)'
    black = 'rgba(18, 18, 18, 1)'

    screen.open('/auto')
    assert screen.find('A').value_of_css_property('color') == blue
    assert screen.find_by_tag('body').value_of_css_property('background-color') == white

    screen.open('/light')
    assert screen.find('B').value_of_css_property('color') == blue
    assert screen.find_by_tag('body').value_of_css_property('background-color') == white

    screen.open('/dark')
    assert screen.find('C').value_of_css_property('color') == red
    assert screen.find_by_tag('body').value_of_css_property('background-color') == black
