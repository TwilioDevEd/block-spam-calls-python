UNAME := $(shell uname)
install:
ifeq ($(UNAME), Windows)
	py -3 -m venv venv; venv\Scripts\activate.bat;
endif
ifeq ($(UNAME), Darwin)
	virtualenv venv; source ./venv/bin/activate;
endif
ifeq ($(UNAME), Linux)
	virtualenv venv; $(shell source ./venv/bin/activate)
endif
	pip3 install -r requirements.txt;

serve:
	python3 block_spam_calls/app.py
