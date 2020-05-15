.PHONY: venv install
UNAME := $(shell uname)
venv:
ifeq ($(UNAME), Windows)
	py -3 -m venv venv;
else
	python3 -m venv venv
endif
install: venv
ifeq ($(UNAME), Windows)
	venv\Scripts\activate.bat;
else
	. venv/bin/activate;
endif
	pip3 install -r requirements.txt;
serve:
	python3 block_spam_calls/app.py
