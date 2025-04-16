# Copyright 2020-2025 Sine Nomine Associates
#
# This makefile is a optional tox front-end.
# You can run tox directly without this makefile if you
# prefer. For example:
#
#    $ pipx tox
#    $ tox list
#    $ tox -e <testenv> -- <pytest_options>
#

TOX=tox
TESTENV=latest
PYTEST_FLAGS=

.PHONY: help
help:
	@echo "usage: make <target> [options]"
	@echo ""
	@echo "targets:"
	@echo "  lint       run lint checks"
	@echo "  test       run tests"
	@echo "  docs       generate html docs"
	@echo "  preview    local preview html docs"
	@echo "  release    upload to pypi.org"
	@echo "  clean      remove generated files"
	@echo "  distclean  remove generated files and venvs"
	@echo ""
	@echo "options:"
	@echo "  TOX=<path>           tox path [default: .venv/bin/tox]"
	@echo "  TESTENV=<env>        tox testenv [default: latest]"
	@echo "  PYTEST_FLAGS=<flags> pytest options [default: (none)]"

.PHONY: lint
lint:
	$(TOX) -e lint

.PHONY: test
test: lint
	$(TOX) -e $(TESTENV) -- $(PYTEST_FLAGS)

.PHONY: docs
docs:
	$(TOX) -e docs

.PHONY: preview
preview: docs
	xdg-open docs/build/html/index.html

.PHONY: release upload
release upload:
	$(TOX) -e release

.PHONY: clean
clean:
	rm -rf .pytest_cache src/*/__pycache__ tests/__pycache__
	rm -rf build dist
	rm -rf .eggs *.egg-info src/*.egg-info
	rm -rf docs/build

.PHONY: reallyclean distclean
reallyclean distclean: clean
	rm -rf .config .tox
