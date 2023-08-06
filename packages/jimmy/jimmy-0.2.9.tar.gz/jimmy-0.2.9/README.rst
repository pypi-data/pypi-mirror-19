.. image:: https://ci-team.github.io/logo+title_small.png

.. image:: https://travis-ci.org/ci-team/jimmy.svg?branch=master
    :target: https://travis-ci.org/ci-team/jimmy

Jimmy is a command line tool to manage `Jenkins <https://jenkins.io>`_
Master configuration,
including Jenkins plugin parameters like Gerrit URL for Gerrit Trigger
plugin or global credentials.

See `./plugins/` directory for full list of supported plugins.

How to use
==========

#. Clone Jimmy repo::

     $ git clone https://review.fuel-infra.org/fuel-infra/jimmy
     $ cd jimmy

#. Setup venv::

     $ sudo pip install virtualenv
     $ cd work_folder && virtualenv venv
     $ source venv/bin/activate

#. Install the required python packages using pip::

     $ pip install -r requirements.txt


#. Create YAML file `my_jenkins.yaml` with jenkins parameters. Check
   `./samples/input/jenkins.yaml` for example.

#. Define env (Jenkins instance) in jimmy.yaml::

     envs:
       my_jenkins:
         jenkins_url: http://localhost:8080
         jenkins_config_path: my_jenkins.yaml

#. Run::

     $ python jimmy.py --conf-path jimmy.yaml -e my_jenkins
