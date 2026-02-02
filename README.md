# python-docker-template
Template for starting a python + docker project from scratch. Provides base boilerplate code for building docker images based on pypi+conda environment via pixi but slimmed down.

All code should follow `src` folder convention.

# Contents

This template repo provides with the following boilerplate files:

- An example package with under [src/example_pacakge](src/example_package)
- A [pyproject.toml](pyproject.toml) file
- An example [Dockerfile](Dockerfile)
- Three Github Actions Workflows for CD under [.github/workflows](.github/workflows)
- [This README file](README.md)
- A basic [.gitignore](.gitignore) file for python development

# Usage post-forking

After a fork, several files should be modified before doing any actual work. They're simple placeholder sustituions and renaming, though. The actual process may be as follow:

1. Rename example package directory to actual project name
2. Update `pyproject.toml` file:
   1. Basic project info goes under `[project]`
   2. Conda deps go under `[tool.pixi.dependencies]`
   3. PyPi deps go under `[tool.pixi.pypi-dependencies]`
3. Alter both GitHub workflow files `main.yml` and `develop.yml` where the commented section is and do the following:
   1. Uncomment that section
   2. Change target docket image name. Specfically at the line containing something like `tags: ${{ secrets.REGISTRY_LOGIN_SERVER }}/python-docker-template`. Leave the actual image tag (either `main` or `dev`) as is.
4. (Optional) Alter `Dockerfile` arguments `TARGET_ENV_NAME`,  `DOCKER_USER_NAME` and `DOCKER_USER_GROUP` to heart's content.

