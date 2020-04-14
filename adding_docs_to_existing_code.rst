.. _adding_docs_to_the_project:

Adding Sphinx docs to Existing Repositories
===========================================

So, you need to add some docs for code that we've already written.
You've come to the right place!

There are two common "setup" scenarios:
    - :ref:`Project with no Sphinx docs<docs_from_scratch>`
    - :ref:`Project with existing Sphinx docs, but no docs from code<adding_apidocs>`

No mater where you start, there are some :ref:`common
enhancements<tweaking_conf_file>` to improve the generated output.

In a nutshell, we use `Sphinx`_ with documentation placed in the
``docs`` directory off the root of the project.

.. _docs_from_scratch:

Adding Sphinx to a project with no docs yet
-------------------------------------------

Make sure `Sphinx`_ is installed on your machine (it shouldn't be in
your project's virtual environment). From the top level project
directory, run::

    sphinx-apidoc -F -A "RelEng Team" -V "0.1" -o docs $python_module_name

If you happen to have an early stage project, without a python module
directory yet, GOOD FOR YOU!!! You'll just do the normal
``sphinx-quickstart``. Please keep the defaults, except for 'autodoc'
and 'viewcode' (say 'Y'/Yes to both)::

    sphinx-quickstart docs

No matter which way you add Sphinx, don't forget to add ``docs/_build``
to the project's ``.hgignore`` or ``.gitignore`` file.

.. _adding_apidocs:

Adding autodoc to a project already using Sphinx
------------------------------------------------

The following command should maintain you existing docs, while adding
the generated code documentation. From the top directory::

    sphinx-apidoc -o docs $python_module_name

This will produce a file ``modules.rst`` which you'll need to manually
add into your existing ``index.rst`` file.

.. _tweaking_conf_file:

Tweaking the conf.py file
-------------------------

After you've added generated documentation to your Sphinx project,
you'll also need to tweak the generated ``docs/conf.py`` file needs a
couple of edits to work properly.  Around line 21, add the following
lines::

    sys.path.insert(0, os.path.abspath('..'))
    import mock
    MOCK_MODULES = []
    for mod_name in MOCK_MODULES:
        sys.modules[mod_name] = mock.Mock()

The first line ensures the module under development is found. The
remaining lines are a handy framework for satisfying import requirements
for your module.

.. note::
    If you want to import the real code during document generation,
    you'll need to add it to the read-the-docs requirements file, if it
    isn't already in your project's requirements.txt file..

.. _Sphinx: http://www.sphinx-doc.org/
