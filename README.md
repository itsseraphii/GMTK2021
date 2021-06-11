# GMTK 2021 Project
## Project setup
To set up the project, you must have `Python 3` or higher installed, as well as `pip` if it was not included in your install.

1. Install poetry
```cmd
py -m pip install poetry
```
2. Run poetry on the project
```cmd
py -m poetry install
```

## Adding dependencies
If you wish to add a dependency, be sure to add them using poetry so this updates the .tomnl and .lock file.
```cmd
py -m poetry add (module-name-here)
```