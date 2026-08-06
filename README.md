# jd-helper

Introduction

Usage, etc.


## Development on this project itself

See [nens-meta's documentation](https://nens-meta.readthedocs.io) for an explanation of the config files like `.editorconfig` and tools like `pre-commit` and `uv`.

The standard commands apply:

    uv sync        # Yes, add 'uv.lock' to git afterwards!
    uv run pytest
    uv run python  # You can also activate the virtualenv in .venv
    pre-commit run --all  # You can also do 'pre-commit install'
    uv add some-dependency

`uv` replaces pip/venv/requirement.txt/pip-tools. `pre-commit` does basic formatting.

The tests and pre-commit are also run automatically [on "github actions"](https://github.com/nens/jd-helper/actions) for "main" and for pull requests. So don't just make a branch, but turn it into a pull request right away. On your pull request page, you also automatically get the feedback from the automated tests.

If you need a new dependency (like `requests`), add it in
`pyproject.toml` in `dependencies`:

    $ uv add requests


## Steps to do after generating with cookiecutter

- Add a new project on <https://github.com/nens/> with the same name.  Think
  about the visibility to ("public" / "private") and do not generate a
  license or readme.

  Note: "public" means "don't put customer data or sample data with real
  persons' addresses on github"!

- Push your project to github (note: the current instructions on github only add the README, but we want to add all files):

      git init
      git add -A
      git commit -m "Generated with cookiecutter"
      git branch -M main
      git remote add origin https://github.com/nens/jd-helper.git
      # git remote add origin git@github.com:nens/jd-helper.git  # If you use ssh
      git push -u origin main

- Go to
  https://github.com/nens/jd-helper/settings/access
  and add the teams with write access (you might have to ask someone with
  admin rights (like Reinout) to do it).

- Update this readme.

- Remove this section as you've done it all :-)

- Look at the `climatescan` project for docker-compose examples.
