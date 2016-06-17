feature = $(path) behave --stop --no-skipped $(FLAGS)

#################################################
#
# Documentation
#
#################################################

doc: $(find man/*.mkd) Gemfile.lock
	bundle exec ronn ./man/auto-qc.1.mkd

#################################################
#
# Unit tests
#
#################################################

autofeature:
	clear && $(feature)
	fswatch -o ./auto_qc -o ./test -o ./bin -o ./features \
		| xargs -n 1 -I {} bash -c "clear && $(feature)"

feature:
	@$(feature)

autotest:
	@clear && $(test) || true
	@fswatch \
		--exclude 'pyc' \
		--one-per-batch	./auto_qc \
		--one-per-batch ./test \
		| xargs -n 1 -I {} bash -c "$(autotest)"

test:
	@$(test)

test    = clear && tox

#################################################
#
# Bootstrap project requirements for development
#
#################################################

bootstrap: Gemfile.lock .tox

.tox: requirements.txt
	tox --notest
	@touch $@

Gemfile.lock: Gemfile
	mkdir -p log
	bundle install --path vendor/ruby 2>&1 > log/gem.txt

.PHONY: bootstrap test feature autotest autofeature doc
