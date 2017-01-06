"""Tests for the Learning Journal application."""
# -*- coding: utf-8 -*-

import pytest
from pyramid import testing

from learning_journal.models import Jentry, get_tm_session
from learning_journal.models.meta import Base

import faker
import datetime
import random

# =============== TEST JENTRYS ================

FAKE = faker.Faker()
now = datetime.datetime.now()
CATEGORIES = [
    "history",
    "economics",
    "current events",
    "distractions",
    "python",
    "music production",
    "new music",
    "environment",
    "cool ideas",
    "the end of the world",
]

JENTRYS = [
    Jentry(
        title=FAKE.job(),
        content=FAKE.text(max_nb_chars=200),
        contentr='',
        created=now,
        modified=now,
        category=random.choice(CATEGORIES)
    ) for i in range(100)
]

# ================== TEST SESSION =====================


@pytest.fixture(scope="session")
def configuration(request):
    """Configurator."""
    config = testing.setUp(settings={'sqlalchemy.url': 'sqlite:///:memory:'})
    config.include('learning_journal.models')
    config.include('learning_journal.routes')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture()
def db_session(configuration, request):
    """Create test DB session."""
    SessionFactory = configuration.registry['dbsession_factory']  # noqa
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Make a fake HTTP request with DB Session."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_models(dummy_request):
    """Generate model instances in the db."""
    dummy_request.dbsession.add_all(JENTRYS)


# @pytest.fixture
# def set_auth_credentials():
#     """Username/password for testing."""
#     import os
#     from passlibs.apps import custom_app_context as pwd_context

#     os.environ["AUTH_USERNAME"] = "testme"
#     os.environ["AUTH_PASSWORD"] = pwd.context.hash("foobar")

# ============ UNIT TESTS ===============

def test_new_jentry(db_session):
    """New journals are added to the database."""
    db_session.add_all(JENTRYS)
    query = db_session.query(Jentry).all()
    assert len(query) == len(JENTRYS)


def test_list_view_returns_empty_when_empty(dummy_request):
    """Test that the list view returns nothing."""
    from learning_journal.views.default import list_view
    result = list_view(dummy_request)
    assert len(result["journal"]) == 0
