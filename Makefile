REBAR := ./rebar
BSHADOW_VSN := "svn.`svn info | grep '^Revision' | awk '{print $$2}'`"

.PHONY: all deps doc test clean release start self

all:
	$(REBAR) skip_deps=true compile	

all_withdeps: deps version
	$(REBAR) compile

self:
	$(REBAR) compile skip-deps=true

deps:
	$(REBAR) get-deps
	
doc:
	$(REBAR) doc skip_deps=true

test:
	$(REBAR) eunit skip_deps=true

clean:
	$(REBAR) clean

dialyzer: all test
	dialyzer --src src/*.erl deps/*/src/*.erl

release: all
	$(REBAR) generate

version:
	@echo "-define(bshadow_vsn, \"${BSHADOW_VSN}\")." | tee include/vsn.hrl
	
install:
	$(INSTALL) -d ${DESTDIR}/usr/local/ ${DESTDIR}${exec_prefix}/bin
	cp -r rel/bshadow ${DESTDIR}/usr/local/
	$(INSTALL) betternow ${DESTDIR}${exec_prefix}/bin
	
start: all
	exec erl -pa ebin deps/*/ebin -boot start_sasl \
		-name "bshadow@127.0.0.1" \
		-config rel/files/app.config \
		-s bshadow \
		-mnesia dir "\"data/mnesia\"" 
		-env ERL_CRASH_DUMP "log/erlang_crash_$$.dump" \
		+K true \
		+P 65536
