Flake8 Extension to enforce trailing commas.
============================================

Usage
-----

If you are using flake8 it's as easy as:

.. code:: shell

    pip install flake8-commas

Now you can avoid those annoying merge conflicts on dictionary and list diffs.

Errors
------

Different versions of python require commas in different places. Ignore the
errors for languages you don't use in your flake8 config:

+------+---------------------------------------+
| Code | message                               |
+======+=======================================+
| C812 | missing trailing comma                |
+------+---------------------------------------+
| C813 | missing trailing comma in Python 3    |
+------+---------------------------------------+
| C814 | missing trailing comma in Python 2    |
+------+---------------------------------------+
| C815 | missing trailing comma in Python 3.5+ |
+------+---------------------------------------+


0.3.1 (2017-01-18)
------------------

- Also parse unpacks with literals.
  (`Issue #30 <https://github.com/flake8-commas/flake8-commas/issue/30>`_)


0.3.0 (2017-01-16)
------------------

- If there is a comment after the last item, do not report an error.
  (`Issue #18 <https://github.com/flake8-commas/flake8-commas/issue/18>`_)
- If there is an empty, tuple, list, dict, or function, do not report an error.
  (`Issue #17 <https://github.com/flake8-commas/flake8-commas/issue/17>`_)
- Support PEP 3132 Python 3.5+ extended unpacking.
  (`Issue #26 <https://github.com/flake8-commas/flake8-commas/issue/26>`_)
- `*args` should not require a trailing comma.
  (`Issue #27 <https://github.com/flake8-commas/flake8-commas/issue/27>`_)


0.2.0 (2017-01-13)
------------------

- First version of flake8-commas with changelog
- Fix HTML readme render on PyPI.
- Support various parenth_form edge cases.
- Merge from flake8-trailing-commas


