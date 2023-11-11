# Utiliser les thèmes avec ttk.

Les liens:
- [tkdoc](https://tkdocs.com/tutorial/styles.html).

- [readthedocs](https://ttkthemes.readthedocs.io/en/latest/index.html)

- [list of themes](https://wiki.tcl-lang.org/page/List+of+ttk+Themes)

Les thèmes disponibles sous giihub se télécharge en clonant simplement le dépôt, coomme par example ceci.

```shell
git clone https://github.com/TkinterEP/ttkthemes/
```
Souvent, on est pas sur la bonne page et il faut racourcir le chemin par arriver à la racine du dépôt pour ce clonage.


On peut voir les thèmes existants avec les instructions suivantes.

```python
from tkinter import ttk
s = ttk.Style()
print(s)
```

pour connaitre le thème actuel.

```python
s.theme_use()
```

