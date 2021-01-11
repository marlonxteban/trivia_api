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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        #change database_path with the following to use the docker environment
        #self.database_path = "postgres://{}@{}/{}".format('marlon:admin','localhost:5442', self.database_name)
        #changed port from 5432 to 5442 to use local container environment
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

    def test_delete_question(self):
        total_questions_expected = 14
        res = self.client().delete("/questions/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["total_questions"], total_questions_expected)

    def test_404_sent_nonexistent_id(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], 'resource not found')

    def test_create_question(self):
        new_question = {
            "question": "is this a new question?",
            "answer": "yes",
            "category": 1,
            "difficulty": 1
        }

        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created_question"])

    def test_422_missing_category(self):
        new_question = {
            "question": "is this a new question?",
            "answer": "yes",
            "difficulty": 1
        }

        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable")

    def test_422_missing_difficulty(self):
        new_question = {
            "question": "is this a new question?",
            "answer": "yes",
            "category": 1
        }

        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable")

    def test_search_soccer_in_question(self):
        search_term = {
            "searchTerm":"soccer"
        }
        expected_questions = 4
        res = self.client().post("/questions/search", json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["totalQuestions"], expected_questions)
        self.assertEqual(len(data["questions"]), expected_questions)

    def test_404_no_results_for_searchTerm(self):
        search_term = {
            "searchTerm":"parangaricutirimicuaro"
        }
        res = self.client().post("/questions/search", json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], 'resource not found')

    def test_400_no_searchTerm(self):
        search_term = {
            "searchTerm":None
        }
        res = self.client().post("/questions/search", json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], 'bad request')

    def test_questions_by_category(self):
        expected_category_id = 1
        expected_questions = 5

        res = self.client().get(f"/categories/{expected_category_id}/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["questions"]), expected_questions)
        self.assertEqual(data["totalQuestions"], expected_questions)
        self.assertEqual(data["currentCategory"], expected_category_id)

    def test_404_category_not_exist(self):
        category_id = 9999

        res = self.client().get(f"/categories/{category_id}/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], 'resource not found')

    def test_quizzes_return_different_question_at_time_no_category(self):
        params = {
            "previous_questions": [],
            "quiz_category": None
        }

        res = self.client().post("/quizzes", json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertFalse(data["previousQuestions"])
        self.assertTrue(data["question"])

        params2 = {
            "previous_questions": [data["question"]["id"]],
            "quiz_category": None
        }
        res2 = self.client().post("/quizzes", json=params2)
        data2 = json.loads(res2.data)

        self.assertEqual(res2.status_code, 200)
        self.assertTrue(data2["success"])
        self.assertEqual(data2["previousQuestions"], params2["previous_questions"])
        self.assertTrue(data2["question"])
        self.assertNotEqual(data2["question"], data["question"])

    def test_400_sent_invalid_category(self):
        params = {
            "previous_questions": [],
            "quiz_category": "bad"
        }

        res = self.client().post("/quizzes", json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()