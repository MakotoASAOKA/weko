import os
import json
import copy
import pytest
import unittest
import datetime
from mock import patch, MagicMock, Mock
from flask import current_app, make_response, request
from flask_login import current_user
from flask_babelex import Babel

from invenio_resourcesyncserver.api import ResourceListHandler, ChangeListHandler
from invenio_resourcesyncserver.utils import (
    get_real_path,
    render_capability_xml,
    render_well_know_resourcesync,
    query_record_changes,
    check_existing_record_in_list,
    parse_date,
    get_timezone,
    get_pid
)


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


# def get_real_path(path):
def test_get_real_path(i18n_app):
    path = ["test/test"]

    assert get_real_path(path)
    assert get_real_path(["test"])


# def render_capability_xml():
def test_render_capability_xml(i18n_app, db):
    data_1 = [MagicMock()]
    data_2 = [MagicMock()]

    with patch("invenio_resourcesyncserver.api.ResourceListHandler.get_capability_content", return_value=data_1):
        with patch("invenio_resourcesyncserver.api.ChangeListHandler.get_capability_content", return_value=data_2):
            assert render_capability_xml()


# def render_well_know_resourcesync():
def test_render_well_know_resourcesync(i18n_app):
    assert render_well_know_resourcesync()


# def query_record_changes(repository_id,
# def test_query_record_changes(i18n_app, db, search_result):
#     test = sample_ResourceListHandler()

#     # db.session.add(test)
#     # db.session.commit()

#     repository_id = 33
#     date_from = datetime.datetime.now() - datetime.timedelta(days=1)
#     date_until = datetime.datetime.now()
#     max_changes_size = None
#     change_tracking_state = None

#     assert query_record_changes(
#         repository_id=repository_id,
#         date_from=date_from,
#         date_until=date_until,
#         max_changes_size=max_changes_size,
#         change_tracking_state=change_tracking_state
#     )


# def check_existing_record_in_list(record_id, results):
def test_check_existing_record_in_list(i18n_app):
    results = {
        "record_id": 11
    }
    record_id = 11

    assert check_existing_record_in_list(record_id, [results])

    results["record_id"] = 10

    assert not check_existing_record_in_list(record_id, [results])


# def parse_date(date):
def test_parse_date(i18n_app):
    date = str(datetime.datetime.now() - datetime.timedelta(days=1))
    data_1 = datetime.datetime.now()
    data_2 = str(datetime.datetime.now() - datetime.timedelta(days=1))

    with patch("invenio_resourcesyncserver.utils.get_timezone", return_value=(data_1, data_2)):
        assert parse_date(date)


# def get_timezone(date):
def test_get_timezone(i18n_app):
    date_1 = "1:1+1:1+1:1"
    date_2 = "1-1:1:1"

    assert get_timezone(date_1)
    assert get_timezone(date_2)


# def get_pid(pid):
def test_get_pid(i18n_app, es_records):
    assert get_pid(1)
    assert not get_pid(11)