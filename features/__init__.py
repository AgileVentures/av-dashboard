from aloe import before, step, world
from nose.tools import assert_equals
from av_dashboard import create_app
import json

@before.each_example
def before_all(*args):
    app = create_app()
    world.app = app.test_client()

@step(r'When I visit the dashboard')
def when_i_visit_the_dashboard(self):
    world.response = world.app.get('/')

@step(r'Then I should see the dashboard')
def then_i_should_see_a_proper_title_page(self):
    assert world.response.status_code == 200
    assert b'Agile Ventures Dashboard' in world.response.data

@step(r'Then I should be redirected to get a token from WSO')
def then_i_should_be_redirected_to_WSO(self):
    assert world.response.status_code == 302
    assert world.response.location == "https://www.agileventures.org/get-token"

@step(r'When I return with a valid token')
def when_i_return_with_a_valid_token(self):
    data=dict(
        token="notquitevalid"
    )
    world.response = world.app.post('/', data=data)
