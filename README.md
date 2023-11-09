# Syncrhonized measures readings a table.


The aim of the application from this directory is to reformat several sets of measures readings into a table of synchronized data.

A set of measure consists in a title, which corresponds to the calling of the measure, followed by a a list of couple made of a date-time and a value. The date-time are separated by constant time step all over one set.

Now the sets can have different starting date-time, different ending date-time and different time step between each measures. The aim is now to build a table in which the first column is made of date-time and the following columns are filled with the values of the different sets read at those date-time intervalle.

Example of data files are stored in the directory [dat](./dat/).

More explanation in the directory [build/html](./build/html/index.html).
