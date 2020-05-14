#!/usr/bin/env python3
import unittest
import json
import os

from block_spam_calls import app


class BlockSpamCalls(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client(self)

    def load_json_fixture(self, filename):
        filepath = os.path.join(os.path.dirname(__file__), 'fixtures/', filename)
        with open(filepath, 'rb') as fd:
            fixture = fd.read()
        return fixture.decode('utf-8-sig')

    def test_successful_without_add_ons(self):
        result = self.app.post('/')
        self.assertFalse(b'<Reject' in result.data)

    def test_successful_with_marchex(self):
        add_ons = self.load_json_fixture('successful_marchex.json')
        result = self.app.post('/', data={'AddOns': add_ons})
        self.assertFalse(b'<Reject' in result.data)

    def test_blocked_with_marchex(self):
        add_ons = self.load_json_fixture('spam_marchex.json')
        result = self.app.post('/', data={'AddOns': add_ons})
        self.assertTrue(b'<Reject' in result.data)

    def test_successful_with_nomorobo(self):
        add_ons = self.load_json_fixture('successful_nomorobo.json')
        result = self.app.post('/', data={'AddOns': add_ons})
        self.assertFalse(b'<Reject' in result.data)

    def test_blocked_with_nomorobo(self):
        add_ons = self.load_json_fixture('spam_nomorobo.json')
        result = self.app.post('/', data={'AddOns': add_ons})
        self.assertTrue(b'<Reject' in result.data)

    def test_successful_with_ekata(self):
        add_ons = self.load_json_fixture('successful_ekata.json')
        result = self.app.post('/', data={'AddOns': add_ons})
        self.assertFalse(b'<Reject' in result.data)

    def test_blocked_with_ekata(self):
        add_ons = self.load_json_fixture('spam_ekata.json')
        result = self.app.post('/', data={'AddOns': add_ons})
        self.assertTrue(b'<Reject' in result.data)

    def test_successful_with_nomorobo_api_failure(self):
        add_ons = self.load_json_fixture('failed_nomorobo.json')
        result = self.app.post('/', data={'AddOns': add_ons})
        self.assertFalse(b'<Reject' in result.data)


if __name__ == '__main__':
    unittest.main()