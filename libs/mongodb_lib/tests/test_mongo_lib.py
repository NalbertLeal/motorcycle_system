import unittest

import pymongo

from mongodb_lib.connection import create_connection
from mongodb_lib.collection import access_collection
from mongodb_lib.query import get_all, get_by_id
from mongodb_lib.change import delete_all, insert_one

class TestKafkaLib(unittest.TestCase):
    def test_mongo_connection(self):
        try:
            host = 'localhost'
            port = '27017'
            user = 'root'
            password = '231564'
            create_connection(host, port, user, password)

            self.assertTrue(True)
        except:
            self.assertTrue(False)
    
    def test_access_collection(self):
        try:
            host = 'localhost'
            port = '27017'
            user = 'root'
            password = '231564'
            conn = create_connection(host, port, user, password)

            access_collection(conn, 'some_db', 'some_collection')

            self.assertTrue(True)
        except:
            self.assertTrue(False)
    
    def test_get_all(self):
        try:
            # setup test
            host = 'localhost'
            port = '27017'
            user = 'root'
            password = '231564'
            conn = create_connection(host, port, user, password)

            some_collection = access_collection(conn, 'some_db', 'some_collection')
            delete_all(some_collection)
            insert_one(
                some_collection,
                {
                    'field_1': 1,
                    'field_2': 2,
                }
            )
            insert_one(
                some_collection,
                {
                    'field_3': 3,
                    'field_4': 4,
                }
            )

            # test
            all_objects = get_all(some_collection)
            if len(all_objects) == 2:
                self.assertTrue(True)
            else:
                self.assertTrue(False)

            # after test
            delete_all(some_collection)
        except:
            self.assertTrue(False)
    
    def test_get_by_id(self):
        try:
            # setup test
            host = 'localhost'
            port = '27017'
            user = 'root'
            password = '231564'
            conn = create_connection(host, port, user, password)

            some_collection = access_collection(conn, 'some_db', 'some_collection')
            delete_all(some_collection)
            id_1 = insert_one(
                some_collection,
                {
                    'field_1': 1,
                    'field_2': 2,
                }
            )
            id_2 = insert_one(
                some_collection,
                {
                    'field_3': 3,
                    'field_4': 4,
                }
            )

            # test
            obj_1 = get_by_id(some_collection, id_1)
            obj_2 = get_by_id(some_collection, id_2)
            if obj_1.get('field_1', '') == 1 and\
                obj_2.get('field_3', '') == 3:
                self.assertTrue(True)
            else:
                self.assertTrue(False)

            # after test
            delete_all(some_collection)
        except:
            self.assertTrue(False)