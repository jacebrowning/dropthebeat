PROJECT := DropTheBeat
PACKAGE := dtb
SOURCES := Makefile setup.py README.md

CACHE := .cache
VIRTUALENV := env
DEPENDS := $(VIRTUALENV)/.depends
EGG_INFO := $(subst -,_,$(PROJECT)).egg-info

ifeq ($(OS),Windows_NT)
	VERSION := C:\\Python33\\python.exe
	BIN := $(VIRTUALENV)/Scripts
	EXE := .exe
	OPEN := cmd /c start
	# https://bugs.launchpad.net/virtualenv/+bug/449537
	export TCL_LIBRARY=C:\\Python33\\tcl\\tcl8.5
else
	VERSION := python3
	BIN := $(VIRTUALENV)/bin
	OPEN := open
endif
MAN := man
SHARE := share

PYTHON := $(BIN)/python$(EXE)
PIP := $(BIN)/pip$(EXE)
RST2HTML := $(BIN)/rst2html.py
PDOC := $(BIN)/pdoc
PEP8 := $(BIN)/pep8$(EXE)
PYLINT := $(BIN)/pylint$(EXE)
NOSE := $(BIN)/nosetests$(EXE)

# Installation ###############################################################

.PHONY: all
all: develop

.PHONY: develop
develop: .env $(EGG_INFO)
$(EGG_INFO): $(SOURCES)
	$(PYTHON) setup.py develop
	touch $(EGG_INFO)  # flag to indicate package is installed

.PHONY: .env
.env: $(PYTHON)
$(PYTHON):
	virtualenv --python $(VERSION) $(VIRTUALENV)

.PHONY: depends
depends: .env $(DEPENDS) $(SOURCES)
$(DEPENDS):
	$(PIP) install docutils pdoc pep8 nose coverage wheel --download-cache=$(CACHE)
	$(MAKE) .pylint
	touch $(DEPENDS)  # flag to indicate dependencies are installed

# issue: pylint is not currently installing on Windows from PyPI
# tracker: https://bitbucket.org/logilab/pylint/issue/51
# workaround: install from the source repositories on Windows/Cygwin
.PHONY: .pylint
ifeq ($(shell uname),$(filter $(shell uname),Windows CYGWIN_NT-6.1 CYGWIN_NT-6.1-WOW64))
.pylint: .env
	$(PIP) install https://bitbucket.org/moben/logilab-common/get/cb9cb5b8fff228b9a4244e4a6d9b2464a7b6148f.zip --download-cache=$(CACHE)
	$(PIP) install https://bitbucket.org/logilab/pylint/get/8200a32b14597c24f0f4706417bf30aec1e25386.zip --download-cache=$(CACHE)
else
.pylint: .env
	$(PIP) install pylint --download-cache=$(CACHE)
endif

# Documentation ##############################################################

.PHONY: doc
doc: depends
	pandoc -f markdown_github -t rst -o README.rst README.md
	pandoc -f markdown_github -t html -o docs/README-github.html README.md
	$(PYTHON) $(RST2HTML) README.rst docs/README-pypi.html
	$(PYTHON) $(PDOC) --html --overwrite $(PACKAGE) --html-dir apidocs

.PHONY: read
read: doc
	$(OPEN) apidocs/$(PACKAGE)/index.html
	$(OPEN) docs/README-pypi.html
	$(OPEN) docs/README-github.html

# Static Analysis ############################################################

.PHONY: pep8
pep8: depends
	$(PEP8) $(PACKAGE) --ignore=E501 

.PHONY: pylint
pylint: depends
	$(PYLINT) $(PACKAGE) --reports no \
	                     --msg-template="{msg_id}:{line:3d},{column}:{msg}" \
	                     --max-line-length=79 \
	                     --disable=I0011,W0142,W0511,R0801

.PHONY: check
check: depends
	$(MAKE) doc
	$(MAKE) pep8
	$(MAKE) pylint

# Testing ####################################################################

.PHONY: test
test: develop depends
	$(NOSE)

.PHONY: tests
tests: develop depends
	TEST_INTEGRATION=1 $(NOSE) --verbose --stop --cover-package=$(PACKAGE).cli

# Cleanup ####################################################################

.PHONY: .clean-env
.clean-env:
	rm -rf $(VIRTUALENV)

.PHONY: .clean-dist
.clean-dist:
	rm -rf dist build *.egg-info 

.PHONY: clean
clean: .clean-env .clean-dist
	rm -rf */*.pyc */*/*.pyc */*/*/*.pyc */*/*/*/*.pyc
	rm -rf */__pycache__ */*/__pycache__ */*/*/__pycache__ */*/*/*/__pycache__
	rm -rf apidocs docs/README.html .coverage README.rst

.PHONY: clean-all
clean-all: clean
	rm -rf $(CACHE)

# Release ####################################################################

.PHONY: dist
dist: develop depends doc
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel

.PHONY: upload
upload: develop depends doc
	$(PYTHON) setup.py register sdist upload
	$(PYTHON) setup.py bdist_wheel upload


# Execution ##################################################################

.PHONY: gui
gui:
	$(BIN)/DropTheBeat$(EXE)
