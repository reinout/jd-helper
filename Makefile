# Exit upon error
.SHELLFLAGS = -e
JDEX = ~/jdex

build: install
	.venv/bin/jdh

install: jdex_dir install_python style

jdex_dir:
	mkdir -p ${JDEX}

upgrade:
	prek autoupdate
	uv lock --upgrade

clean:
	rm -rf node_modules .venv ${JDEX}

install_python:
	uv sync

style:
	cp jdex.css ${JDEX}
