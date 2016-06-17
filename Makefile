#################################################
#
# Documentation
#
#################################################

doc: man/auto-qc.1

man/%: man/%.mkd
	bundle exec ronn $<

#################################################
#
# Unit and Feature tests
#
#################################################

autofeature:
	@clear && $(feature) || true
	@fswatch \
		--exclude 'pyc' \
		--one-per-batch	./auto_qc \
		--one-per-batch ./feature \
		| xargs -n 1 -I {} bash -c "$(feature)"

feature:
	@$(feature)

autotest:
	@clear && $(test) || true
	@fswatch \
		--exclude 'pyc' \
		--one-per-batch	./auto_qc \
		--one-per-batch ./test \
		| xargs -n 1 -I {} bash -c "$(test)"

test:
	@$(test)

# Commands for running tests and features
feature = tox -e feature $(FLAGS)
test    = clear && tox -e unit

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
