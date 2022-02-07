init:
	pip install -r requirements.txt

format:
	yapf --style .style.yapf -r -i beatrice/backend/app

lint:
	pylint --rcfile .pylintrc beatrice/backend/app

run:
	( cd beatrice/backend; uvicorn app.main:app --reload )

.PHONY: init
