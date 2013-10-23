export PYTHONPATH
PYTHONPATH = $(HOME)/src/bin
FILT=201310
ALL=$(wildcard /osha/radio/in/i.d.hb.$(FILT)*.0?.*)
a: $(ALL:%=tmp/%)
#ARGS += --nalichni-opisi='/zapisi/op/*/op/*'

ARGS +=	--cron-earlier-minutes=9
ARGS +=	--cron-later-minutes=9
ARGS +=	--cron-later-percent=50
tmp/%:
	@mkdir -p tmp/plan
	-cd tmp; ../radioschedule.py --ienc=utf8 --daily=$* --today-daily --cron=rr --save-text --save-plan=plan/p $(ARGS)

	mkdir -p $@

mn:
	$(PY) radioizv.py rm.izv.yaml  --save
n:
	#echo $$PYTHONPATH
	#python -c 'import sys; print sys.path'
	python3 svd_util/yamls/usability.py rm.izv.yaml
	#python3 svd_util/yamls/usability.py bbb

# vim:ts=4:sw=4:noexpandtab
