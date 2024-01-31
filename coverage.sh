#!/usr/bin/bash

# Responsible for cleaning up the coverage report
function cleanup {
	rm -rf .coverage ./htmlcov/
}

# Responsible for generating the coverage report
function generate() {
	python3 -m coverage run -m pytest
	python3 -m coverage html
}


# Check if the user wants to clean up or generate the report
if [ "$1" == "clean" ]; then
	echo "Cleaning up..."
	cleanup
	echo "Done."
else
	echo "Generating coverage report..."
	generate
	# Open the coverage report in the browser
	xdg-open ./htmlcov/index.html
	echo "Done."
fi
