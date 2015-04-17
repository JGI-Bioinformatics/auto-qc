test = PYTHONPATH=env/lib/python2.7/site-packages env/bin/nosetests --rednose

bootstrap: env

env: requirements.txt
	mkdir -p log
	virtualenv $@ 2>&1 > log/virtualenv.txt
	$@/bin/pip install -r $< 2>&1 > log/pip.txt

test: env
	$(test)

autotest:
	clear && $(test)
	fswatch -o ./auto_qc -o ./test | xargs -n 1 -I {} bash -c "clear && $(test)"

feature: env
	PYTHONPATH=$</lib/python2.7/site-packages $</bin/behave --stop

.PHONY: test feature autotest
