import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    """
    Populate database with example data
    """
    def populatedb(self, db):
        category1 = Category(type="cience")
        question1 = Question(question="oxigen symbol", answer="o", category=category1.type, difficulty=1)
        question2 = Question(question="sodium symbol", answer="na", category=category1.type, difficulty=2)
        question3 = Question(question="water composition", answer="h2o", category=category1.type, difficulty=3)
        question4 = Question(question="hydrogen peroxide composition", answer="h2o2", category=category1.type, difficulty=4)
        question5 = Question(question="vitamin c composition", answer="c6h8o6", category=category1.type, difficulty=5)

        category2 = Category(type="dragon ball")
        question6 = Question(question="goku last name", answer="son", category=category2.type, difficulty=1)
        question7 = Question(question="goku 2nd son", answer="goten", category=category2.type, difficulty=2)
        question8 = Question(question="saiyan prince", answer="vegeta", category=category2.type, difficulty=3)
        question9 = Question(question="goku mom name", answer="gine", category=category2.type, difficulty=5)
        question10 = Question(question="frieza dad name", answer="cold", category=category2.type, difficulty=4)
        
        questions = [question1, question2, question3, question4, question5, question6, question7, question8, question9, question10]

        try:
            db.session.add(category1)
            db.session.add(category2)
            for question in questions:
                db.session.add(question)
        
            db.session.commit()
        except expression as identifier:
            db.session.rollback()

        

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
        """Executed after reach test"""
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.session.query(Question).delete()
            self.db.session.query(Category).delete()
            self.db.session.commit()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["total"], 2)
        self.assertTrue(data["success"])
        self.assertTrue(len(data["categories"]))
        self.assertEqual(len(data["categories"]), 2)
        self.assertTrue(lambda x: x["type"] == "dragon ball" in data["categories"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()