from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class BoggleTests(TestCase):

    def setUp(self):
        """To do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_welcome(self):
        """Make sure the instruction page displays properly"""

        with self.client:
            res = self.client.get('/')
            self.assertIn('<h2>Instructions:</2>', res.data)

    def test_start(self):
        """Make sure the game sesison is well initialized"""

        with self.client:
            res = self.client.get('/start')
            self.assertIn('board', session)
            self.assertIn('highscore', session)
            self.assertIn('play', session)
            self.assertEqual(session.get('play'), 0)
            self.assertEqual(session.get('highscore'), 0)
            self.assertEqual(session.get('board'), [])

    def test_show_oard(self):
        """Make sure the board is displayed properly"""

        with self.client:
            res = self.client.get('/board')
            self.assertIn('board', session)
            self.assertIn(
                '<label for="guess">Enter your guess:</label>', res.data)

    def test_check_word(self):
        """Test if word is valid """

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["N", "E", "R", "E", "A"], ["N", "E", "R", "E", "A"], [
                    "N", "E", "R", "E", "A"], ["N", "E", "R", "E", "A"], ["N", "E", "R", "E", "A"]]

        res = self.client.get('/word?guess=nerea')
        self.assertEqual(res.json['result'], 'ok')
        res = self.client.get('/ word?guess=cat')
        self.assertNotEqual(res.json['result'], 'ok')

    def test_end(self):
        """Test if end of game works properly"""

        with self.client as client:
            with client.session_transaction() as session:
                session['highscore'] = 23
                session['play'] = 50

        res = self.client.get('/end')
        self.assertEqual(res.json['record'], 23)
        self.assertEqual(res.json['play'], 50)
