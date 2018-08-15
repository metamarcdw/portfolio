
init:
	pip install -r requirements.txt
	git clone https://github.com/wzuo/Flask-Images.git ../Flask-Images
	pip install -e ../Flask-Images

go:
	export PORTFOLIO_MODE=development && export PORTFOLIO_DB=localhost && python -m server

.PHONY: init go
