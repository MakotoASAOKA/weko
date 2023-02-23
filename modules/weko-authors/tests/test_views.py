# -*- coding: utf-8 -*-
#
# This file is part of WEKO3.
# Copyright (C) 2017 National Institute of Informatics.
#
# WEKO3 is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# WEKO3 is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WEKO3; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.

"""Module tests."""
# .tox/c1/bin/pytest --cov=weko_authors tests/test_views.py -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-authors/.tox/c1/tmp

import json
import pytest
from flask import url_for
from mock import patch, MagicMock

from invenio_accounts.testutils import login_user_via_session


def assert_role(response,is_permission,status_code=403):
    if is_permission:
        assert response.status_code != status_code
    else:
        assert response.status_code == status_code

class MockIndexer():
    def __init__(self):
        self.client = self.MockClient()

    class MockClient():
        def __init__(self):
            pass

        def search(self, index=None, doc_type=None, body=None):
            return {"hits": {"hits": [{"_source":
                    {"authorNameInfo": "", "authorIdInfo": "", "emailInfo": ""}
                    }]}}

        def index(self, index=None, doc_type=None, body=None):
            return {}

        def get(self, index=None, doc_type=None, id=None, body=None):
            return {"_source": {"authorNameInfo": {},
                                "authorIdInfo": {},
                                "emailInfo": {},
                                "affiliationInfo":{}
                                }
                    }

        def update(self, index=None, doc_type=None, id=None, body=None):
            return {"_source": {"authorNameInfo": "", "authorIdInfo": "",
                                "emailInfo": ""}}


def get_json(response):
    """Get JSON from response."""
    return json.loads(response.get_data(as_text=True))


def test_create_prefix_guest(client):
    """
    Test of create author prefix.
    :param client: The flask client.
    """
    input = {'name': 'test', 'scheme': 'test', 'url': 'https://test/##'}
    res = client.put('/api/authors/add_prefix',
                     data=json.dumps(input),
                     content_type='application/json', follow_redirects=False)
    assert res.status_code == 302
    # TODO check that the path changed
    # assert res.url == url_for('security.login')


#.tox/c1/bin/pytest --cov=weko_authors tests/test_views.py::test_create_prefix_users -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-authors/.tox/c1/tmp
@pytest.mark.parametrize('users_index, is_permission', [
    (0,True), # sysadmin
    (1,True), # repoadmin
    (2,True), # comadmin
    (3,True), # contributor
    (4,False), # generaluser
    (5,False), # originalroleuser
    (6,True), # originalroleuser2
    (7,False), # user
    (8,False), # student  
])
def test_create_prefix_users(client, users, users_index, is_permission):
    """
    Test of create author prefix.
    :param client: The flask client.
    """
    # login
    login_user_via_session(client=client, email=users[users_index]['email'])

    input = {'name': 'test0', 'scheme': 'test0', 'url': 'https://test0/##'}
    res = client.put('/api/authors/add_prefix',
                     data=json.dumps(input),
                     content_type='application/json')
    assert_role(res, is_permission)


#.tox/c1/bin/pytest --cov=weko_authors tests/test_views.py::test_update_prefix_guest -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-authors/.tox/c1/tmp
def test_update_prefix_guest(client, id_prefix):
    """
    Test of update author prefix.
    :param client: The flask client.
    """
    input2 = {'id': id_prefix, 'name': 'testchanged', 'scheme': 'testchanged',
              'url': 'https://testchanged/##'}
    res = client.post('/api/authors/edit_prefix',
                      data=json.dumps(input2),
                      content_type='application/json')
    assert res.status_code == 302
    # TODO check that the path changed
    # assert res.url == url_for('security.login')

#.tox/c1/bin/pytest --cov=weko_authors tests/test_views.py::test_update_prefix_users -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-authors/.tox/c1/tmp
@pytest.mark.parametrize('users_index, is_permission', [
    (0,True), # sysadmin
    (1,True), # repoadmin
    (2,True), # comadmin
    (3,True), # contributor
    (4,False), # generaluser
    (5,False), # originalroleuser
    (6,True), # originalroleuser2
    (7,False), # user
    (8,False), # student  
])
def test_update_prefix_users(client, users, id_prefix, users_index, is_permission):
    """
    Test of update author prefix.
    :param client: The flask client.
    """
    # login
    login_user_via_session(client=client, email=users[users_index]['email'])
    input2 = {'id': id_prefix, 'name': 'test0changed', 'scheme': 'test0changed',
              'url': 'https://test0changed/##'}
    res = client.post('/api/authors/edit_prefix',
                      data=json.dumps(input2),
                      content_type='application/json')
    assert_role(res, is_permission)


def test_delete_prefix_guest(client, id_prefix):
    """
    Test of delete author prefix.
    :param client: The flask client.
    """
    # delete prefix
    url = url_for('weko_authors.delete_prefix', id=id_prefix)
    res = client.delete(url)
    assert res.status_code == 302
    # TODO check that the path changed
    # assert res.url == url_for('security.login')


@pytest.mark.parametrize('users_index, is_permission', [
    (0,True), # sysadmin
    (1,True), # repoadmin
    (2,True), # comadmin
    (3,True), # contributor
    (4,False), # generaluser
    (5,False), # originalroleuser
    (6,True), # originalroleuser2
    (7,False), # user
    (8,False), # student  
])
def test_delete_prefix_users(client, users, id_prefix, users_index, is_permission):
    """
    Test of delete author prefix.
    :param client: The flask client.
    """
    # login for delete prefix
    login_user_via_session(client=client, email=users[users_index]['email'])
    url = url_for('weko_authors.delete_prefix', id=id_prefix)
    res = client.delete(url)
    assert_role(res, is_permission)


def test_getById_guest(client):
    """
    Test of get author data by id.
    :param client: The flask client.
    """
    input = {"Id": "1"}
    res = client.post('/api/authors/search_edit',
                      data=json.dumps(input),
                      content_type='application/json')
    assert res.status_code == 302
    # TODO check that the path changed
    # assert res.url == url_for('security.login')

@pytest.mark.parametrize('users_index, is_permission', [
    (0,True), # sysadmin
    (1,True), # repoadmin
    (2,True), # comadmin
    (3,True), # contributor
    (4,False), # generaluser
    (5,False), # originalroleuser
    (6,True), # originalroleuser2
    (7,False), # user
    (8,False), # student  
])
def test_getById_users(client, users, users_index, is_permission):
    """
    Test of get author data by id.
    :param client: The flask client.
    """
    login_user_via_session(client=client, email=users[users_index]['email'])
    input = {"Id": "1"}
    mock_indexer = MagicMock(side_effect=MockIndexer)
    with patch('weko_authors.views.RecordIndexer', mock_indexer):

        res = client.post('/api/authors/search_edit',
                          data=json.dumps(input),
                          content_type='application/json')
    assert_role(res, is_permission)


def test_gatherById_guest(client):
    """
    Test of gather author data by id.
    :param client: The flask client.
    """
    input = {'idFrom': ['1', '2'], 'idFromPkId': ['1', '2'], 'idTo': '1'}
    res = client.post('/api/authors/gather',
                      data=json.dumps(input),
                      content_type='application/json')
    assert res.status_code == 302
    # TODO check that the path changed
    # assert res.url == url_for('security.login')


@pytest.mark.parametrize('users_index, is_permission', [
    (0,True), # sysadmin
    (1,True), # repoadmin
    (2,True), # comadmin
    (3,True), # contributor
    (4,False), # generaluser
    (5,False), # originalroleuser
    (6,True), # originalroleuser2
    (7,False), # user
    (8,False), # student  
])
def test_gatherById_users(client, users, users_index, is_permission):
    """
    Test of gather author data by id.
    :param client: The flask client.
    """
    login_user_via_session(client=client, email=users[users_index]['email'])
    input = {'idFrom': ['1', '2'], 'idFromPkId': ['1', '2'], 'idTo': '1'}
    mock_indexer = MagicMock(side_effect=MockIndexer)
    with patch('weko_authors.views.RecordIndexer', mock_indexer):
        with patch('weko_deposit.tasks.update_items_by_authorInfo'):
            res = client.post('/api/authors/gather',
                              data=json.dumps(input),
                              content_type='application/json')
            assert_role(res, is_permission)


def test_get_guest(client):
    """
    Test of search and get author data.
    :param client: The flask client.
    """
    input = {"searchKey": "", "pageNumber": 1, "numOfPage": 25,
             "sortKey": "", "sortOrder": ""}
    res = client.post('/api/authors/search',
                      data=json.dumps(input),
                      content_type='application/json')
    assert res.status_code == 302
    # TODO check that the path changed
    # assert res.url == url_for('security.login')


@pytest.mark.parametrize('users_index, is_permission', [
    (0,True), # sysadmin
    (1,True), # repoadmin
    (2,True), # comadmin
    (3,True), # contributor
    (4,False), # generaluser
    (5,False), # originalroleuser
    (6,True), # originalroleuser2
    (7,False), # user
    (8,False), # student  
])
def test_get_users(client, users, users_index, is_permission):
    """
    Test of search and get author data.
    :param client: The flask client.
    """
    login_user_via_session(client=client, email=users[users_index]['email'])
    input = {"searchKey": "", "pageNumber": 1, "numOfPage": 25,
             "sortKey": "", "sortOrder": ""}
    mock_indexer = MagicMock(side_effect=MockIndexer)
    with patch('weko_authors.views.RecordIndexer', mock_indexer):
        res = client.post('/api/authors/search',
                          data=json.dumps(input),
                          content_type='application/json')
    assert_role(res, is_permission)


def test_create_guest(client):
    """
    Test of create author.
    :param client: The flask client.
    """
    input = {
            "id": "",
            "pk_id": "",
            "authorNameInfo": [
                {
                    "familyName": "テスト",
                    "firstName": "タロウ",
                    "fullName": "",
                    "language": "ja-Kana",
                    "nameFormat": "familyNmAndNm",
                    "nameShowFlg": "true"
                }
            ],
            "authorIdInfo": [
                {
                    "idType": "2",
                    "authorId": "0123",
                    "authorIdShowFlg": "true"
                }
            ],
            "emailInfo": [
                {"email": "example@com"}
            ]
    }
    res = client.post('/api/authors/add',
                      data=json.dumps(input),
                      content_type='application/json')
    assert res.status_code == 302
    # TODO check that the path changed
    # assert res.url == url_for('security.login')


@pytest.mark.parametrize('users_index, is_permission', [
    (0,True), # sysadmin
    (1,True), # repoadmin
    (2,True), # comadmin
    (3,True), # contributor
    (4,False), # generaluser
    (5,False), # originalroleuser
    (6,True), # originalroleuser2
    (7,False), # user
    (8,False), # student  
])
def test_create_users(client, users, users_index, is_permission):
    """
    Test of create author.
    :param client: The flask client.
    """
    login_user_via_session(client=client, email=users[users_index]['email'])
    input = {
            "id": "",
            "pk_id": "",
            "authorNameInfo": [
                {
                    "familyName": "テスト",
                    "firstName": "タロウ",
                    "fullName": "",
                    "language": "ja-Kana",
                    "nameFormat": "familyNmAndNm",
                    "nameShowFlg": "true"
                }
            ],
            "authorIdInfo": [
                {
                    "idType": "2",
                    "authorId": "0123",
                    "authorIdShowFlg": "true"
                }
            ],
            "emailInfo": [
                {"email": "example@com"}
            ]
    }
    mock_indexer = MagicMock(side_effect=MockIndexer)
    with patch('weko_authors.views.RecordIndexer', mock_indexer):
        with patch('weko_authors.views.Authors.get_sequence', return_value=1):
            res = client.post('/api/authors/add',
                              data=json.dumps(input),
                              content_type='application/json')
    assert_role(res, is_permission)


def test_update_author_guest(client):
    """
    Test of update author data.
    :param client: The flask client.
    """
    input = {
            "id": "1",
            "pk_id": "1",
            "authorNameInfo": [
                {
                    "familyName": "テスト",
                    "firstName": "タロウ",
                    "fullName": "",
                    "language": "ja-Kana",
                    "nameFormat": "familyNmAndNm",
                    "nameShowFlg": "true"
                }
            ],
            "authorIdInfo": [
                {
                    "idType": "2",
                    "authorId": "0123",
                    "authorIdShowFlg": "true"
                }
            ],
            "emailInfo": [
                {"email": "examplechanged@com"}
            ]
    }
    res = client.post('/api/authors/edit',
                      data=json.dumps(input),
                      content_type='application/json')
    assert res.status_code == 302
    # TODO check that the path changed
    # assert res.url == url_for('security.login')


@pytest.mark.parametrize('users_index, is_permission', [
    (0,True), # sysadmin
    (1,True), # repoadmin
    (2,True), # comadmin
    (3,True), # contributor
    (4,False), # generaluser
    (5,False), # originalroleuser
    (6,True), # originalroleuser2
    (7,False), # user
    (8,False), # student  
])
def test_update_author_users(client, users, create_author, users_index, is_permission):
    """
    Test of update author data.
    :param client: The flask client.
    """
    author_data = {
                "authorNameInfo": [
                    {
                        "familyName": "テスト",
                        "firstName": "ハナコ",
                        "fullName": "",
                        "language": "ja-Kana",
                        "nameFormat": "familyNmAndNm",
                        "nameShowFlg": "true"
                    }
                ],
                "authorIdInfo": [
                    {
                        "idType": "2",
                        "authorId": "01234",
                        "authorIdShowFlg": "true"
                    }
                ],
                "emailInfo": [
                    {"email": "example@com"}
                ]
        }
    id = 1
    author_id = create_author(author_data, id)
    login_user_via_session(client=client, email=users[users_index]['email'])
    input = {
            "id": author_id,
            "pk_id": author_id,
            "authorNameInfo": [
                {
                    "familyName": "テスト",
                    "firstName": "タロウ",
                    "fullName": "",
                    "language": "ja-Kana",
                    "nameFormat": "familyNmAndNm",
                    "nameShowFlg": "true"
                }
            ],
            "authorIdInfo": [
                {
                    "idType": "2",
                    "authorId": "0123",
                    "authorIdShowFlg": "true"
                }
            ],
            "emailInfo": [
                {"email": "examplechanged@com"}
            ]
    }
    mock_indexer = MagicMock(side_effect=MockIndexer)
    with patch('weko_authors.views.RecordIndexer', mock_indexer):
        with patch('weko_deposit.tasks.update_items_by_authorInfo'):
            res = client.post('/api/authors/edit',
                              data=json.dumps(input),
                              content_type='application/json')
            assert_role(res, is_permission)


def test_delete_author_guest(client):
    """
    Test of delete author data.
    :param client: The flask client.
    """
    input = {"pk_id": "1"}
    res = client.post('/api/authors/delete',
                      data=json.dumps(input),
                      content_type='application/json')
    assert res.status_code == 302
    # TODO check that the path changed
    # assert res.url == url_for('security.login')


@pytest.mark.parametrize('users_index, is_permission', [
    (0,True), # sysadmin
    (1,True), # repoadmin
    (2,True), # comadmin
    (3,True), # contributor
    (4,False), # generaluser
    (5,False), # originalroleuser
    (6,True), # originalroleuser2
    (7,False), # user
    (8,False), # student  
])
def test_delete_author_users(client, users, create_author, users_index, is_permission):
    """
    Test of delete author data.
    :param client: The flask client.
    """
    author_data = {
                "authorNameInfo": [
                    {
                        "familyName": "テスト",
                        "firstName": "ハナコ",
                        "fullName": "",
                        "language": "ja-Kana",
                        "nameFormat": "familyNmAndNm",
                        "nameShowFlg": "true"
                    }
                ],
                "authorIdInfo": [
                    {
                        "idType": "2",
                        "authorId": "01234",
                        "authorIdShowFlg": "true"
                    }
                ],
                "emailInfo": [
                    {"email": "example@com"}
                ]
        }
    author_id = 1
    id = create_author(author_data, author_id)
    login_user_via_session(client=client, email=users[users_index]['email'])
    input = {"pk_id": str(id)}
    mock_indexer = MagicMock(side_effect=MockIndexer)
    with patch('weko_authors.views.RecordIndexer', mock_indexer):
        with patch('weko_authors.utils.RecordIndexer', mock_indexer):
            res = client.post('/api/authors/delete',
                              data=json.dumps(input),
                              content_type='application/json')
            assert_role(res, is_permission)


def test_mapping_guest(client):
    """
    Test of mapping author data.
    :param client: The flask client.
    """
    input = {"id": "1"}
    res = client.post('/api/authors/input',
                      data=json.dumps(input),
                      content_type='application/json')
    assert res.status_code == 302
    # TODO check that the path changed
    # assert res.url == url_for('security.login')

# .tox/c1/bin/pytest --cov=weko_authors tests/test_views.py::test_mapping_users -vv -s --cov-branch --cov-report=term --basetemp=/code/modules/weko-authors/.tox/c1/tmp
@pytest.mark.parametrize('users_index, is_permission', [
    (0,True), # sysadmin
    (1,True), # repoadmin
    (2,True), # comadmin
    (3,True), # contributor
    (4,False), # generaluser
    (5,False), # originalroleuser
    (6,True), # originalroleuser2
    (7,False), # user
    (8,False), # student  
])
def test_mapping_users(client, users, users_index, is_permission):
    """
    Test of mapping author data.
    :param client: The flask client.
    """
    login_user_via_session(client=client, email=users[users_index]['email'])
    input = {"id": "1"}
    mock_indexer = MagicMock(side_effect=MockIndexer)
    with patch('weko_authors.views.RecordIndexer', mock_indexer):
        res = client.post('/api/authors/input',
                          data=json.dumps(input),
                          content_type='application/json')
        assert_role(res, is_permission)

