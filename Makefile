.PHONY: fetch db-up db-down nuke-db

fetch:
	python3 -c "from runner import fetch; fetch()"

db-up:
	python3 -c "from runner import db_up; db_up()"

db-down:
	python3 -c "from runner import db_down; db_down()"

nuke-db: db-down db-up
