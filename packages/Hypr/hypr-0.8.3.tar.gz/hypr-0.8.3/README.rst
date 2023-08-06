Hypr. |master-travis| |master-coveralls|
========================================

Build a secure and RESTful hypermedia API.


Hypr. is an open-source framework to empower you to build modern webservices
and let your projects embrace the hyperconnectivity era with no concession on
the security.

Driven by concepts such as KISS and DRY, getting started with Hypr. is a matter
of minutes. Scroll this page to discover some of the included features.


An example before going further
-------------------------------

::

  from hypr import Hypr
  from hypr.models import SQLiteModel
  from hypr.providers import CRUDProvider


  class User(SQLiteModel):
      """A simple user."""

      def __init__(self, name):
          self.name = name


  class UserProvider(CRUDProvider):
      """A CRUD provider for User."""

      __model__ = User


  app = Hypr()
  app.add_provider(UserProvider, '/users', '/users/<int:id>')

  if __name__ == '__main__':

      app.run()




Running this example will start a stand-alone development server listening on
port 5555. The created API lets you to query, create, update or delete User
objects.

If you want to give a try, execute the following commands :

Create a user::

  $ curl -XPOST http://127.0.0.1:5555/users -d '{"name": "dave"}'

List registered users::

  $ curl -XGET http://127.0.0.1:5555/users

Get a specific user::

  $ curl -XGET http://127.0.0.1:5555/users/1

Where 1 is the user's id.

Update a specific user::

  $ curl -XPUT http://127.0.0.1:5555/users/1 -d {"name": "hal"}

Delete a user::

  $ curl -XDELETE http://127.0.0.1:5555/users/1

This example is pretty useless but illustrates perfectly the simplicity and
philosophy behind Hypr.

To discover how to take advantage of all the features included in Hypr, check
out the project documentation. You also can contribute to the project on Github
by reporting bugs or submitting features you want to see to appear.


.. |master-coveralls| image:: https://coveralls.io/repos/github/project-hypr/hypr2/badge.svg?branch=master
   :target: https://coveralls.io/github/project-hypr/hypr2?branch=master

.. |master-travis| image:: https://travis-ci.org/project-hypr/hypr2.svg?branch=master
   :target: https://travis-ci.org/project-hypr/hypr2
