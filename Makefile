VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
REQS = requirements.txt

.PHONY: setup clean

setup: $(VENV)/bin/activate
	echo "Virtual environment created at $(VENV). Run `make clean` to remove environment"

$(VENV)/bin/activate: $(REQS)
	python3 -m venv $(VENV)
	$(PIP) install -r $(REQS)

clean:
	rm -rf __pycache__
	rm -rf $(VENV)