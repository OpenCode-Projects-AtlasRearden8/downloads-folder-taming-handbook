# Convenience targets for the handbook.
# The actual logic lives in build.py and tests/test_build.py.

.PHONY: build clean test check

build:
	python3 build.py

test:
	python3 -m unittest discover -s tests -v

clean:
	rm -rf site

check: build test
	@echo "build + tests: OK"
