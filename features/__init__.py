from aloe import before, step, world
from nose.tools import assert_equals
from av_dashboard import create_app


@before.each_example
def before_all(*args):
    app = create_app()
    world.app = app.test_client()

@step(r'When I visit the dashboard')
def when_i_visit_the_dashboard(self):
    world.response = world.app.get('/')

@step(r'Then I should see a proper title page')
def then_i_should_see_a_proper_title_page(self):
    assert b'Agile Ventures Dashboard' in world.response.data
