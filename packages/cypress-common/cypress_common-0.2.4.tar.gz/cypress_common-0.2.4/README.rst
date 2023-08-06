Cypress Common Modules
======================

To use the common modules on you local machine:

1. Pull the latest code for the cypress\_common project

2. Go to the **cypress\_common** directory and run the command (for
   Ubuntu):

   ::

       sudo python setup.py install

3. Import the cypress\_common modules

   Ex) How to import the CypressCache from other projects:

   ::

       from cypress_common.cypress_cache import CypressCache

**Note: Everytime a change is made to this project, we need to run the
command in step 2) again.**
