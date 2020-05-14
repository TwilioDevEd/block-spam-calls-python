UNAME := $(shell uname)
install:
ifeq ($(UNAME), Windows)
	py -3 -m venv venv; venv\Scripts\activate.bat;
else
	virtualenv venv; . venv/bin/activate;
endif
	pip3 install -r requirements.txt;

serve:
	python3 block_spam_calls/app.py
