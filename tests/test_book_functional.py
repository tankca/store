# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/

TESTS MUST START WITH "test"
"""
import pytest

from flask import url_for
from store.book.models import Book
from store.dummy_data import books as testdata
from store.book.forms import AddBookForm


@pytest.mark.usefixtures('db')
class TestBook:
    """Tests for book."""

    def test_book_is_not_not_found(self, testapp):
        """Book page 404."""
        # !!! URL needs the / at the end.
        res = testapp.get('/book/')
        assert res.status_code != 404

    def test_book_is_accessible(self, testapp):
        """Book page 200."""
        # testapp made available from the tests module
        res = testapp.get('/book/')
        assert res.status_code == 200

    def test_book_has_book(self, testapp):
        """There is a book on book page."""
        book = testdata.sample_list[0]
        book.save()

        res = testapp.get('/book/book')

        # i have discovered that "string" in res is case sensitive
        # in general to know more see:
        # http://webtest.readthedocs.io/en/latest/api.html#webtest-response-testresponse
        assert "9780439708180" in res

    def test_book_has_some_books(self, testapp):
        """There are some books."""
        for book in testdata.sample_list:
            book.save()

        res = testapp.get('/book/books')

        assert "9780439064873" in res

        # When program encounters an assert statement, Python evaluates
        # the accompanying expression, which is hopefully true.
        # If the expression is false, Python raises an AssertionError
        # exception.


class TestAddBook:
    """Test adding book."""

    def test_can_add_book(self, testapp):
        """Can add a book."""
        res = testapp.get('/book/add')
        form = res.forms['addBookForm']

        res = form.submit()
        assert "Invalid" in res