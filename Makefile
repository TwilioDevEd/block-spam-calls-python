.PHONY: venv install
UNAME := $(shell uname)
venv:
	python -m venv venv

install:
ifeq ($(UNAME), Windows)
	py -3 -m venv venv; venv\Scripts\activate.bat;
endif
ifeq ($(UNAME), Linux)
	virtualenv venv; bash -c "source ./venv/bin/activate";
endif
ifeq ($(UNAME), Darwin)
	venv
	. venv/bin/activate;
endif
	pip3 install -r requirements.txt;

serve:
	python3 block_spam_calls/app.py
