ruff:
	ruff check --fix --show-fixes .
	ruff check --select F401 --fix --show-fixes .
	ruff format .

indenter:
	find backend -name "*.html" | xargs djhtml -t 2

autopep8:
	find backend -name "*.py" | xargs autopep8 --max-line-length 120 --in-place

isort:
	isort -m 3 * --skip migrations --skip .venv

lint: ruff indenter
