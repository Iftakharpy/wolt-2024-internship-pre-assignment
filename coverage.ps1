param(
	[bool]$clean = $false
)

# Responsible for cleaning coverage files
function Clean {
	Remove-Item -Path .\htmlcov -Recurse -Force
	Remove-Item -Path .\*.coverage -Force
}

# Responsible for generating coverage report
function Generate {
	python3 -m coverage run -m pytest
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
