==================
Django View Export
==================

Generate CSV reports by simply creating SQL views.

Authenticated staff members can then directly download these reports as CSV.
It's a nice agile way to deal with the changing requirements for reports.


Quick start
-----------

1. Include the URLconf in your project ``urls.py`` like this:

   .. code-block:: python

        url(r'^reports/', include('view_export.urls')),


2. Create an SQL view in your database:

   .. code-block:: sql

        => CREATE VIEW v_staff_names AS (
        ->      SELECT first_name, last_name FROM auth_user
        ->      WHERE is_staff = TRUE);

   You'll probably want to record this SQL in a file such as ``reports.sql`` or
   even better, add it to a Django migration.

3. Start the development server and visit ``http://127.0.0.1:8000/reports/view-export/staff_names/``
   or ``http://127.0.0.1:8000/reports/view-export/v_staff_names/`` to download the SQL view named
   ``v_staff`` as a CSV file.

No settings are required by default and there's no need to add the package to
Django's ``INSTALLED_APPS``. Staff login access is required, so you may wish to
set the ``LOGIN_URL`` setting to ``/admin/login/`` initially.
