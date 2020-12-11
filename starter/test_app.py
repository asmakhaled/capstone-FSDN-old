import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies


class AgencyTestCase(unittest.TestCase):
    """This class represents the Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency"
        self.database_path = "postgres://{}@{}/{}".format(
            'postgres:1234', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.assistant_token = {
            'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBFMW02cW1xc09yUDc3SlZKeGRMZSJ9.eyJpc3MiOiJodHRwczovL2FzbWEta2hhbGVkLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMzE4MDk2NjQ0NzQwNTgwMjMzOSIsImF1ZCI6WyJhZ2VuY3ktYXBpIiwiaHR0cHM6Ly9hc21hLWtoYWxlZC5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjA3NzAzMjgwLCJleHAiOjE2MDc3ODk2ODAsImF6cCI6IjFPeTNGNE12b3hDcENQdWRnaTZZQnZYSW1LUTQxbUtLIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.hozjWRVHfRGqQIP_oFoUifSiqu3Uo3K3yuO6ScjhWX5U8RgN1ED5q-rt34_LKVEPRC0wNgmGcdrzL6898S1T6Gmnb0L78kVSvZExOSAwqxpA9Ax69T2SvldO9gotVLyQCf-ZK1n2BuctOJq6stPd-kSdr_6HkhGjd3fBrGfO-llLHREB_FlAUiM7rG1BavTjwmPlSYwg91TaaHjvpCJpVdsTYygMemCsHZkUCrs7NyGDpqOik86nwTt8YZhsK-Oa5mqdME2A03IcBW9RjOkwzcux3TQyJH32N9MY6T5y863gdL5hD8HzwnykBilfUFr4NfI449-ysVdXYqEbMS8Y8Q'
        }

        self.director_token = {
            'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBFMW02cW1xc09yUDc3SlZKeGRMZSJ9.eyJpc3MiOiJodHRwczovL2FzbWEta2hhbGVkLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmQwYTVjM2Q4NWEyYzAwNmVkYjU2MzMiLCJhdWQiOiJhZ2VuY3ktYXBpIiwiaWF0IjoxNjA3NzAzNDAyLCJleHAiOjE2MDc3ODk4MDIsImF6cCI6IjFPeTNGNE12b3hDcENQdWRnaTZZQnZYSW1LUTQxbUtLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.rK1Ao4IegV-533h4qdRL83mULoek-Bx0MsNf8oJw65Fmqbwm-0xHjWpgzreeTQRIE84ngQPkQoECB6izEF7B7W8Z_6TMUAGp5hP05rrPvRm-DROe8fvN4o23tbNw5wV4kWSdGQvPC7xNUFXqOGYWsd-KO2tKs4PkyiCZAWmsZbUFHfVf6Qoi2iLqIONMW17t6MONvFsVQX78VS0LprlliwEBC_2Q8jqvtKjv-36s0wjSPH6mNfQsSKC6IW5NcIF_opK43sb6ixhJm2x5YRKwvsfvTAftwch-0bm3otAdlruIgzAP0WIbLm_Yc5RxOToRx2E2qRxKwfXlQZyyiZd0Ww'
        }

        self.producer_token = {
            'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBFMW02cW1xc09yUDc3SlZKeGRMZSJ9.eyJpc3MiOiJodHRwczovL2FzbWEta2hhbGVkLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMjQyMTI2NjI3MDExNTE5Nzc5MiIsImF1ZCI6WyJhZ2VuY3ktYXBpIiwiaHR0cHM6Ly9hc21hLWtoYWxlZC5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjA3NzAzNDg3LCJleHAiOjE2MDc3ODk4ODcsImF6cCI6IjFPeTNGNE12b3hDcENQdWRnaTZZQnZYSW1LUTQxbUtLIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.FDJfvswb7hG8q0xJBuYRy5feEQXmo_j9Uya-dRllcDgHWDZF2U1TGSnuzDvcgpochx_zcGHGyu81jqFxCzkIY_4t1TABRlc-x6K_iZQcatxcrmpmvUcq7np8g9OfN7rQurqewhVUgIgfDtno14WMBxTLKE3XlxuLY7KlN9hfh_IpN-X_RhdFbUmkJlR04OJUdlE5FIYyE8v8MB-oRpFfW23MOuRjC0OaSW9ptTWvNT4_N8aGbncMqdkR-e5Xh82vGiOZN7EM1KqS6t1VJtRezv8wN2-Bi9Kv0rd_mPwuQcH2lylTDxxYZIV2bMKg4FpyGhTF92IBmIIwaou1UkDRsA'
        }

        self.unauthorized_token = {
            'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBFMW02cW1xc09yUDc3SlZKeGRMZSJ9.eyJpc3MiOiJodHRwczovL2FzbWEta2hhbGVkLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmQzNmJhMmM3ZjEzNjAwNzlmZTRkMmIiLCJhdWQiOiJhZ2VuY3ktYXBpIiwiaWF0IjoxNjA3NzAzNTg0LCJleHAiOjE2MDc3ODk5ODQsImF6cCI6IjFPeTNGNE12b3hDcENQdWRnaTZZQnZYSW1LUTQxbUtLIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6W119.BKq1wLMOyO5iec1rSVc5Dt17RSma0cbd9Bd-eNgjeMH8d_7fUbOrjDZFhWnkNoXVdtNreGdY0Hw3vMix7XfbT1qgaYixIhjaBGlmRux7zr6DOyFwt4QxRwthxBuo41b-rMZa3rSWd0q6VKYOMOSTChgBP0ya-4f0lY6jR4NoOMYhioYQUBP54UPlWwJ6qTbRX4mPyc1H0HJJ0zSLrEXcnizxc8O7DFVX0JXyWFxhuZndrdSiyom7-YgKFS5zz8OKe5LIY5HED_DU5vNIdPEb5X6Kfu4tFqyR_FTHcoCDPyRevfkc6aYOLg-tChliXuMtbTEQOzudwJSSVMkulmvO4g'
        }

        self.new_actor = {
            'name': 'liam neeson',
            'age': 68,
            'gender': 'male'
        }

        self.new_movie = {
            'title': 'Non-Stop',
            'date': 'February 28, 2014'
        }

        self.new_age = {'age': 30}

        self.new_title = {'title': 'Unknown'}

        self.wrong_actor = {
            'name': 'johnny depp',
            'age': 57,
            'gender': ''
        }

        self.wrong_movie = {
            'title': 'Bird Box',
            'date': ''
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test for successful operation.
    """

    # test get actors
    def test_get_actors(self):
        res = self.client().get(
            '/actors', headers=self.assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # test get movies
    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers=self.assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # test add actor
    def test_add_actor(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['totalActors'])

    # test add movie
    def test_add_movie(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['totalMovies'])

    # test edit actor
    def test_edit_actor(self):
        res = self.client().patch(
            '/actors/1',
            json=self.new_age,
            headers=self.director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['age'])

    # test edit movie
    def test_edit_movie(self):
        res = self.client().patch(
            '/movies/1',
            json=self.new_title,
            headers=self.director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['title'])

    # test delete an actor
    def test_delete_actors(self):
        res = self.client().delete(
            '/actors/2', headers=self.producer_token)
        data = json.loads(res.data)

        #actor = Actors.query.filter(Actors.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    # test delete a movie
    def test_delete_actors(self):
        res = self.client().delete(
            '/movies/2', headers=self.producer_token)
        data = json.loads(res.data)

        #movie = Movies.query.filter(Movies.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    """
    Test for expected errors
    """

    # test request get movies with unauthorized token
    def test_403_unauthorized_get_actors(self):
        res = self.client().get(
            '/actors', headers=self.unauthorized_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    # test request get actors with unauthorized token
    def test_403_unauthorized_get_movies(self):
        res = self.client().get(
            '/movies', headers=self.unauthorized_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    # test request post actor with assistant token
    def test_403_unauthorized_post_actor(self):
        res = self.client().post(
            '/actors', headers=self.assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    # test request delete movie with director token
    def test_403_unauthorized_delete_movie(self):
        res = self.client().delete(
            '/movies/1', headers=self.director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    # test if we want to delete an actor that does not
    # exists

    def test_422_delete_unavailable_actor(self):
        res = self.client().delete(
            '/actors/1000', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # test if we want to delete a movie that does not exists
    def test_422_delete_unavailable_movie(self):
        res = self.client().delete(
            '/movies/1000', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # test if the add actor failed
    def test_422_add_actor_failed(self):
        res = self.client().post(
            '/actors',
            json=self.wrong_actor,
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # test if the add movie failed
    def test_422_add_movie_failed(self):
        res = self.client().post(
            '/actors',
            json=self.wrong_movie,
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # test if the edit actor failed
    def test_404_edit_actor_failed(self):
        res = self.client().patch(
            '/actors/1000',
            json=self.new_age,
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'resource not found')

    # test if the edit movie failed
    def test_404_edit_movie_failed(self):
        res = self.client().patch(
            '/movies/1000',
            json=self.new_title,
            headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
