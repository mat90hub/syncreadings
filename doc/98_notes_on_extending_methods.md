# Extending methods

When building a class as a descendant of an existing class (or widget), one will be facing the topic of extending existing method to add the new features introduced.

The recommended way to do it is as below:

- searching the new features in the keys of ``kwargs`` and retrieve them with ``pop`` method. This allow to be sure, the initialisation with this parameters won't be done twice.
- initialize the rest of the parameters at the end with the method ``super().__init__`` which is launching the initialisation of the ancestor
- perform the other action

This is the good method to extend ``__init__`` or ``configure``

One example.

```python

class EntryWithModel(tk.Entry):
    """Entry widget with a model."""
    def __init__(self, container, **kwargs):
        # recover all particular new parameters
        # from kwargs (avoid mixing)
        if 'model' in kwargs:
            self.MODEL_TEXT = kwargs.pop('model')
        else:
            # the right place for the defaut value
            self.MODEL_TEXT = " sin(x)  "
  
	# ... only some initialisations shown here ...
        if 'min' in kwargs:
            self.MIN = kwargs.pop('min')

	# the standard parameters, that may be absent
        if 'width' not in kwargs:
            self.WIDTH = len(self.MODEL_TEXT) + 2
            self.configure(width=self.WIDTH)

        # initialize the remaining parameters
        super().__init__(container, **kwargs)
  
        # other initializations
        self.IS_EMPTY = True
        self.FG_COLOR = self.cget("foreground")
        self.BG_COLOR = self.cget("background")

```

My practice has been also to capture those parameters in internal variable of the object with capatical letters.

For methods like ``cget``, one don't need to do this, since this method is supposed to get only one parameter.
