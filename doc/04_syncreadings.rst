The script `syncreadings.py`.
=============================

The file consists in the definition of the class ``application``, which is
instantiated into an object and launch at the end of the script. The class
constructor is calling a method ``create_menu_bar``. The rest of the
methods are the commands launched by this menu.

.. list-table:: 
    :widths: 25 25 50
    :header-rows: 1

    * - Menu command 
      - Appli method
      - Actions
    * - `Load File`
      - ``load_file``
      - Read the source file to display it.
    * - `Close File`
      - ``close_file``
      - Unload the source file and clean the screen.
    * - `Exit`
      - ``self.destroy()``
      - Close the application.
    * - `Sets analysis`
      - ``sets_analysis``
      - Give general information on the sets.
    * - `Format into table`
      - ``format_datasets``
      - Format the loaded sets into a synchronized table and display it.
    * - `Export to CSV`
      -  ``export_do_csv``
      - Write the table into a csv file.
    * - `Export to XLSS`
      - ``export_to_xlsx``
      - Write the table into a xlsx file (Excel).
    * - `About`
      - ``user_manual``
      - Display a short window presenting the application.
    * - `User manual`
      - ``menu_help``
      - Display a window giving user instructions.

The command ``load_file`` is reading the input file as a simple text file 
and displays it on the screen. It allows the user to have a view of this
input file and to avoid entering blindly a file, which would have no meaning
for our purpose.

The actual command that will start to workout the input file are either 
``sets_analysis`` of ``format_datasets``. This function have a double
check with ``if elif`` to check:

  1. an input file was selected

  2. it was read with the function ``read_measures``.

The function ``read_measures`` of the library ``transform_data_sets`` will
do the actual conversion of the text file into a dictionary, as we will see
below.


