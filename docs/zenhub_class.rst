Usage
=====

Testing!

.. autoclass:: zenhub.Zenhub

Issues
------

Get Issue Data
^^^^^^^^^^^^^^
.. automethod:: zenhub.Zenhub.get_issue_data

Get Issue Events
^^^^^^^^^^^^^^^^
.. automethod:: zenhub.Zenhub.get_issue_events

Move issues
^^^^^^^^^^^
.. automethod:: zenhub.Zenhub.move_issue

Move issues in oldest workspace
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: zenhub.Zenhub.move_issue_in_oldest_workspace

Set issue estimate
^^^^^^^^^^^^^^^^^^
.. automethod:: zenhub.Zenhub.set_issue_estimate


Epics
-----

Get Epics for a Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.get_epics

Get Epic Data
^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.get_epic_data

Convert an Epic to an Issue
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.convert_epic_to_issue

Convert an Issue to Epic
^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.convert_issue_to_epic

Add or Remove Issues from an Epic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.add_or_remove_issues_to_epic

Workspaces
----------

Get ZenHub Workspaces for a repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.get_workspaces

Get a ZenHub Board for a repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.get_repository_board

Get the oldest ZenHub Board for a repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.get_oldest_repository_board

Milestones
----------

Set the Milestone Start Date
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.set_milestone_start_date

Get the Milestone Start Date
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.get_milestone_start_date

Dependencies
------------

Get Dependencies for a Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.get_dependencies

Create a Dependency
^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.create_dependency

Remove a Dependency
^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.remove_dependency

Release Reports
---------------

Create a Release Report
^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.create_release_report

Get a Release Report
^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.get_release_report

Get Release Reports for a Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.get_release_reports

Edit a Release Report
^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.edit_release_report

Add a Repository to a Release Report
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.add_repo_to_release_report

Remove a Repository from a Release Report
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.remove_repo_from_release_report

Release Report Issues
---------------------

Get all the Issues in a Release Report
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.get_release_report_issues

Add or Remove Issues from a Release Report
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: zenhub.Zenhub.add_or_remove_issues_from_release_report

Rate Limits
-----------
.. automethod:: zenhub.Zenhub.rate_limit
