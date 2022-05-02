.ONESHELL:
.PHONY: build pypi dist 
SHELL := /bin/bash
SRC = $(wildcard ./*.ipynb)

build: 
	nbdev_build_lib
	nbdev_build_docs --mk_readme true
	nbdev_clean_nbs
    
pypi: dist
	twine upload --repository pypi dist/*

dist: build
	nbdev_bump_version
	python setup.py sdist bdist_wheel