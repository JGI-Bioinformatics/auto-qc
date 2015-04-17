test    = PYTHONPATH=env/lib/python2.7/site-packages env/bin/nosetests --rednose
feature = PYTHONPATH=env/lib/python2.7/site-packages env/bin/behave --stop

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

autofeature:
	clear && $(feature)
	fswatch -o ./auto_qc -o ./test -o ./bin -o ./features \
		| xargs -n 1 -I {} bash -c "clear && $(feature)"

feature: env
	$(feature)

.PHONY: test feature autotest autofeature
