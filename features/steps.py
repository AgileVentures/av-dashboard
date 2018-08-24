import datetime
import json

import jwt
from aloe import before, step, world
from freezegun import freeze_time
from nose.tools import assert_equals

from av_dashboard import create_app


@before.each_example
def before_all(*args):
    app = create_app({'session_key': 'secret_session', 'jwt_key': 'super_sauce', 'postgres': {'user': 'postgres', 'pw': 'password', 'host': 'localhost', 'port': '5432', 'db': 'db'}})
    app.config['TESTING'] = True
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

@step(r'When I return with a valid token with authorization privileges(?: expiring on (.*))?')
def when_i_return_with_a_valid_token(self, expiration):
    data = dict(
        token = jwt.encode({'exp': datetime.datetime.strptime(expiration, "%Y-%m-%d").timestamp(), 'authorized': 'true' }, 'super_sauce', algorithm='HS256')
    )
    world.response = world.app.post('/', data=data)

@step(r'When I return with a valid token without authorization privileges(?: expiring on (.*))?')
def when_i_return_with_a_valid_token_without_authorization(self, expiration):
    data = dict(
        token = jwt.encode({'exp': datetime.datetime.strptime(expiration, "%Y-%m-%d").timestamp(), 'authorized': 'false' }, 'super_sauce', algorithm='HS256')
    )
    world.response = world.app.post('/', data=data)

@step(r'When the date is 2012-10-01')
def set_date_to_2012_10_01(self):
    freeze_time("2012-10-01 12:00:01").start()

@step(r'When the date is 2012-10-03')
def set_date_to_2012_10_01(self):
    freeze_time("2012-10-03 12:00:01").start()

@step(r"Then I should see a message saying I do not have access")
def see_no_access_message(self):
    assert b'You are not authorized to view this resource' in world.response.data
