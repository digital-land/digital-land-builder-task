
.PHONY: \
	compile \
	init \
	run-task \
	test \
	test-unit \
	test-acceptance

compile ::
	# Don't build requirements.txt with piptools as we need to get digital-land from GH
	python -m piptools compile --output-file=requirements/requirements.txt requirements/requirements.in
	python -m piptools compile --output-file=requirements/test-requirements.txt requirements/test-requirements.in

init ::
	bats -v || sudo apt install bats -y
	pip install --upgrade pip
	pip install -r requirements/test-requirements.txt
	pip install -r requirements/requirements.txt

run-task : 
	./task/run.sh;

test: test-acceptance

lint:
	@

test-unit:
	python -m pytest tests/unit

test-acceptance:
	# run bats test of the script
	bats tests/acceptance/test_run.bats

ifeq ($(VAR_DIR),)
VAR_DIR=var/
endif

ifeq ($(CACHE_DIR),)
CACHE_DIR=$(VAR_DIR)cache/
endif

SOURCE_URL=https://raw.githubusercontent.com/digital-land

ifeq ($(DATASTORE_URL),)
DATASTORE_URL=https://files.planning.data.gov.uk/
endif

specification::
	@mkdir -p specification/
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/attribution.csv' > specification/attribution.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/licence.csv' > specification/licence.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/typology.csv' > specification/typology.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/theme.csv' > specification/theme.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/collection.csv' > specification/collection.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/dataset.csv' > specification/dataset.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/dataset-field.csv' > specification/dataset-field.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/field.csv' > specification/field.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/datatype.csv' > specification/datatype.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/prefix.csv' > specification/prefix.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/provision-rule.csv' > specification/provision-rule.csv
	# deprecated ..
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/pipeline.csv' > specification/pipeline.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/dataset-schema.csv' > specification/dataset-schema.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/schema.csv' > specification/schema.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/schema-field.csv' > specification/schema-field.csv
	# additional
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/issue-type.csv' > specification/issue-type.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/severity.csv' > specification/severity.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/cohort.csv' > specification/cohort.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/project.csv' > specification/project.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/project-organisation.csv' > specification/project-organisation.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/include-exclude.csv' > specification/include-exclude.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/role.csv' > specification/role.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/role-organisation.csv' > specification/role-organisation.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/role-organisation-rule.csv' > specification/role-organisation-rule.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/specification.csv' > specification/specification.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/specification-status.csv' > specification/specification-status.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/project-status.csv' > specification/project-status.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/provision.csv' > specification/provision.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/provision-rule.csv' > specification/provision-rule.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/provision-reason.csv' > specification/provision-reason.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/fund.csv' > specification/fund.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/award.csv' > specification/award.csv
	curl -qfsL '$(SOURCE_URL)/specification/main/specification/quality.csv' > specification/quality.csv

init::	specification
init:: $(CACHE_DIR)organisation.csv

# local copy of organsiation datapackage
$(CACHE_DIR)organisation.csv:
	@mkdir -p $(CACHE_DIR)
ifneq ($(COLLECTION_DATASET_BUCKET_NAME),)
	aws s3 cp s3://$(COLLECTION_DATASET_BUCKET_NAME)/organisation-collection/dataset/organisation.csv $(CACHE_DIR)organisation.csv
else
	curl -qfs "$(DATASTORE_URL)organisation-collection/dataset/organisation.csv" > $(CACHE_DIR)organisation.csv
endif


clean::
	rm -rf ./var

clobber::
	rm -rf var/collection
	rm -rf var/pipeline
	rm -rf dataset/
	rm -rf data/
	rm -rf performance/

clobber-performance::
	rm -rf $(DB_PERF)