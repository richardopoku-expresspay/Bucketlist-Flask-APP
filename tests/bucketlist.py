import unittest
import os, json, sys

topdir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(topdir)
from app import db, create_app


class BucketListTestCase(unittest.TestCase):
    '''Represents the bucketlists test case'''


    def setUp(self):
        '''Define test variables and initialize the app.'''
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go to Germany.'}

        with self.app.app_context():
            # create the db migrations
            db.create_all()

    def test_can_create_bucketlist(self):
        '''Test that can create a bucketlist (POST request)'''
        res = self.client().post('/bucketlists', data=self.bucketlist)
        self.assertEqual(res.status_code, 201) # created
        self.assertIn('Go to Germany.', str(res.data))

    def test_can_get_all_bucketlists(self):
        '''Test that can retrieve all the bucketlists (GET request)'''
        res = self.client().post('/bucketlists', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/bucketlists')
        self.assertEqual(res.status_code, 200) # success
        self.assertIn('Go to Germany.', str(res.data))

    def test_can_get_bucketlist_by_id(self):
        '''Test that a bucketlist item can be retrieved by id (GET request)'''
        rv = self.client().post('/bucketlists', data=self.bucketlist)
        self.assertEqual(rv.status_code, 201)
        json_result = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        print(json_result['data']['bucketlist']['id'])
        res = self.client().get('/bucketlists/{}'.format(json_result['data']['bucketlist']['id']))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Germany.', str(res.data))


    def test_can_edit_a_bucketlist(self):
        '''Test that an existing bucketlist item can be edited (PUT request)'''
        rv = self.client().post('/bucketlists', data=self.bucketlist)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put('/bucketlists/1', data={'name': 'Go to USA.'})
        self.assertEqual(rv.status_code, 200)
        res = self.client().get('/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to USA.', str(res.data))

    def test_can_delete_bucketlist(self):
        '''Test that an existing bucketlist item can be deleted (DELETE request)'''
        rv = self.client().post('/bucketlists', data=self.bucketlist)
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        res = self.client().get('/bucketlists/1')
        self.assertEqual(res.status_code, 404) # no longer exists

    def tearDown(self):
        '''Remove all initialized variables.'''
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()