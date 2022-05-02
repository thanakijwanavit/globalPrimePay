.ONESHELL:
SHELL := /bin/bash
SRC = $(wildcard ./*.ipynb)

build: 
	nbdev_build_lib
	nbdev_build_docs --mk_readme true
	nbdev_clean_nbs
test: build
	cp layer/requirements.txt app/requirements.txt
	sam build
	sam local invoke -e testData/Get.json Get
	sam local invoke -e testData/RefreshEcommerce.json RefreshEcommerce
	rm app/requirements.txt
	touch app/requirements.txt
deploy: test
	sam build
	sam deploy --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --debug --parameter-overrides \
        "BRANCH=dev-manual" 