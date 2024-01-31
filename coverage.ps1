param(
	[bool]$clean = $false
)

function Clean {
	Remove-Item -Path .\htmlcov -Recurse -Force
	Remove-Item -Path .\*.coverage -Force
}

function Generate {
	# Run pytest
	python3 -m coverage run -m pytest
	# Generate coverage report
	python3 -m coverage html
}

if ($clean) {
	echo "Cleaning coverage files..."
	Clean
	echo "Done."
} else {
	echo "Generating coverage report..."
	Generate
	# Open coverage report
	start .\htmlcov\index.html
	echo "Done."
}
