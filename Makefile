.PHONY: up down nuke fetch sql

up:
	python3 -c "from task import up; up()"

down:
	python3 -c "from task import down; down()"

nuke: down up

fetch:
	python3 -c "from task import fetch; fetch()"

sql:
	sqlite3 data.db

# populate:
# 	python3 -c "from task import populate; populate()"