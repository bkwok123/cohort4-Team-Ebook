import pytest

from flask import json
from datetime import datetime

import appserver
from db import db

# Only initialize and create tables in test module once
def setup_module(module):
    appserver.app.config['TESTING'] = True
    appserver.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    db.init_app(appserver.app)
    @appserver.app.before_first_request
    def create_tables():
        db.create_all()

@pytest.fixture
def client():

    client = appserver.app.test_client()

    yield client

def test_book(client):

    # No data for the test book
    rv = client.get('/book/1')

    # Expect Not Found request
    assert(rv.status_code == 404)
    assert(b'Book not found' in rv.data)

    rv = client.post('/book', data=dict(
            book_description="testTitle1 description"
            ))
    # Expect bad request due to client error
    assert(rv.status_code == 400)
    assert(b'Every book needs a title.' in rv.data)

    rv = client.post('/book', data=dict(
            book_title="testTitle1",
            book_description="testTitle1 description",
            book_genre="testTitle1 genre"
            ))
    # Expect created success status
    assert(rv.status_code == 201)
    assert(b'book_id' in rv.data)
    assert(b'book_title' in rv.data)
    assert(b'book_description' in rv.data)
    assert(b'testTitle1 description' in rv.data)
    assert(b'book_genre' in rv.data)
    assert(b'book_creation' in rv.data)
    ts = datetime.now().strftime('%Y-%m-%d')
    assert(bytes(ts, 'utf-8') in rv.data)
    assert(b'book_update' in rv.data)
    assert(bytes(ts, 'utf-8') in rv.data)    

    rv = client.put('/book/999', data=dict(
            book_description="testTitle1 description2",
            book_genre="testTitle1 genre2"
            ))
    # Expect success status response
    assert(rv.status_code == 400)

    rv = client.put('/book/1', data=dict(
            book_title="testTitle1",
            book_description="testTitle1 description2",
            book_genre="testTitle1 genre2"
            ))
    # Expect success status response
    assert(rv.status_code == 200)
    assert(b'"book_title": "testTitle1"' in rv.data)
    assert(b'"book_description": "testTitle1 description2"' in rv.data)
    assert(b'"book_genre": "testTitle1 genre2"' in rv.data)    

    rv = client.delete('/book/1', data=dict(
            book_description="testTitle1 description2",
            book_genre="testTitle1 genre2"
            ))
    # Expect success status response
    assert(rv.status_code == 200)
    assert(b'Book deleted' in rv.data)

def test_books(client):

    #####################################
    # Check empty book case
    #####################################
    rv = client.get('/books')
    assert(rv.status_code == 200)
    assert(b'[]' in rv.data)

    #####################################
    # Check a list of books case
    #####################################
    # Create test data
    rv = client.post('/book', data=dict(
        book_title="testTitle1",
        book_description="testTitle1 description1",
        book_genre="testTitle1 genre1"
        ))
    rv = client.post('/book', data=dict(
        book_title="testTitle2",
        book_description="testTitle2 description2",
        book_genre="testTitle2 genre2"
        ))

    rv = client.get('/books')
    assert(rv.status_code == 200)
    assert(b'"book_title": "testTitle1"' in rv.data)
    assert(b'"book_description": "testTitle1 description1"' in rv.data)
    assert(b'"book_genre": "testTitle1 genre1"' in rv.data)
    assert(b'"book_title": "testTitle2"' in rv.data)
    assert(b'"book_description": "testTitle2 description2"' in rv.data)
    assert(b'"book_genre": "testTitle2 genre2"' in rv.data)    