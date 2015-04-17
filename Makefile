bootstrap: env

env: requirements.txt
	mkdir -p log
	virtualenv $@ 2>&1 > log/virtualenv.txt
	$@/bin/pip install -r $< 2>&1 > log/pip.txt

test: env
	PYTHONPATH=$</lib/python2.7/site-packages $</bin/nosetests --rednose



.PHONY: test
