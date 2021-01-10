import os
import unittest
import json
import sys
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    """
    Populate database with example data
    """
    def populatedb(self, db):
        category1 = Category(type="science")
        question1 = Question(question="oxigen symbol", answer="o", category_id=1, difficulty=1)
        question2 = Question(question="sodium symbol", answer="na", category_id=1, difficulty=2)
        question3 = Question(question="water composition", answer="h2o", category_id=1, difficulty=3)
        question4 = Question(question="hydrogen peroxide composition", answer="h2o2", category_id=1, difficulty=4)
        question5 = Question(question="vitamin c composition", answer="c6h8o6", category_id=1, difficulty=5)

        category2 = Category(type="dragon ball")
        question6 = Question(question="goku last name", answer="son", category_id=2, difficulty=1)
        question7 = Question(question="goku 2nd son", answer="goten", category_id=2, difficulty=2)
        question8 = Question(question="saiyan prince", answer="vegeta", category_id=2, difficulty=3)
        question9 = Question(question="goku mom name", answer="gine", category_id=2, difficulty=5)
        question10 = Question(question="frieza dad name", answer="cold", category_id=2, difficulty=4)

        category3 = Category(type="latam sports")
        question11 = Question(question="best international soccer team from south america", answer="boca", category_id=3, difficulty=1)
        question12 = Question(question="best ecuadorian soccer team", answer="ldu", category_id=3, difficulty=2)
        question13 = Question(question="2nd best ecuadorian soccer team", answer="idv", category_id=3, difficulty=3)
        question14 = Question(question="Ecuadorian olympics gold winner in Athlanta '96", answer="jefferson perez", category_id=3, difficulty=5)
        question15 = Question(question="2nd best soccer team in argentina", answer="river", category_id=3, difficulty=4)

        questions1 = [question1, question2, question3, question4, question5]
        questions2 = [question6, question7, question8, question9, question10]
        questions3 = [question11, question12, question13, question14, question15]

        category1.questions = questions1
        category2.questions = questions2
        category3.questions = questions3

        try:
            db.session.add(category1)
            db.session.add(category2)
            db.session.add(category3)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

        

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}@{}/{}".format('marlon:admin','localhost:5442', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            self.populatedb(self.db)
    
    def tearDown(self):
        with self.app.app_context():
            #drop tables
            Question.__table__.drop(self.db.engine)
            Category.__table__.drop(self.db.engine)

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        total_categories_expected = 3
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["total"], total_categories_expected)
        self.assertTrue(data["success"])
        self.assertTrue(len(data["categories"]))
        self.assertEqual(len(data["categories"]), total_categories_expected)
        self.assertTrue(lambda x: x["type"] == "dragon ball" in data["categories"])

    def test_get_paginated_questions(self):
        total_questions_expected = 15
        total_paginated_questions_expected = 10
        total_categories_expected = 3
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["total_questions"], total_questions_expected)
        self.assertEqual(len(data["questions"]), total_paginated_questions_expected)
        self.assertEqual(len(data["categories"]), total_categories_expected)

    def test_404_sent_invalid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()