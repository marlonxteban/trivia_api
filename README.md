# trivia_api
Project 02 in full stack web developer nanodegree

# Main Changes with the base project

- Updated requirements.txt
- Added migrations
- Added relationship between categories and questions using category id
- Added test data on unit test file setUp
- Drop test tables on unit test file tearDown
- Use docker compose for DB
- used docker to setup and run the database


## Database Setup (skip this if use base project database setup)

For this step (If want to use docker) you need docker[docker](https://www.docker.com/) and docker-compose.

### steps:
- run
```bash
docker-compose up
```
#### Setup pgAdmin4 (for manage postgres database)
- get pgadmin container ID
```bash
docker container ls
```
- get pgadmin Ip:
```bash
docker inspect [container ID]
```
look for `IPAddress:xxx.xxx.xxx.xxx`
- open pgadmin from a browser at `localhost:8889` sign in with user `marlonxteban@gmail.com` and pass `admin` (this values can be changed in file `docker-compose.yml` prior execute docker compose)

- create server in pgAdmin, in `Connection` tab set `Host` with the IP of the container, `Port` with `5432` and `Username` with `marlon` (the value `Username` can be changed in file `docker-compose.yml` prior execute docker compose)

- Create databases `trivia` and `trivia_test`

# Run the server

If tables are not created yet:

- From folder `backend/flaskr/` run
```bash
export FLASK_APP=flaskr
flask db upgrade
```

## Notes:
Scripts to insert demo data are provided in folder `database`, run in order: `00` first then `01`.


# Endpoints

## GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
### response example
```json
    {
      "status_code": 200,
      "total": 1,
      "success": "True",
      "categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	  }
    }
```

## GET '/questions'
- Fetches an array of questions paginated
- Request Arguments: `page` integer as a part of the querystring. if not sent the endpoint return max 10 questions per request.
- Returns: An object that contains the array of paginated questions, the object of categories, the total number of qustions.
### response example
```json
{
	"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	},
	"current_category": null,
	"questions": [{
		"answer": "me",
		"category": 5,
		"difficulty": 1,
		"id": 1,
		"question": "Who is this?"
	}, {
		"answer": "Apollo 13",
		"category": 5,
		"difficulty": 4,
		"id": 2,
		"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
	}, {
		"answer": "Apollo 13",
		"category": 5,
		"difficulty": 4,
		"id": 4,
		"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
	}, {
		"answer": "Maya Angelou",
		"category": 2,
		"difficulty": 4,
		"id": 5,
		"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
	}, {
		"answer": "Edward Scissorhands",
		"category": 5,
		"difficulty": 3,
		"id": 6,
		"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
	}, {
		"answer": "Muhammad Ali",
		"category": 6,
		"difficulty": 1,
		"id": 9,
		"question": "What boxer's original name is Cassius Clay?"
	}, {
		"answer": "Brazil",
		"category": 6,
		"difficulty": 3,
		"id": 10,
		"question": "Which is the only team to play in every soccer World Cup tournament?"
	}, {
		"answer": "Uruguay",
		"category": 6,
		"difficulty": 4,
		"id": 11,
		"question": "Which country won the first ever soccer World Cup in 1930?"
	}, {
		"answer": "George Washington Carver",
		"category": 4,
		"difficulty": 2,
		"id": 12,
		"question": "Who invented Peanut Butter?"
	}, {
		"answer": "Lake Victoria",
		"category": 3,
		"difficulty": 2,
		"id": 13,
		"question": "What is the largest lake in Africa?"
	}],
	"status_code": 200,
	"success": true,
	"total_questions": 20
}
```
## DELETE '/questions/<int:id>'
- Delete question using id
- Request Arguments: `id` integer.
- Returns: An object that contains: `status_code`, `success`, `total_questions` (after delete).
### response example
```json
{
	"status_code": 200,
	"success": true,
	"total_questions": 19
}
```

## POST '/questions'
- Create new question
- Request Arguments: `question` string, `answer`: string, `difficulty`: integer, `category`: integer (category id).
- Returns: An object that contains: `status_code`, `success`, `created_question` (id of new question).
### request body example
```json
{
	"question": "Who is this?",
	"answer": "me",
	"difficulty": 1,
	"category": 5
}
```
### response example
```json
{
	"created_question": 3,
	"status_code": 200,
	"success": true
}
```

## POST '/questions/search'
- Fetches an array of questions that accomplishes a search term.
- Request Arguments: `searchTerm` string.
- Returns: An object that contains: `status_code`, `success`, `questions`, `totalQuestions`.
### request body example
```json
{"searchTerm":"actor"}
```
### response example
```json
{
	"currentCategory": null,
	"questions": [{
		"answer": "Apollo 13",
		"category": 5,
		"difficulty": 4,
		"id": 4,
		"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
	}],
	"status_code": 200,
	"success": true,
	"totalQuestions": 1
}
```

## GET '/categories/<int:id>/questions'
- Fetches an array of questions that accomplishes the category type.
- Request Arguments: `id` integer.
- Returns: An object that contains: `status_code`, `success`, `questions`, `totalQuestions`, `currentCategory`.

### response example
```json
{
	"currentCategory": 1,
	"questions": [{
		"answer": "The Liver",
		"category": 1,
		"difficulty": 4,
		"id": 20,
		"question": "What is the heaviest organ in the human body?"
	}, {
		"answer": "Blood",
		"category": 1,
		"difficulty": 4,
		"id": 22,
		"question": "Hematology is a branch of medicine involving the study of what?"
	}],
	"status_code": 200,
	"success": true,
	"totalQuestions": 2
}
```

## POST '/quizzes'
- Fetches one question to play the trivia filtered by category and previous questions.
- Request Arguments: `previous_questions` Array of ids of questions to filter previous answered questions, `quiz_category` json object that contains type and Id of a category. If not arguments are not sent the question should be of any avaliable category. 
- Returns: An object that contains: `previousQuestions`, `success`, `status_code`, `question`.
### request body example
```json
{
	"previous_questions": [],
	"quiz_category": {
		"type": "Science",
		"id": "1"
	}
}
```
### response example
```json
{
	"previousQuestions": [],
	"question": {
		"answer": "Blood",
		"category": 1,
		"difficulty": 4,
		"id": 22,
		"question": "Hematology is a branch of medicine involving the study of what?"
	},
	"status_code": 200,
	"success": true
}
