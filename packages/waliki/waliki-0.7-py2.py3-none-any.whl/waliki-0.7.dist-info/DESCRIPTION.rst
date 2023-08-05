
**Waliki** is an extensible wiki app for Django with a Git backend.


.. attention:: It's in an early development stage. I'll appreciate your feedback and help.


.. image:: https://badge.fury.io/py/waliki.png
    :target: https://badge.fury.io/py/waliki

.. image:: https://travis-ci.org/mgaitan/waliki.png?branch=master
    :target: https://travis-ci.org/mgaitan/waliki

.. image:: https://coveralls.io/repos/mgaitan/waliki/badge.png?branch=master
    :target: https://coveralls.io/r/mgaitan/waliki?branch=master

.. image:: https://readthedocs.org/projects/waliki/badge/?version=latest
   :target: https://readthedocs.org/projects/waliki/?badge=latest
   :alt: Documentation Status

.. image:: https://pypip.in/wheel/waliki/badge.svg
    :target: https://pypi.python.org/pypi/waliki/
    :alt: Wheel Status

:home: https://github.com/mgaitan/waliki/
:demo: http://waliki.pythonanywhere.com
:documentation: http://waliki.rtfd.org
:twitter: `@Waliki_ <http://twitter.com/Waliki_>`_ // `@tin_nqn_ <http://twitter.com/tin_nqn_>`_
:group: https://groups.google.com/forum/#!forum/waliki-devs
:license: `BSD <https://github.com/mgaitan/waliki/blob/master/LICENSE>`_

At a glance, Waliki has these features:

* File based content storage.
* UI based on Bootstrap and CodeMirror
* Version control and concurrent edition for your content using `git <http://waliki.readthedocs.org/en/latest/git.html>`_
* An `extensible architecture <http://waliki.readthedocs.org/en/latest/write_a_plugin.html>`_ through plugins
* reStructuredText or Markdown support, configurable per page
  (and it's easy to add extensions)
* A very simple *per slug* `ACL system <http://waliki.readthedocs.org/en/latest/acl.html>`_
* A nice `attachments manager <http://waliki.readthedocs.org/en/latest/attachments.html>`_ (that respects the permissions over the page)
* Realtime `collaborative edition <http://waliki.readthedocs.org/en/latest/togetherjs.html>`_ via togetherJS
* Wiki content embeddable in any django template (as a "`dummy CMS <http://waliki.readthedocs.org/en/latest/boxes.html>`_")
* Few helpers to migrate content (particularly from MoinMoin, using moin2git_)
* It `works <https://travis-ci.org/mgaitan/waliki>`_ with Python 2.7, 3.4 or PyPy in Django 1.8, 1.9 (and 1.10, most probably)

It's easy to create a site powered by Waliki using the preconfigured project_ which is the same code that motorize the demo_.

Waliki was inspired in Github's wikis, but it tries to be a bit smarter than many others `git backed wiki engines`_ at handling changes: instead of a hard *"newer wins"* or *"page blocking"* approaches, Waliki uses git's merge facilities on each save. So, if there was another change during an edition and git can merge them automatically, it's done and the user is notified. If the merge fails, the last edition is still saved but the editor is reloaded asking the user to fix the conflict.

.. _project: https://github.com/mgaitan/waliki/tree/master/waliki_project
.. _demo: http://waliki.pythonanywhere.com
.. _git backed wiki engines: https://waliki.pythonanywhere.com/Git-powered-wiki-engines

Getting started
----------------

Install it with pip::

    $ pip install waliki[all]

Or the development version::

    $ pip install https://github.com/mgaitan/waliki/tarball/master


Add ``waliki`` and the optionals plugins to your INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'waliki',
        'waliki.git',           # optional but recommended
        'waliki.attachments',   # optional but recommended
        'waliki.pdf',           # optional
        'waliki.search',        # optional, additional configuration required
        'waliki.slides',        # optional
        'waliki.togetherjs',    # optional
        ...
    )

Include ``waliki.urls`` in your project's ``urls.py``. For example::

    urlpatterns = patterns('',
        ...
        url(r'^wiki/', include('waliki.urls')),
        ...
    )

Configure search in your projects ``settings.py``.  For example::

    HAYSTACK_CONNECTIONS = {
      'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'search_index'),
      },
    }

    HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

Sync your database::

    $ python manage.py migrate   # syncdb in django < 1.7



.. tip::

   Do you already have some content? Put it in your ``WALIKI_DATA_DIR`` (or set it to the actual path) and run::

        $ python manage.py sync_waliki

   Do you want everybody be able to edit your wiki? Set::

        WALIKI_ANONYMOUS_USER_PERMISSIONS = ('view_page', 'add_page', 'change_page')

   in your project's settings.



Contribute
----------

This project is looking for contributors. If you have a feature you'd like to see implemented or a bug you'd liked fixed, the best and fastest way to make that happen is to implement it and submit it back upstream for consideration. All contributions will be given thorough consideration.

Everyone interacting in the Waliki project's codebases, issue trackers and mailing lists is expected to follow the `PyPA Code of Conduct`_.


Why *Waliki* ?
----------------

**Waliki** is an `Aymara <http://en.wikipedia.org/wiki/Aymara_language>`_ word that means *all right*, *fine*.
It sounds a bit like *wiki*, has a meaningful sense and also plays with the idea of using a non-mainstream language [1]_ .

And last but most important, it's a humble tribute to the president `Evo Morales <http://en.wikipedia.org/wiki/Evo_Morales>`_ and the Bolivian people.


.. [1] *wiki* itself is a hawaiian word
.. _moin2git: https://github.com/mgaitan/moin2git
.. _`PyPA Code of Conduct`: https://www.pypa.io/en/latest/code-of-conduct/




Changelog
---------

0.6 (2016-12-19)
++++++++++++++++

- Fix compatibility with Django 1.9.x and Markup 2.x (thanks to `Oleg Girko`_ for the contribution)

.. _Oleg Girko: https://github.com/OlegGirko


0.6 (2015-10-25)
+++++++++++++++++

- Slides view use the cache. Fix `#81 <https://github.com/mgaitan/waliki/issues/81>`__
- Implemented an RSS feed listing lastest changes. It's part of `#32 <https://github.com/mgaitan/waliki/issues/32>`__
- Added a `configurable "sanitize" <http://waliki.readthedocs.org/en/latest/settings.html#confval-WALIKI_SANITIZE_FUNCTION>`_ function.
- Links to attachments doesn't relay on IDs by default (but it's backaward compatible).  `#96 <https://github.com/mgaitan/waliki/issues/32>`_
- Added an optional "`breadcrumb <http://waliki.readthedocs.org/en/latest/settings.html#confval-WALIKI_BREADCRUMBS>`_ " hierarchical links for pages. `#110 <https://github.com/mgaitan/waliki/pull/110>`_
- Run git with output to pipe instead of virtual terminal. `#111 <https://github.com/mgaitan/waliki/pull/111>`_

0.5 (2015-04-12)
++++++++++++++++++

- Per page markup is now fully functional. It allows to
  have a mixed rst & markdown wiki. Fixed `#2 <https://github.com/mgaitan/waliki/issues/2>`__
- Allow save a page without changes in a body.
  Fixed `#85 <https://github.com/mgaitan/waliki/issues/85>`__
- Fixed `#84 <https://github.com/mgaitan/waliki/issues/84>`__, that marked deleted but no commited after a move
- Allow to choice markup from new page dialog. `#82 <https://github.com/mgaitan/waliki/issues/82>`__
- Fix wrong encoding for raw of an old revision. `#75 <https://github.com/mgaitan/waliki/issues/75>`__


0.4.2 (2015-03-31)
++++++++++++++++++

- Fixed conflict with a broken dependecy


0.4.1 (2015-03-31)
++++++++++++++++++

- Marked the release as beta (instead of alpha)
- Improves on setup.py and the README

0.4 (2015-03-31)
++++++++++++++++

- Implemented views to add a new, move and delete pages
- Implemented real-time collaborative editing via together.js
  (`#33 <https://github.com/mgaitan/waliki/issues/33>`__)
- Added pagination in *what changed* page
- Added a way to extend waliki's docutils with directives and transformation for
- A deep docs proofreading by `chuna <https://github.com/chuna>`__
- Edit view redirect to detail if the page doesn't exist
  (`#37 <https://github.com/mgaitan/waliki/issues/37>`__)
- waliki\_box fails with missing slug
  `#40 <https://github.com/mgaitan/waliki/issues/40>`__
- can't view diffs on LMDE
  `#60 <https://github.com/mgaitan/waliki/issues/60>`__
- fix typos in tutorial
  `#76 <https://github.com/mgaitan/waliki/pull/76>`__
  (`martenson <https://github.com/martenson>`__)
- Fix build with Markups 0.6.
  `#63 <https://github.com/mgaitan/waliki/pull/63>`__
  (`loganchien <https://github.com/loganchien>`__)
- fixed roundoff error for whatchanged pagination
  `#61 <https://github.com/mgaitan/waliki/pull/61>`__
  (`aszepieniec <https://github.com/aszepieniec>`__)

- Enhance slides `#59 <https://github.com/mgaitan/waliki/pull/59>`__
  (`loganchien <https://github.com/loganchien>`__)

- Fix UnicodeDecodeError in waliki.git.view.
  `#58 <https://github.com/mgaitan/waliki/pull/58>`__
  (`loganchien <https://github.com/loganchien>`__)

0.3.3 (2014-11-24)
++++++++++++++++++

- Tracking page redirections
- fix bugs related to attachments in `sync_waliki`
- The edition form uses crispy forms if it's installed
- many small improvements to help the integration/customization

0.3.2 (2014-11-17)
++++++++++++++++++

- Url pattern is configurable now. By default allow uppercase and underscores
- Added ``moin_migration_cleanup``, a tool to cleanup the result of a moin2git_ import
- Improve git parsers for *page history* and *what changed*

.. _moin2git: https://github.com/mgaitan/moin2git


0.3.1 (2014-11-11)
++++++++++++++++++

- Plugin *attachments*
- Implemented *per namespace* ACL rules
- Added the ``waliki_box`` templatetag: use waliki content in any app
- Added ``entry_point`` to extend templates from plugins
- Added a webhook to pull and sync change from a remote repository (Git)
- Fixed a bug in git that left the repo unclean

0.2 (2014-09-29)
++++++++++++++++

- Support concurrent edition
- Added a simple ACL system
- ``i18n`` support (and locales for ``es``)
- Editor based in Codemirror
- Migrated templates to Bootstrap 3
- Added the management command ``waliki_sync``
- Added a basic test suite and setup Travis CI.
- Added "What changed" page (from Git)
- Plugins can register links in the nabvar (``{% navbar_links %}``)

0.1.2 / 0.1.3 (2014-10-02)
++++++++++++++++++++++++++

* "Get as PDF" plugin
* rst2html5 fixes

0.1.1 (2014-10-02)
++++++++++++++++++

* Many Python 2/3 compatibility fixes

0.1.0 (2014-10-01)
++++++++++++++++++

* First release on PyPI.

