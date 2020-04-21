SHELL=/bin/bash
export ENV=dev

.PHONY: python-dependencies
python-dependencies:
	pip3 install -r requirements.txt

.PHONY: test
test:
	pip3 install -r requirements.txt && cd ./assignment && python3 manage.py test

.PHONY: serve-application
serve-application:
	docker build -t wikiracer . && docker run -p 8000:8000 -t wikiracer

.PHONY: build
build:
	docker build -t wikiracer . 

.PHONY: run
run:
	docker run -p 8000:8000 -t wikiracer

	

# .PHONY: test
# test:
# 	docker build . -t wikiracer

# cd wikiracer && <ANOTHER COMMAND> && <ANOTHER COMMAND>