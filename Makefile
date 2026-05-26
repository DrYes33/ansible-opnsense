PATH := $(CURDIR)/.venv/bin:$(PATH)

.PHONY: build test unit-test functional-test lint

build:
	bash scripts/build.sh

test:
	bash scripts/unit_test.sh

unit-test:
	bash scripts/unit_test.sh

functional-test:
	bash scripts/test.sh

lint:
	bash scripts/lint.sh
