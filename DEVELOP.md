# Some hint for developers

## Virtual environment with Poetry

The project is developed using the virtual environment Poetry and I'm using VSC as code editor on this project. To start this project with Poetry, you should have close the preceding session of VSC (no pending directory opened when you closed VSC), you do on the directory of this application and launch.

```shell
poetry shell
```

this will open a shell in this virtual environment. In it, you launch VSC by simply typing.

```shell
code .
```

The files of the virtual envrionement are stored under the directory `/.venv`.

The file `pyproject.toml` contains the information on the project such as its dependencies, the version of Python used.


## Working with Visual Studio Code

To work confortably with VSCode, I have the following addins:

| add-ins                     | Provider                | usage                                                                                                                                                                                                                             |
| --------------------------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Python                      | IntelliSense, Microsoft | For using Python                                                                                                                                                                                                                  |
| Python Environement Manager | Don Jayamanne           | Allow in particular to activate the Python of the virual<br />environament if it was not done at launch time.                                                                                                                     |
| reStructuredText            | LeXstudio Inc.          | Aide pour les fichiers RST utilisés par Sphinx et en<br />particulier pour prévisualiser. Mais il ne faut pas <br />installer l'add-in Esbonio qui fonctionne avec Rst Preview<br />qui sont alors incompatibles (à creuser) |


## Documentation with Sphinx

The project is documented using Sphinx which is on the the directory
`doc`. The `makefile` is under this directory. You can generate it
with this command launch from this directory.

```shell
make html
```

The documentation will generated unde the directory `doc/_build/html`.

