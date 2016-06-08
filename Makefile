path := PATH=./vendor/python/bin


doc: $(find man/*.mkd) Gemfile.lock
	bundle exec ronn ./man/auto-qc.1.mkd

#################################################
#
# Unit tests
#
#################################################

test    = clear && $(path) nosetests --rednose
feature = clear && $(path) behave --stop --no-skipped $(FLAGS)

test: vendor/python
	@$(test)

autotest:
	@$(test) || true # Using true starts even on failure
	@fswatch -o ./auto_qc -o ./test | xargs -n 1 -I {} bash -c "$(test)"

feature: vendor/python
	@$(feature)

autofeature:
	clear && $(feature) || true # Using true starts even on failure
	fswatch -o ./auto_qc -o ./test -o ./bin -o ./features \
		| xargs -n 1 -I {} bash -c "clear && $(feature)"

#################################################
#
# Bootstrap project requirements for development
#
#################################################

bootstrap: Gemfile.lock vendor/python

Gemfile.lock: Gemfile
	mkdir -p log
	bundle install --path vendor/ruby 2>&1 > log/gem.txt

vendor/python: requirements.txt
	mkdir -p log
	virtualenv $@ 2>&1 > log/virtualenv.txt
	$@/bin/pip install -r $< 2>&1 > log/pip.txt

.PHONY: bootstrap test feature autotest autofeature doc
