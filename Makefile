# Exit upon error
.SHELLFLAGS = -e
JDEX = ~/jdex

build: install
	.venv/bin/jdh build-index

install: jdex_dir install_python install_npm style

jdex_dir:
	mkdir -p ${JDEX}

upgrade:
	prek autoupdate
	npm update
	uv lock --upgrade

clean:
	rm -rf node_modules .venv ${JDEX}

install_python:
	uv sync

install_npm: node_modules/tailwindcss

node_modules/tailwindcss: package.json
	npm install .

style: jdex.css

jdex.css: tailwind-input.css src/jd_helper/templates/*.html
	node_modules/.bin/tailwindcss -i tailwind-input.css -o jdex.css
	cp jdex.css ${JDEX}
