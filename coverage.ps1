param(
	[switch]$clean
)

# Responsible for cleaning coverage files
function Clean {
	# Pytest coverage files
	Remove-Item -Recurse -Force -Path .\*.coverage, .pytest_cache
	
	# Coverage report files
	Remove-Item -Recurse -Force -Path .\htmlcov

	# Remove pycache files
	Get-ChildItem -Recurse $Path | Where{$_.Name -Match ".*pycache.*"} | Remove-Item -Force -Recurse
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
