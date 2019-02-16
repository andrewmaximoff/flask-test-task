# flask-test-task

~~~bash
$ pipenv install
$ pipenv shell
(flask-test-task)$ export $(cat config/.env)
(flask-test-task)$ docker-compose up -d
(flask-test-task)$ flask db init
(flask-test-task)$ flask db migrate
(flask-test-task)$ flask db upgrade
(flask-test-task)$ flask run
~~~
