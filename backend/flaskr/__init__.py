import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.exceptions import HTTPException

from models import setup_db, Question, Category
from .helper import *

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,PATCH,DELETE,OPTIONS')
        return response
    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route("/categories")
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        return jsonify({
            "status_code": 200,
            "total": len(categories),
            "success": True,
            "categories": {category.id: category.type
                           for category in categories}
        })

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of
    the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route("/questions")
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = helper.paginate_questions(request, selection)
        categories = Category.query.order_by(Category.id).all()
        if not current_questions:
            abort(404)

        return jsonify({
            "status_code": 200,
            "total_questions": len(selection),
            "success": True,
            "categories": {category.id: category.type
                           for category in categories},
            "current_category": None,
            "questions": current_questions
        })

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()

            if not question:
                abort(404)

            question.delete()
            total_questions = Question.query.count()

            return jsonify({
                "status_code": 200,
                "success": True,
                "total_questions": total_questions
            })

        except HTTPException as e:
            if e.code == 404:
                raise
        except:
            abort(422)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the
    end of the last page
    of the questions list in the "List" tab.
    '''

    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        if not helper.is_valid_question(body):
            abort(422)

        question = body.get("question")
        answer = body.get("answer")
        difficulty = body.get("difficulty")
        category_id = body.get("category")

        try:
            last_question = Question.query.order_by(Question.id.desc()).first()
            new_question = Question(question=question, answer=answer,
                                    difficulty=difficulty,
                                    category_id=category_id)
            new_question.id = last_question.id + 1
            new_question.insert()

            return jsonify({
                "status_code": 200,
                "success": True,
                "created_question": new_question.id
            })
        except:
            abort(422)

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route("/questions/search", methods=["POST"])
    def search_question():
        body = request.get_json()
        search_term = body.get("searchTerm", None)

        if not search_term:
            abort(400)

        results = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()

        if not results:
            abort(404)

        return jsonify(
            {
                "status_code": 200,
                "success": True,
                "questions": [question.format() for question in results],
                "totalQuestions": len(results),
                "currentCategory": None
            }
        )

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route("/categories/<int:id>/questions")
    def get_questions_by_category(id):
        category = Category.query.filter(Category.id == id).one_or_none()

        if not category:
            abort(404)

        return jsonify({
            "status_code": 200,
            "success": True,
            "questions": [question.format()
                          for question in category.questions],
            "totalQuestions": len(category.questions),
            "currentCategory": category.id
        })

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route("/quizzes", methods=["POST"])
    def get_next_question():
        body = request.get_json()
        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)

        try:
            query = build_quiz_query(body)
            results = query.all()
            current_question = None
            if results:
                question = random.choice(results)
                current_question = question.format()

            return jsonify({
                "status_code": 200,
                "success": True,
                "previousQuestions": previous_questions,
                "question": current_question
            })
        except:
            abort(400)

    def build_quiz_query(body):
        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)

        query = Question.query

        if quiz_category and quiz_category["id"]:
            query = query.filter(Question.category_id == quiz_category["id"])
        if previous_questions:
            query = query.filter(~Question.id.in_(previous_questions))

        return query
    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
