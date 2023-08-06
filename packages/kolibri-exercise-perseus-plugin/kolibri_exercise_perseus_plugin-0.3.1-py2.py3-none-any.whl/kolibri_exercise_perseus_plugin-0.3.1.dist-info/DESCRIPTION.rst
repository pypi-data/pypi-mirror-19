Kolibri Exercise Renderer for Perseus
=====================================

What is Kolibri?
----------------

Kolibri is a Learning Management System / Learning App designed to run on low-power devices, targeting the needs of
learners and teachers in contexts with limited infrastructure. A user can install Kolibri and serve the app on a local
network, without an internet connection. Kolibri installations can be linked to one another, so that user data and
content can be shared. Users can create content for Kolibri and share it when there is network access to another
Kolibri installation or the internet.

See https://learningequality.org/kolibri/ for more info.

What is Perseus?
----------------

Khan Academy's exercise question editor and renderer.

See https://github.com/Khan/perseus for more info.

What is this plugin?
--------------------

A Perseus renderer wrapper for Kolibri that can track learning progress and save to the database.

How can I install this plugin?
------------------------------

1. Inside your Kolibri virtual environment:
    ``pip install kolibri-perseus-exercise-plugin``

2. Activate the plugin:

    ``kolibri plugin exercise_perseus_renderer enable``

3. Restart Kolibri.

How can I install this plugin for development?
------------------------------

1. Download this repo.
2. Open terminal in your Kolibri repo.
4. run the following commands:

    ``pip install -e <KOLIBRI-PERSEUS-PLUGIN-LOCAL-PATH>``

    ``kolibri plugin exercise_perseus_renderer enable``

5. Then run the commands to install frontend packages in Kolibri, this plugin will have its recursively installed.

6. If you have updated the version of Perseus in the repo, run the following command:

    ``./update_perseus.sh``

How to publish to PyPi?
------------------------------

1. Follow the instructions above to installing the plugin for development.
2. From the Kolibri directory run the frontend build command.
3. update `setup.py` to a newer version.
4. Terminal move to the root level of repo dir and run the following command to publish to PyPi:

    ``make release``


How can I contribute?
---------------------

 * `Documentation <http://kolibri.readthedocs.org/en/latest/>`_ is available online, and in the ``docs/`` directory.
 * Mailing list: `Google groups <https://groups.google.com/a/learningequality.org/forum/#!forum/dev>`_.
 * IRC: #kolibri on Freenode


