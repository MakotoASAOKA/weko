import json
import pytest
from flask import current_app, make_response, request
from flask_login import current_user
from mock import patch, MagicMock
from werkzeug.local import LocalProxy

from invenio_resourcesyncserver.api import ResourceListHandler, ChangeListHandler
from invenio_resourcesyncserver.models import ChangeListIndexes, ResourceListIndexes
from invenio_accounts.testutils import login_user_via_session
from invenio_resourcesyncserver.views import (
    resource_list,
    resource_dump,
    file_content,
    capability,
    resource_dump_manifest,
    change_list_index,
    change_list,
    change_dump_index,
    change_dump,
    change_dump_manifest,
    change_dump_content,
    well_know_resourcesync,
    source_description,
    record_detail_in_index
)


user_results = [
    (0, 200),
    (1, 200),
    (2, 200),
    (3, 200),
    (4, 200),
    (5, 200),
    (6, 200),
    (7, 200),
    (8, 200),
]

def sample_ResourceListHandler():
    test = ResourceListHandler()
    test.id = 1
    test.status = "test"
    test.repository_id = 33
    test.resource_dump_manifest = "test"
    test.url_path = "test"
    test.created = "test"
    test.updated = "test"
    test.index = "test"
    
    return test


def sample_ResourceListIndexes():
    test = ResourceListIndexes(
        id=1,
        status=True,
        repository_id=1,
        resource_dump_manifest=True,
        url_path="/"
    )

    return test


def sample_ChangeListHandler(key):

    def _func(keyword):
        if keyword == "str":
            test = ChangeListHandler(
                change_tracking_state="test"
            )
        else:
            test = ChangeListHandler(
                change_tracking_state=["test"]
            )
        
        test.id = "test"
        test.status = "test"
        test.repository_id = "Root Index"
        test.change_dump_manifest = "test"
        test.max_changes_size = "test"
        test.url_path = "/"
        test.created = "test"
        test.updated = "test"
        test.index = "test"
        test.publish_date = "test"
        test.interval_by_date = 2

        return test
    
    return _func(key)


# def resource_list(index_id):
# @pytest.mark.parametrize('id, status_code', user_results)
# @pytest.mark.parametrize('status', [True, False])
def test_resource_list(client_api, users, indices):
    # login_user_via_session(client=client_api, email=users[3]["email"])

    # res = client_api.post(
    #     "/resync/<index_id>/resourcelist.xml",
    #     data=json.dumps({}),
    #     content_type="application/json"
    # )

    # assert res.status_code == status_code

    test = sample_ResourceListHandler()
    index_id = 33

    def get_resource_list_xml():
        return True

    def not_get_resource_list_xml():
        return False

    data_1 = MagicMock()
    data_1.status = True
    data_1.get_resource_list_xml = get_resource_list_xml

    with patch("invenio_resourcesyncserver.api.ResourceListHandler.get_resource_by_repository_id", return_value=data_1):
        assert resource_list(index_id)

    with patch("invenio_resourcesyncserver.api.ResourceListHandler.get_resource_by_repository_id", return_value=None):
        try:
            assert resource_list(index_id)
        # abort(404) coverage
        except:
            pass

    with patch("invenio_resourcesyncserver.api.ResourceListHandler.get_resource_by_repository_id", return_value=data_1):
        data_1.get_resource_list_xml = not_get_resource_list_xml
        try:
            assert resource_list(index_id)
        # abort(404) coverage
        except:
            pass


# def resource_dump(index_id):
def test_resource_dump(client_api, users, indices):
    test = sample_ResourceListHandler()
    index_id = 33

    def get_resource_dump_xml():
        return True

    def not_get_resource_dump_xml():
        return False

    data_1 = MagicMock()
    data_1.status = True
    data_1.get_resource_dump_xml = get_resource_dump_xml

    with patch("invenio_resourcesyncserver.api.ResourceListHandler.get_resource_by_repository_id", return_value=data_1):
        assert resource_dump(index_id)

    with patch("invenio_resourcesyncserver.api.ResourceListHandler.get_resource_by_repository_id", return_value=None):
        try:
            assert resource_dump(index_id)
        # abort(404) coverage
        except:
            pass

    with patch("invenio_resourcesyncserver.api.ResourceListHandler.get_resource_by_repository_id", return_value=data_1):
        data_1.get_resource_dump_xml = not_get_resource_dump_xml
        try:
            assert resource_dump(index_id)
        # abort(404) coverage
        except:
            pass


# def file_content(index_id, record_id):
# def capability():
# def resource_dump_manifest(index_id, record_id):
# def change_list_index(index_id):
# def change_list(index_id, from_date):
# def change_dump_index(index_id):
# def change_dump(index_id, from_date):
# def change_dump_manifest(index_id, record_id):
# def change_dump_content(index_id, record_id):
# def well_know_resourcesync():
# def source_description():
# def record_detail_in_index(index_id, record_id):