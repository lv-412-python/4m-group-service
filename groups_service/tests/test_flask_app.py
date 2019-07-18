"""Tests for form service."""
from unittest import main
from flask_testing import TestCase

from groups_service import APP
from groups_service.config.test_config import TestConfiguration
from groups_service.db import DB
from groups_service.models.group import Groups, Forms

def create_app(config_obj):
    """
    Creates Flask app with configuration, you need.
    :param config_obj: name of configuration.
    :return: flask app.
    """
    app = APP
    app.config.from_object(config_obj)
    return app

class GetPutTest(TestCase):
    """Tests for get, put and delete resources with the same set-up."""

    def create_app(self):
        """
        Creates Flask app with Test Configuration.
        :return: flask app.
        """
        return create_app(TestConfiguration)

    def setUp(self):
        """Creates tables and puts objects into database."""
        DB.create_all()
        form1 = Forms(1)
        form2 = Forms(2)
        form3 = Forms(3)
        group1 = Groups("Test", 2, "1, 3, 4, 5", [form1, form2])
        group2 = Groups("Another test", 3, "1, 6, 4, 5", [form1, form3, form2])
        DB.session.add(group1)
        DB.session.add(group2)
        DB.session.commit()
        id1 = Groups.query.filter_by("Test", 2, "1, 3, 4, 5", [form1, form2]).first()
        self.group_id_1 = id1.id
        id2 = Groups.query.filter_by("Another test", 3, "1, 6, 4, 5", [form1, form3, form2]).first()
        self.group_id_2 = id2.id

    def tearDown(self):
        """Drops all tables."""
        DB.session.remove()
        DB.drop_all()

    def test_get_all_groups(self):
        """Tests get method to get all forms by some owner."""
        with self.create_app().test_client() as client:
            response = client.get('/group')
            check = [{
                "title": "Test",
                "owner_id": 2,
                "members": [1, 3, 4, 5],
                "assigned_to_forms": [1, 2]
            }, {
                "title": "Another test",
                "owner_id": 3,
                "members": [1, 6, 4, 5],
                "assigned_to_forms": [1, 3, 2]
            }]
            self.assertEqual(response.json, check)

    def test_get_one_form(self):
        """Tests get method to get one particular form."""
        with self.create_app().test_client() as client:
            response = client.get('/form/{}'.format(self.group_id_1))
            check = {
                "title": "Test",
                "owner_id": 2,
                "members": [1, 3, 4, 5],
                "assigned_to_forms": [1, 2]
            }
            self.assertEqual(response.json, check)

    def test_get_no_data(self):
        """Tests get method with id that does not exist."""
        with self.create_app().test_client() as client:
            response = client.get('/group/123464367')
            self.assertEqual(response.json, {'error': 'Does not exist.'})

    def test_put(self):
        """Tests put method."""
        with self.create_app().test_client() as client:
            new = {
                "title": "Test",
                "owner_id": 9,
                "members": [1, 3, 4, 5],
                "assigned_to_forms": [1, 2]
            }
            response = client.put('/form/{}'.format(self.group_id_1), json=new)
            self.assertEqual(response.status_code, 200)

    def test_put_no_form(self):
        """Tests put method."""
        with self.create_app().test_client() as client:
            response = client.put('/group/13575836')
            self.assertEqual(response.json, {'error': 'Does not exist.'})

class PostTest(TestCase):
    """Tests for post method."""

    def create_app(self):
        """
        Creates Flask app with Test Configuration.
        :return: flask app.
        """
        return create_app(TestConfiguration)

    def setUp(self):
        """Creates tables."""
        DB.create_all()

    def test_post_success(self):
        """Tests post resource success."""
        with self.create_app().test_client() as client:
            response = client.post('/group',
                                   json={"title": "Test", "owner_id": 2, "members": [1, 4, 8],
                                         "assigned_to_forms": [1, 2]})
            self.assertEqual(response.status_code, 201)

    def test_post_failure(self):
        """Tests post resource failure."""
        with self.create_app().test_client() as client:
            client.post('/group', json={"title": "Test", "owner_id": 2, "members": [1, 4, 8],
                                        "assigned_to_forms": [1, 2]})
            response = client.post('/group')
            self.assertEqual(response.status_code, 400)

    def tearDown(self):
        """Drops all tables."""
        DB.session.remove()
        DB.drop_all()


if __name__ == '__main__':
    main()
