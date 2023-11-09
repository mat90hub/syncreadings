Progressive construction of a series of time Entries Widgets.
=============================================================

.. héritage et POO: https://gayerie.dev/docs/python/python3/heritage.html

We will be using date-time entries and time-delta. Those are both
particular objects, that can be found in the `datetime` library.
The particularity is that we have a string representation of these
object and a content, which is different. So synergies can be 
between both.

We also wants to have a guidance before entering the date-time in
order to suggest the proper format of entry. For this we are 
introducing a widget ``EntryWithModel`` which is a descendant
from ``tk.Entry``. The other widget dedicated to date-time entry
and to time-delta, respectively ``EntryDatetime`` and 
``EntryTimedelta`` will be both descendants from ``EntryWithModel``.

The last widget is ``entryTimescale`` is no more a descendant, but
it compiles several of this widget into a single object. This
object has a start time, an ending time, a step for each ticks,
which is a time-delta.

As for other development, each file of this library contains a 
*main* part, which is a test bunch.


The widget EntryWithModel.
==========================

The class ``EntryWithModel`` define an ``Entry`` widget, for which
there is a model indicated in grey, when the entry space is empty.
Some additional parameters are then needed.

.. list-table:: New parameters for this widget.
    :widths: 25 25 50
    :header-rows: 1

    * - Parameters
      - Internal variable
      - What's for
    * - ``model``
      - ``MODEL_TEXT``
      - the model that will be shown in the background of the widget.
    * - ``model_color``
      - ``MODEL_COLOR``
      - the text color for the model, inherited from ``EntryWithModel``.

and in addition we have also another internal variable.

.. list-table:: Additional internal variables
    :widths: 25 50
    :header-rows: 0

    * - ``IS_EMPTY``
      - To mentioned when the entry is not filled by an actual entry
        (but it is filled by the ``MODEL_TEXT``).

This variable is important and I made it accessible to external via 
the definition of property .

.. list-table:: Additional properties
    :widths: 25 50
    :header-rows: 0

    * - ``is_empty``
      - Retrieve the status ``IS_EMPTY``


The class is also defining or redefining the following methods.

.. list-table:: The additional methods of EntryWithModel.
    :widths: 25 75
    :header-rows: 1
    
    * - Method
      - What it does
    * - ``configure``
      - add the configuration of ``model`` and
        ``model_color`` with an update of the widget
        if applicable.
    * - ``cget``
      - to obtain the status of ``model`` and ``model_color``.
    * - ``clear``
      - Erase all content a put the ``MODEL_TEXT`` 
    * - ``enter``
      - Force the entry of a value as the user would do.
    * - ``on_focus_in``
      - When entering the widget, erase the ``MODEL_TEXT``
    * - ``on_focus_out``
      - When loose focus, put ``MODEL_TEXT`` if no entry.

Here is the code.

.. literalinclude:: ../lib/entryWithModel.py
   :language: python3
   :lines: 4-83
   :caption: The class EntryWithModel.


The widget EntryTimedelta.
==========================

The class ``EntryTimedelta`` inherits from ``EntryWithModel``
since it proposes a model for writing a time-delta. But before
going further, I needed to define to other functions
``strftimedelta`` and ``strptimedelta`` for respectively
formatting and parsing a time delta on the model of the functions
``strftime`` and ``strptime`` from the library `datetime`.
The first function format a ``timedelta`` object into a string 
and the second do the reverse: it converts a string representing 
a time-delta into an actual ``timedelta`` object 

.. literalinclude:: ../lib/entryTimedelta.py
   :language: python3
   :lines: 7-28
   :caption: The function strptimedelta.

.. literalinclude:: ../lib/entryTimedelta.py
   :language: python3
   :lines: 30-48
   :caption: The function strftimedelta.

The definition of the class ``EntryTimedelta`` is then very
short, since it benefits from the inheritance.

.. literalinclude:: ../lib/entryTimedelta.py
   :language: python3
   :lines: 51-70
   :caption: The class EntryTimedelta.


The widget EntryDatetime.
=========================

The purpose of this widget is to remain simple and as direct as possible
for the entry, avoiding in particular to open calendars, as it is 
now quite common for such widgets. So it uses a model of date-time and 
it will convert a very the string entry to convert it to an actual 
date-time object. There is a bit more new parameters introduced for this 
widget.

.. list-table:: New parameters for this widget.
    :widths: 25 25 50
    :header-rows: 1

    * - Parameters
      - Internal variable
      - What's for
    * - ``model``
      - ``MODEL_TEXT``
      - the model that will be shown in the background of the widget.
    * - ``model_color``
      - ``MODEL_COLOR``
      - the text color for the model, inherited from ``EntryWithModel``.
    * - ``format``
      - ``DATE_FORMAT``
      - the format of the date to be used.
    * - ``err_bg_col``
      - ``ERR_BG_COL``
      - color of the widget background in case of error.
    * - ``err_fg_col``
      - ``ERR_FG_COL``
      - color of the widget foreground (text) in case of error.

There are two additional Internal variables.

.. list-table:: Addition internal variables
    :widths: 25 50
    :header-rows: 0

    * - ``IS_EMPTY``
      - Inherited from ``EntryWithModel``
    * - ``ENTRY_ERROR``
      - When the entry is not representing a correct date-time.


This widget is also declaring the following properties.

.. list-table:: Properties of this widget.
    :widths: 25 75
    :header-rows: 0

    * - ``format``
      - Format of the date.
    * - ``datetime``
      - Provide the content as a datetime object, when ``cget`` will
        give it as a string.
    * - ``entryError``
      - Boolean to report an entry error.
    * - ``isEmpyt``
      - Inherited from ``EntryWithModel``.
    
The following methods have been defined or redefined.

.. list-table:: The additional methods of EntryDatetime.
    :widths: 25 75
    :header-rows: 1
    
    * - Method
      - What it does
    * - ``model_match_format``
      - checking if model and format are matching, not used so far.
    * - ``update_format_with_model``
      - when we enter a model first, the format is here updated.
        (but no widget update)
    * - ``update_model_with_format``
      - when we enter a new format, the model is adapted.
        (but no widget update)
    * - ``configure``
      - allowing to change the new parameters (and the old ones).
    * - ``cget``
      - obtaining the value of the new parameters (and the old ones)
    * - ``clear``
      - call the ``clear`` method of ``EntryWithModel``
    * - ``on_focus_in``
      - When entering the widget, withdraw the model and put background
        the normal foreground color.
    * - ``on_focus_out``
      - if loss the focus and no entry, reput the model.
    * - ``key-press_handler``
      - an help for autocompletion, when we are in the widget.
    * - ``move_cursor_left``
      - to allow correction and moving in the text, despite assistance
        for autocompletion. (could be merged with preceding)
    * - ``move_cursor_right``
      - same remark as preceding.
    * - ``final_validation``
      - check that the input is correct when leaving the widget.
    * - ``leave_widget``
      - action triggered when leaving the widget.


Here is the complete code.

.. literalinclude:: ../lib/entryDatetime.py
   :language: python3
   :lines: 6-253
   :caption: The class EntryDatetime.


The widget entryTimescale.
==========================

This widget is defining a time scale. It has

* a starting date-time ;
* an ending date-time ;
* a step to define each ticks on the scale.

Additionally to these elements, which have all their own internal
parameters as we have seen before, this object will have additional
properties.

.. list-table:: Properties dedicated to this object
    :widths: 25 50
    :header-rows: 0

    * - ``start``
      - the start as a ``datetime`` object
    * - ``end``
      - the end as a ``datetime`` object
    * - ``step``
      - the step as a ``timedelta`` object
    * - ``duration``
      - the difference between start and end as a ``timedelta`` 
        object.
    * - ``ticks_number``
      - the number of ticks in the time scale.
    * - ``ticks_list``
      - all the ticks as a list of ``datetime`` objects.

  