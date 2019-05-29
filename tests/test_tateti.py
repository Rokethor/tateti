#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tateti import Tateti, CELLS, SUCCESS
import unittest
import random

class TestTateti(unittest.TestCase):

    def setUp(self):
        self.tateti = Tateti()

    def test_init_vars(self):
        self.assertIs(type(self.tateti), Tateti)
        self.assertEqual(True, self.tateti.inProgress)
        self.assertIn(self.tateti.turn, (0, 1))

    def test_random_turn(self):
        for i in range(100):
            self.assertIn(self.tateti.randomStart(), (0, 1))

    def test_len_table(self):
        self.assertEqual(330, len(self.tateti.getTableStr([' '] * 10)))

    def test_numbers_in_table(self):
        table = self.tateti.getTableStr([' '] * 10)
        for cell in CELLS:
            self.assertTrue(cell in table)

    def test_full_table(self):
        table1 = ['X', '', 'O', 'O', 'X', 'X', 'O', '', '', '']
        table2 = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O']
        self.assertFalse(self.tateti.fullTable(table1))
        self.assertTrue(self.tateti.fullTable(table2))

    def test_computer_move_ia(self):
        tables = [
            ['', 'X', 'O', '', '', 'O', '', 'X', '', ''],
            ['', '', 'X', '', '', 'O', '', '', 'O', 'X'],
            ['', 'X', 'X', 'O', '', 'X', 'O', '', 'O', ''],
            ['', 'O', 'X', '', '', '', '', 'O', 'X', ''],
            ['', '', 'X', 'X', '', 'X', 'O', 'O', '', ''],
            ['', '', 'X', '', '', 'O', 'O', '', '', ''],
            ['', '', 'X', 'X', '', '', 'O', '', 'O', 'O'],
            ['', 'X', '', 'O', 'X', 'O', '', '', '', ''],
        ]
        letters = ['X', 'O']
        randomInt = self.tateti.randomStart()
        computerLetter = letters[randomInt]
        playerLetter = letters[int(not randomInt)]
        for table in tables:
            self.assertIsNone(self.tateti.getComputerMove(table, computerLetter, playerLetter))

    def test_is_winner_true(self):
        letter = 'X'
        for tup in SUCCESS:
            table = [' '] * 10
            for i in tup:
                table[i] = letter
            self.assertTrue(self.tateti.isWinner(table, letter))

    def test_is_winner_false(self):
        letter = 'X'
        for tup in SUCCESS:
            table = [' '] * 10
            for i in tup:
                table[i] = letter
            x = random.choice([i for i in tup])
            table[x] = 'O'
            self.assertFalse(self.tateti.isWinner(table, letter))
