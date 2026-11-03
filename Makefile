all: clean build
clean:
	rm -rf build

.venv:
	python3 -m venv .venv
	source .venv/bin/activate ;\
	pip3 install -r requirements.txt

build: .venv
	mkdir build
	cp template/* build/
	source .venv/bin/activate ; \
	python3 build.py