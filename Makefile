init:
	source bin/activate

run: init
	python3 main.py

update_deps: init
	