VENV = .venv/
PYTHON = $(VENV)/bin/python3
PIP = $(PYTHON) -m pip
REQS = requirements.txt

DATA = data/
RESULTS = results/

.PHONY: setup run clean

setup: $(VENV)/bin/activate
	@echo "Virtual environment ready at $(VENV).\n\n"

run: $(VENV)/bin/activate $(RESULTS) $(DATA)/arxiv/multiplex.edgelist $(DATA)/celegans/multiplex.edgelist
	$(PYTHON) recreate_real-multiplex_reconstruction.py

$(VENV)/bin/activate: $(REQS)
	@echo "Creating a virtual environment...\n\n"
	@python3 -m venv $(VENV)
	@echo "Installing required packages (install log at .logs/install_log.log)...\n\n"
	@if ! [ -d .logs/ ]; then mkdir .logs/; fi
	@$(PIP) install -r $(REQS) 1> .logs/install_log.log
	@echo "Virtual environment created!\n\n"

$(DATA): $(VENV)/bin/activate
	if ! [ -d $(DATA) ]; then mkdir $(DATA); fi
	@whiptail --msgbox "TESTING" 12 12

$(RESULTS): $(DATA)
	if ! [ -d $(RESULTS) ]; then mkdir $(RESULTS); fi

$(DATA)/arxiv/multiplex.edgelist: $(DATA) $(RESULTS)
	if ! [ -d $(DATA)/arxiv ]; then mkdir $(DATA)/arxiv; fi
	curl -o $(DATA)/arxiv_raw.zip https://manliodedomenico.com/data/arXiv-Netscience_Multiplex_Coauthorship.zip
	unzip -d $(DATA)/arxiv/ $(DATA)/arxiv_raw.zip
	rm -rf $(DATA)/arxiv_raw.zip $(DATA)/arxiv/__MACOSX/
	grep "^[267]" $(DATA)/arxiv/arXiv-Netscience_Multiplex_Coauthorship/Dataset/arxiv_netscience_multiplex.edges > $(DATA)/arxiv/multiplex.edgelist
	@whiptail --msgbox "THATS IT FOR NOW, CHIEF" 12 12

$(DATA)/celegans/multiplex.edgelist: $(DATA) $(RESULTS)
	if ! [ -d $(DATA)/celegans ]; then mkdir $(DATA)/celegans; fi
	curl -o $(DATA)/celegans_raw.zip https://manliodedomenico.com/data/CElegans_Multiplex_Neuronal.zip
	unzip -d $(DATA)/celegans/ $(DATA)/celegans_raw.zip
	rm -rf $(DATA)/celegans_raw.zip $(DATA)/celegans/__MACOSX/
	cp $(DATA)/celegans/CElegans_Multiplex_Neuronal/Dataset/celegans_connectome_multiplex.edges $(DATA)/celegans/multiplex.edgelist
	@whiptail --msgbox "THATS IT FOR NOW, CHIEF" 12 12


clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	if [ -d $(DATA)/arxiv/ ]; then rm -rf $(DATA)/arxiv/; fi
	if [ -d $(DATA)/celegans/ ]; then rm -rf $(DATA)/celegans/; fi