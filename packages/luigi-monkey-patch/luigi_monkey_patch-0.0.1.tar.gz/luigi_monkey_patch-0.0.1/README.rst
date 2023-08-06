Luigi is a Python (2.7, 3.3, 3.4, 3.5) package that helps you build complex 
pipelines of batch jobs. It handles dependency resolution, workflow management, 
visualization, handling failures, command line integration, and much more.


Current Luigi has some issues in s3 file iteration in production. When the file 
is too large, Amazon s3 would tend to disconnect first. Any application should 
support retry based on current status to aquire the whole part. This project add 
this part for luigi s3 file iteration feature.

Getting Started
---------------

Run ``pip install luigi_monkey_patch`` to install the latest stable version from `Pypi <https://pypi.python.org/pypi/luigi_monkey_patch>`_. Documentation and any issues are hosted `here <https://github.com/zenixls2/luigi_monkey_patch>`__.

Modified Functions
------------------
* ``luigi.s3.ReadableS3File.close``
* ``luigi.s3.ReadableS3File.__iter__``

Authors
-------

Luigi was built at `Spotify <https://www.spotify.com/us/>`_.
This patch is done by `Zenix Huang <https://github.com/zenixls2>`_.
