venv:
	. beatrice/backend/.venv/bin/activate

format:
	yapf --style beatrice/backend/.style.yapf -r -i beatrice/backend/app

lint:
	pylint --rcfile beatrice/backend/.pylintrc beatrice/backend/app

run:
	( cd beatrice/backend; uvicorn app.main:app --reload )

init-db:
	( cd beatrice/backend; python -m app.init )

.PHONY: init format lint run init-db
