bump-upload:
	bumpversion --config-file .bumbversion.cfg patch
	git push --tags
	git push --all
	python setup.py sdist upload
