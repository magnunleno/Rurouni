check:
	@PYTHONPATH=`pwd` py.test tests -x

check-all:
	@PYTHONPATH=`pwd` py.test tests

check-q:
	@PYTHONPATH=`pwd` py.test tests -q

check-v:
	@PYTHONPATH=`pwd` py.test tests -x -v

check-v-all:
	@PYTHONPATH=`pwd` py.test tests -v

check-pdb:
	@PYTHONPATH=`pwd` py.test tests -x --pdb

clean:
	@find . -type d -name "__pycache__" | xargs -I@ rm -rf @
	@find . -type f -name "*.pyc" | xargs -I@ rm -rf @

