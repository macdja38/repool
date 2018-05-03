# Copyright (C) 2014  Nicolas Jouanin
#
# This file is part of repool.
#
# Repool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Repool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Repool.  If not, see <http://www.gnu.org/licenses/>.
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
# import logging
from repool import ConnectionPool, ConnectionWrapper


# logging.basicConfig(level="DEBUG")

class TestPool(unittest.TestCase):
    @patch('repool.pool.r')
    def test_create_pool(self, mock_r):
        mock_r.connect = MagicMock()
        mock_r.close = MagicMock()
        from repool.pool import ConnectionPool
        p = ConnectionPool(cleanup=1)
        self.assertFalse(p.empty())
        p.release_pool()

    @patch('repool.pool.r')
    def test_acquire_release_one(self, mock_r):
        mock_r.connect = MagicMock()
        mock_r.close = MagicMock()
        from repool.pool import ConnectionPool
        p = ConnectionPool(cleanup=1)
        nb_init = p._pool.qsize()
        conn = p.acquire()
        p.release(conn)
        nb_term = p._pool.qsize()
        self.assertEqual(nb_init, nb_term)
        p.release_pool()

    @patch('repool.pool.r')
    def test_acquire_one(self, mock_r):
        mock_r.connect = MagicMock()
        mock_r.close = MagicMock()
        from repool.pool import ConnectionPool
        p = ConnectionPool(cleanup=1)
        nb_init = p._pool.qsize()
        conn = p.acquire()
        nb_term = p._pool.qsize()
        self.assertEqual(nb_init - 1, nb_term)
        p.release(conn)
        p.release_pool()

    @patch('repool.pool.r')
    def test_acquire(self, mock_r):
        mock_r.connect = MagicMock()
        mock_r.close = MagicMock()
        from repool.pool import ConnectionPool
        p = ConnectionPool(cleanup=1)
        conn = p.acquire()
        self.assertIsInstance(conn, MagicMock)
        p.release(conn)
        p.release_pool()

    @patch('repool.pool.r')
    def test_release_pool(self, mock_r):
        mock_r.connect = MagicMock()
        mock_r.close = MagicMock()
        from repool.pool import ConnectionPool, PoolException
        p = ConnectionPool(cleanup=1)
        conn1 = p.acquire()
        conn2 = p.acquire()
        p.release(conn1)
        with self.assertRaises(PoolException):
            p.release_pool()

    @patch('repool.pool.r')
    def test_connect(self, mock_r):
        mock_r.connect = MagicMock()
        mock_r.close = MagicMock()
        from repool.pool import ConnectionPool
        p = ConnectionPool(pool_size=1)
        with p.connect() as conn:
            self.assertEqual(0, p._pool.qsize())
        self.assertEqual(1, p._pool.qsize())
        p.release_pool()