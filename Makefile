test    = PYTHONPATH=vendor/python/lib/python2.7/site-packages vendor/python/bin/nosetests --rednose
feature = PYTHONPATH=vendor/python/lib/python2.7/site-packages vendor/python/bin/behave --stop

bootstrap: Gemfile.lock vendor/python

vendor/python: requirements.txt
	mkdir -p log
	virtualenv $@ 2>&1 > log/virtualenv.txt
	$@/bin/pip install -r $< 2>&1 > log/pip.txt

doc: $(find man/*.mkd) Gemfile.lock
	bundle exec ronn ./man/auto-qc.1.mkd

test: vendor/python
	$(test)

autotest:
	clear && $(test)
	fswatch -o ./auto_qc -o ./test | xargs -n 1 -I {} bash -c "clear && $(test)"

autofeature:
	clear && $(feature)
	fswatch -o ./auto_qc -o ./test -o ./bin -o ./features \
		| xargs -n 1 -I {} bash -c "clear && $(feature)"

feature: vendor/python
	$(feature)

Gemfile.lock: Gemfile
	mkdir -p log
	bundle install --path vendor/ruby 2>&1 > log/gem.txt

.PHONY: bootstrap test feature autotest autofeature doc