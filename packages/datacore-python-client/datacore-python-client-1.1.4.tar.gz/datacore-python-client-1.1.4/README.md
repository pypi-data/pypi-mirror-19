# datacore-python-client
A thin client used to access datacore. Supported operations include
POST, GET, HEAD, with access to aggregations, and nearly the full
suite of all RESTful operations datacore accepts. (As new features roll
out for datacore, support will be added for ease). All transactions occur 
over https protocol using the supported API endpoints.


## Installation
##### PYPI (recommended):
> sudo pip3.5 install datacore-python-client

or

> sudo pip3.5 install git+git://github.com/Bodaclick/datacore-python-client.git
##### From source
Download the source package from https://github.com/Bodaclick/datacore-python-client,
and enter the project directory. 
> sudo python3.5 setup.py install


## Usage
Once installed, import the package in your code:
> import datacore


The main object within the package is the Access object:
> datacore_user = os.environ.get("DC_USER") 
> datacore_secret = os.environ.get("DC_SECRET")
> access = datacore.Access(datacore_user, datacore_secret)


All transactions happen through the Access object, which must first
be instantiated. This object only require the user and secret for 
login access. (Note: this module does not support generation of 
authentication "user" or "secret". Please contact EveryMundo to obtain
these credentials). Then, using the appropriate endpoint (again, please
contact EveryMundo if you have not been provided these), we can access
datacore by using MongoDB json queries passed into these lower-level
methods: Access.post(), Access.get(), Access.head(), 
Access.post_lines():

> data = access.get(endpoint, query=my_query, limit=1)

Access.get() supports aggregation queries as well:
> query = \[match_query, group_query, sort_conditions\]
> aggregated_data = Access.get(agg_endpoint, query=query, agg=True)

Access.post() is invoked using a simpler syntax:
> Access.post(bulk_post_endpoint, data_set)

or

> Access.post_lines(write_endpoint, data_set)

Post lines differs from post() by opening a new connection _for each_
document of data (row dictionary) in the data_set.

Please note the difference from the various datacore endpoints. Bulk
post urls are not the same endpoint as the post url (post takes 1 line
of data, and hence expects a dictionary, whereas bulk post takes many,
and expects a list -arraylist- of dictionaries). Aggregation expects
and aggregation pipeline query (a list of dictionary queries), and
the regular read endpoint expects a dictionary query. (For more 
information on the proper query structure, see the MongoDB json query
language syntax on the MongoDB documentation). It is the responsibility
of the user to manage the endpoints and query structures themselves.



## History
####Version 1.1.4
Fixed a bug where the class method Endpoints.endpoints_from_definition()
returned None instead of a new Endpoints instance. Endpoints can have
their attributes (read, write, bulk, agg, version) directly using 
dictionary syntax, both able to be changed and updating the attribute.
However, attempting to add an attribute using dictionary syntax will
cause a DatacoreTypeError to be raised.

Added DatacoreTypeError to exceptions.py.
####Version 1.1.0a0
Created a new class Endpoints to replace the old dictionary implementation.
A distinct class with a strict constructor was chosen over namedtuple() 
for backwards compatibility and for greater ease of understanding the
object structure. 
####Version 1.0.6
Access.endpoints_from_definition() now return a named tuple instead of
a dictionary. This is for easier calls in classes that extend Access.
####Version 1.0.5
Bugfix for exceptions not showing repr when being raised. Added a method 
that returns the number of entries for a given query.
####Version 1.0.4
Bugfix for attemping to bulk post a single document. More exception catch
cases for uncommon bugs, especially those that occur in post() due to
bad/ unexpected payload formatting.
####Version 1.0.0
First major full release (in development). Exception module separated from
restlike.py. Exceptions caught from another exception class now inherit
their original tracebacks. yield_get removed for lack of consistant 
functionality. endpoints_from_definition() implemented (developed originally
in subclasses that inherited from Access objects). Raises DatacoreException
if there is an exception raised during data chunking for post. 
DatacoreException now has user-defined __repr\_\_ and __str\_\_ methods.
####Version 0.2.18
Allows for the objects Access and DatacoreException to be accessed from an 
'import all' statement. Updated tests.
####Version 0.2.17
Minor changes to allow for maximum compatibility with datacore interface
(addressing a get() bug for aggregations.)
####Version 0.2.16
Allows for the DatacoreException class to be exposed from the top-level
package directory.
####Version 0.2.15
Support for mypy/ typing modules now incorporated. New init params!
This is actually a MAJOR version update as this means that for the
time being, existing code will not be available for Python 2.7 users.
(This is not a promise of never, but solidifies this package's 
current functionality).
####Version 0.2.14
Fixed a bug where ConnectionError sourced DatacoreExceptions do not
raise with the correct error text and args.
####Version 0.2.13
Exception handling update. Cleaner and more verbose exception handling.
Each request has had its maximum timeout extended from 120 seconds to
180 seconds to allow datacore time to respond with a failure mesasge.
####Version 0.2.12
Post and subpost had a bad error reporting, it would crash trying to
report post errors with typeError. Fixed.
####Version 0.2.11
Sub post gutted and replaced (largely) by some of the guts of post(). 
This should lead to less buggy implementation and better exception
handling with clearer respones.
####Version 0.2.10
Normal calls (within Access.post()) to Access._sub_post() did not pass
the url parameter, leading to crashes for large posts (posts rejected
for upload to datacore under status code 413). This issue was resolved.
####Version 0.2.9
Removal of one of the two assertions that produce a bug when met with
an "emtpy" data set (scenario that should be expected).
####Version 0.2.8
Now also tells you the type of what you were trying to post in the
aforementioned assertionerror message.
####Version 0.2.7
Added type assertion into post (the bulk post method) for easier flat
out refusal of improperly formatted data packages.
####Version 0.2.6
Fixed a bug where empty queries appended a newline character, confusing
the requests library.
####Version 0.2.5
Major bugfix for the post method. x4 duplicates were being uploaded.
####Version 0.2.4
Reverting to original max_page algorithm in Access.get() to prevent 
never-ending pagination bug in certain queries.
####Versions 0.0.1 through 0.2.3:
Access class, methods post, get, head, post_lines, and their helpers;
Exception cases have been written.


## Credits
Author: Vincent Medina
Email: vincent@everymundo.com
Company: EveryMundo
