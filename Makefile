check:
	@PYTHONPATH=`pwd` py.test tests
clean:
	@find . -type d -name "__pycache__" | xargs -I@ rm -rf @
	@find . -type f -name "*.pyc" | xargs -I@ rm -rf @

