init:
	pip install -r requirements.txt

format:
	yapf --style .style.yapf -r -i beatrice/backend/app

lint:
	pylint --rcfile .pylintrc beatrice/backend/app

run:
	( cd beatrice/backend; uvicorn app.main:app --reload )

init-db:
	( cd beatrice/backend; python -m app.init )

.PHONY: init format lint run init-db
