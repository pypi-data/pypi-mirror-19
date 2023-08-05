.. ViewModels documentation master README file.

==========
viewModels
==========

Uses_
-----

ViewModels are wrappers for the data 'model', that include details of the data
useful in generating views.  An ORM (https://en.wikipedia.org/wiki/Object-relational_mapping).
The current implementation is with mongoDB for
the bottle framework. Generally the concept is to allow information
and flexibly independent of the constraints of the underlying db.  This provides
for the model and also supports the view code, so simplifies both model and view
code.

- `Interface to provide access to database and abstraction`_.
- `Repository for all information relating to data: schema and beyond`_.
- `Increasing range of types available to applications`_.

Background_
-----------

- `History`_.
- `Data tables/collections and data views`_.

Instructions_
-------------
- `Simple Example`_.
- `Describing a table/collection with ViewFields`_.
- `Using 'ViewField' derived classes`_.
- `Building HTML forms`_.
- `Updating from HTML forms`_.

`How it works`_.
----------------
- `The rows Structure`_.

_`Uses`
-------


Interface to provide access to database and abstraction
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

To access a collection in a simply Mongo through pymongo could not
be much simpler. Similarly with other
However this does not provide:
- abstraction between code and database
- types beyond those covered in the BSON type set
- joins, and joins with 'lazy' execution
- a record of schema in use
- support for a web maintenance interface to the database
- web interface supports security and templates for full application

All these advantages are provided by using ViewModel.  However there are times
when none of these justifies an additional layer.  The more complex the
collection, the greater the amount of code, generally the greater the value
of using ViewObject

Abstraction between code and database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Databases migrate.  The Salt database started with direct SQL, then
SQLAlchemy, then mongodb.  Abstraction assists with migrations.
The current Salt system uses Mongo and directly using the pymongo interface
is can be perfect for simple access.  A rewrite would be needed to change
the db but the code is so small it is not a large barrier for small simple
cases. But more complex cases are another matter!

Repository for *all* information relating to data: schema and beyond
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A single repository for all information about data.  Information on both storage
as well as information used for display, all in one place.

Data descriptions can be simple tables/collections or views which comprise multiple
tables which are effectively joined.

The data description provided by viewmodel library, can include extended types
described at a layer of abstraction separate from the storage specification,
allowing the application layer free of the mechanics.

ViewModel was first created for SQL based applications, but then evolved to also
work with NoSQL mongoDB applications.

NoSql collections (or tables) can effectively be irregular with different
fields present potentially in every entry.  While with SQL,just examining a
row can give a reasonable view of that schema, but this can be less clear
from NoSql.  Even with SQL, the schema recorded is restricted to what the database
engine requires, and lacks richer descriptions of the data and rules not
implemented by the database, but a repository for a schema becomes even more
essential with NoSQL.

Increasing range of types available to applications
+++++++++++++++++++++++++++++++++++++++++++++++++++

ViewModel provides mapping between the data in the database and the data
seen by the application. Far more descriptive types and move complex types
can be used by the application with the mapping between these types and
the underlying storage format handle by the ViewModel


_`Background`
-------------
- `History`_.
- `Data tables/collections and data views`_.

History
+++++++

The original Salt project development worked with SQL at a time when
the SQLAlchemy project was still in early stages. So Salt developed its own
layer to abstract to the database in 2007 around the same time as SQLAlchemy
was developed.  Both the salt 'DataModel' and SQLAlchemy libraries developed
specific advantages, but as a popular open sourced project, SQLAlchemy became
the more mature product.
In 2015 the Salt project chose to replace the internal 'DataModel' library
with the SQLAlchemy, due to wider use and greater development of the open
source project, but then found several key features of 'DataModel' were missing
from SQLAlchemy.
The solution was a new library 'ViewModel', which acted as an abstraction
layer between SQLAlchemy and the application.  The name 'ViewModel' came from
the fact that the main elements present in 'DataModel' that were missing
from SQLAlchemy were data extended data schema information that were also
useful in providing data description to views.

The next step brought the current 'ViewModel', by transforming that library to
become an interface between pymongo and the application.

Data tables/collections and data views
++++++++++++++++++++++++++++++++++++++

The ViewModel package focuses on preparing data for views.  How is the data
in a table/collection to be viewed?  For example,
consider a 'Products' table or collection, where products may be viewed:
- individually by product code,
- as a list of products by product group, or by brand
- as a list through a custom search

These become the views of the data from the database.  It is never relevant
to actually retrieve the entire table/collection for the products as if
processing the entire table, each document will be processed in sequence.
In contrast, there may be other table/collections with either a single or
small fixed number of rows/collections the entire table/collection may constitute
a view.

Further, product could have a join to a 'pack sizes' table/collection and
for some views these are also part of the view.

The main concept is that each table has a set of relevant views of the
table/collection for various uses.  The viewmodel specifies not just the
schema of the table/collection, but the actual views of the table/collection.


_`Instructions`
---------------
- `Simple Example`_.
- `Describing a table/collection with ViewFields`_.
- `Using 'ViewField' derived classes`_.
- `Building HTML forms`_.
- `Updating from HTML forms`_.

Simple example
++++++++++++++
This example is given in advance the instructions or details on how the
components of the example work.  The idea is: read the example to gain an
overview, then see more details to understand more and return to this
example.

The simple database
~~~~~~~~~~~~~~~~~~~
The consider a database with a table of students.  Rows or Documents have

- an id
- a name
- a course
- year number within course

Code to describe table find an entry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The code follows::

    from ViewModel import ViewModel, IdField, TxtField, IntField
    import pymongo

    database = pymongo.MongoClient(dbserver).get_database("example")

    class StudentView(ViewModel):
        viewName_ = "Students"
        #models_ = #<database>.Students
        id = IdField()
        name = TxtField()
        course = IntField()
        #  .... field definitions may  continue

    student = StudentView({},models = database.Students)
    # could have used 'models_' within class to avoid needing 'model' parameter
    # {} empty dictionary to ensure an empty view, not needed if the database
    # does not even exist yet, as with a new database, initial view will always
    # be an empty view

    if len(student) > 0:
        print("oh no, we already have data somehow!")

    students.insert_() #add an empty entry to our view

    with student:  #use with so changes written at end of 'with'
        student.name = 'Fred'

    #ok.... now we have a 'Student' table with one entry

Code to read and update our entry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A key concept is that while the class for the view describes a table, set of
tables or joined tables (or collections in Mongo speak), an instance of
a ViewModel is the set of data, or a window of the tables.
Instancing the view actually reads from the
data base in simplest cases, although in more complex cases the data may be read
from the database when accessed, the view instance logically includes all data
from a 'read' operation::

    #same class definition and imports as above

    student = StudentView({'name': 'Fred'},model = database.Students)
    # would save if we could have 'models_' in class definition!

    if not student.course:
        with student:
            student.course_year = 2
            student.course = 'Computing'

Multiple Entry Views
~~~~~~~~~~~~~~~~~~~~
So far our view has only one entry.  Instance of our view is a window viewing
part of the database.  This window, can be a single row/collection or a logical
group of entries(from rows/collections), and for small tables, may even be
the entire table/collection. The code that follows adds another entry, so the sample has
more than one entry, then works with a multi entry
view::

    StudentView.models_ = database.Students
    #modify class, add 'models_' as an attribute,
    #this saves specifying 'models_' each time instancing StudentView

    student = StudentView()
    #no dictionary, this gives an empty view (not multi entry yet)

    student.insert_()
    with student:  #adding a second student
        student.name = 'Jane'
        student.course = "Computing"
        student.course_year = 2

    #now our multi entry view for all year 2 Students
    students = StudentView({'course_year':2})

    for student in students:
        print(student.name)

Note how multi entry view instances can be treated as lists. In fact, single
entry views can also be treated as a list, however for convenience view
properties for single entry views also allow direct access as one entry. For
a single entry view 'student'::

    student.name == student[0].name


Example Summary
~~~~~~~~~~~~~~~
The example bypasses the power of ViewModels in order to a simple introduction.
A key concept is that classes describe a table ( or collection or set/join
of tables). An *instance* of a ViewModel is one set specific subset, a set of
data from a table (or set/join of multiple tables).

Describing a table/collection with ViewFields
+++++++++++++++++++++++++++++++++++++++++++++
When creating a class derived from a ViewModel, add class attributes
which are 'ViewFields' for each field in the table or collection.

The example ( 'Simple example'_. ) uses several types of view fields. However
each 'ViewField' can contain information well beyond the type of data.
An alternative name, a short and long description, formatting and other display
defaults,  value constraints and many other settings.

In the example, only the 'value' attribute of the "name" ViewField is accessed.
'student.name' does not access the ViewField, but instead returns "value"
attribute of the "name" ViewField.  To access the
actual ViewField (or IntField, TextField etc) and have access to these other
attributes use 'student["name"]'.  thus::

    student.name == student["name"].value


Using 'ViewField' derived classes
+++++++++++++++++++++++++++++++++

All 'fields' are sub-classed from ViewField, and represent individual data types.
Each field contains the following properties:

- name: set explicitly, or defaulting to the property name
- label: set explicitly but defaulting to the name
- hint: defaults to '' for display
- value: returns value when field is an attribute of a row object

'ViewModel' interface
+++++++++++++++++++++
The 'ViewModel' provides a base class defines a database table/collection, and each instance of
a ViewModel. Note all system properties and methods start of end with underscore to
avoid name collision with database field names.

ViewModel Interface Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- insert\_()
- labelsList\_()
- update\_()
- <iterate> for row in <ViewModel instance>
- <index>  <ViewModel instance>[row]

ViewModel Interface Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- viewName\_
- models\_
- dbModels\_

ViewModel details
~~~~~~~~~~~~~~~~~
'insert_()' method adds a empty new row (ViewRow instance) to the current ViewModel
instance. At
the next 'update_()', an actual database document/row will be created, provided
some values have been set in the new row.

'labelsList_()' returns a list of the labels from the rows of the current
ViewModel instance.

'update_()' is called automatically at end of a 'with <ViewModel instance>'
statement (python keyword 'with'), or can be called directly, to update the
actual database with values
changed by assignments through  '<ViewModel Instance>.<fieldname> = statements.

'viewName\_' is simply a title for the view for display purposes.

'models\_' is a list of the names of tables, or actual database tables objects
used by the view

'dbModels\_' is a dictionary of database table objects used by the view, with
the model names as keys.

Note: all 'ViewModel' instances with one row implements all of the ViewRow
interface in addition to the methods and properties discussed. 'ViewModel'
instances with more than one row will raise errors if the 'ViewRow' interface
as it is ambiguous which row/document to use.

'ViewRow': The Row Interface
++++++++++++++++++++++++++++
ViewRow objects and ViewModel objects both implement the 'ViewRow' interface.

Where a ViewModel contains one logical row, the operations can be performed
on the ViewModel, which also supports this interface for single row instances.

ViewRow Interface methods
~~~~~~~~~~~~~~~~~~~~~~~~~
- <iterate>:  for field in <ViewRow instance>
- loop\_(case=<case>): for field in a <ViewRow instance>
- <index>:  <ViewRow instance>[<field name>]
- <attribute> <ViewRow instance>.field_name

ViewRow Interface Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- fields\_
- view\_
- label\_
- idx\_

ViewRow details
~~~~~~~~~~~~~~~
'for <field> in <ViewRow instance>:' provides for using a 'for loop' to iterate
over the fields in a row of a viewfield.

Note that this iteration can be for building a view, and as such the iteration
allows for selecting which fields are included in the view.
When fields are declared
(see `'ViewField' interface`_), they can set a 'case' where they are applicable
for views.
For example, this can be in a view, on an edit panel, or the field is for
calculation purposes and part of the model, but not revealed in a view.

<ViewRow instance>[<field name>] or indexing, retrieves the instance of the
ViewField named.  For example::

    student['name'].value = 'Jane'
    print(student['jane'].value)


'fields\_' returns
A 'ViewRow' is a logical entry in a ViewModel.  Consider the example
( 'Simple example'_. ). The line of code::

    student.name = 'Fred'

Is using the ViewRow set attribute interface to set the 'value' of the 'name'
field within the 'row' created by the insert\_() method.

In this example, because the 'student' ViewModel has only one row, then.

This interface allows retrieving and setting data 'fields' or ViewField entries
by name as object attributes.  All internal attributes of ViewRow have either
a trailing underscore to avoid name collisions with field names of the database,
or a leading underscore to indicate that these attributes should not be accessed
externally of the ViewRow or ViewModel.

Provided database fields have no leading or trailing underscore, they will not
collide with the names of internal workings of these classes.


joins & data relationships
--------------------------
The term 'relational database' comes from the concept that data contained
in separate tables (or collections) is related.


Data Relationship types
+++++++++++++++++++++++
Many to one
~~~~~~~~~~~
These are classic 'dry'.  Several records (or rows or documents) in a table
will use the same information.  For example, and address with a city. Since
there are far more addresses than cities, when reading an address, obtaining all
the 'city' information (name, city code, state) from a separate city table will
mean that information for each city is not repeated for each address with the same
city.  From the perspective of the address, the relationship is 'one-to-one' because
for each address there is only one city.  The 'many-to-one' is that many addresses
may reference each city.

If our view is based on a single address, then retrieving the 'join' of the information
for the address together with the information for the city still leaves a single 'row'
in the resulting view.

In database design, to implement a 'many to one', each entry from the many table,
contains a key to the city table.  Read an address, the use the 'key to the city'
to read data from the city table. 


One To Many
~~~~~~~~~~~
>From a technical perspective, this is simply the same as 'Many to One', but viewed
from the opposite perspective. But there is devil in the detail, and having the 
opposite perspective has implications that can mean the correct implementation
is very different.  Looking at the previous cities and addresses, the 'one to many'
view from the city perspective is to consider all addresses with the city.

If our view is based on a single city, then retrieving the 'join' would result in rows for
each address.  So while the one-to-many is the many-to-one from the opposite perspective,
the view changes entirely and in nature depending on which perspective.

In database design, the cross reference key is still the 'key to the city' within the
address table. Read the city key (as 'our city key'). Then using the key field find all addresses with
their 'key to the city' value matching the key in 'our city key'.


Many To Choice
~~~~~~~~~~~~~~
This is a real world application of the 'Many to one' join, where the table of possible 'ones'
effective represents one of a finite set of choices which may be chosen from a 'drop down list box'.
ViewModel has a specific Field Type, the 'EnumForeignField'.  Note that to display choices for 
editing the entire table of choices is required.  There is no strict formulae as to 
when the number of choices or total data of the choices table is too large, but generally
the system must have the capacity to consider having the entire table in memory acceptable.


Many to Many
~~~~~~~~~~~~
Consider now database with not just addresses and cities, but also people.  Each person
might have a relationship to several addresses. But rather than this being a
'One to Many' relationship, like the Cities -> Addresses, where viewed from the other
perspective, Addresses->Cities, for each address there would be only one city, this 
time for each address there may be multiple people.

In database design, this usually represents more of a challenge. If we start with people, we cannot
look for addresses with a 'person key' field that matches since our person, since each address 
will need to match potentially several (or many) people. The matching person cannot be
stored as a single value in our table.  With SQL and even sometimes with NoSQL, the 
solution is to have a separate table of relationships.  If we read this table for all entries
matching our person we can find an entry for each relationship to an address for that person.
This solves the problem because we can have more relationships than we have either 
people or addresses, so one entry per table will not work without a special table that can
have an entry for each relationship.

NoSQL like Mongo provides another alternative, which is keeping a list of relationships inside
one (or even both) of the tables.  Since an entry in the table can be a list, we could keep
a list of addresses in the people table. Read a person and we have a list of addresses.
Read an address and we can read all people with our address in their address list. The
principle is still the same, but there is this implementation choice.

Relationship Specific Data
~~~~~~~~~~~~~~~~~~~~~~~~~~
In some cases, there can be data specific to a relationship. Consider the following people,
addresses and then relationships::

    People:  Bob, Tom, Alice
    Addresses: RedHouse, Office1, Office2, GreenHouse
    Relationships:
        Bob: RedHouse is 'home', Office1 is 'work'
        Alice: RedHouse is 'home' and 'office'
        Tom: GreenHouse is Home, RedHouse is 'work1' and Office2 'work2'

The relationships between the people can each have their own labels, just as 
the relationships between people can. In fact each relationship can have a 
label from each perspective.  Consider people relationships where Bob could be
'husband' to Alice, but the same relationship from the other perspective could
be 'wife'.

So for Bob we may have to have not only added 'RedHouse' and created a relationship,
we also have to manage a label for the relationship.



'ViewField' interface
+++++++++++++++++++++

Getting and Setting 'Row Member' values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To be added


Building HTML Forms
+++++++++++++++++++

To be added


Updating from HTML forms
++++++++++++++++++++++++

To be added

How it works
------------
The rows structure
++++++++++++++++++
The actual data is kept in a view list  called 'dbRows\_',
which reflects the actual data being held in the underlying
database.
For each row of the view, there is one entry in dbRows\_.

The list elements of 'dbRows\_'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
each entry is of type 'objdict' and the elements of the
objdict were originally the values of the fields in the
view, but a new layer has been added, so that 'objdict'
entries at the top level represent the data from a single
source.
from::

    [ {'name':'Jane','course':'computing'}]

    to 
    [ {'students': {'name':'Jane','course':'computing'}}]

The two tiered structure, keyed by the 'table/collection'
which is the data source, better provides for data from
multiple sources.

Data is not added directly to these rows, but through the 'viewmodel_row'
wrappers.  So if a viewmodel row has a view_field (say 'last_name')
which is not present in the row, setting last name would add
a new field to the appropriate ObjDict within the row, but also an 
an entry to an additional 'changes' copy of the row, which hold new values
not yet committed to the database.

The 'rows' and 'changes' are the bridges between what is in the
database files, and what is held in memory.


