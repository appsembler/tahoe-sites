help: #- Display this help menu
	@echo -e "Usage: make <target>\n"
	@echo "<target>:"
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*?#- .*$$}' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?#- "}; {printf "\033[36m  %-35s\033[0m %s\n", $$1, $$2}'

test.requirements: #- Install pip packages in the virtual environment directory with re-install
	pip install -e .
	pip install -r requirements/tests.txt --force-reinstall

test.requirements.fast: #- Install pip packages in the virtual environment directory without re-install
	pip install -e .
	pip install -r requirements/tests.txt

test: #- Run tests using tox
	tox -r

test.fast: #- Run tests using tox, and don't force reinstalling pip packages
	tox

migrations: #- Create database migrate files
	TAHOE_SITES_USE_ORGS_MODELS=False django-admin makemigrations --settings=test_settings
