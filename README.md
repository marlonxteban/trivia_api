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
