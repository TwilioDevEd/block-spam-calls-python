.PHONY: venv install
UNAME := $(shell uname)
venv:
ifeq ($(UNAME), Darwin)
	python3 -m venv venv
endif

install: venv
ifeq ($(UNAME), Windows)
	py -3 -m venv venv; venv\Scripts\activate.bat;
endif
ifeq ($(UNAME), Linux)
	virtualenv venv; bash -c "source ./venv/bin/activate";
endif
ifeq ($(UNAME), Darwin)
	. venv/bin/activate;
endif
	pip3 install -r requirements.txt;

serve:
	python3 block_spam_calls/app.py
