# Bigorna

Bigorna is a simple job manager to submit tasks.

[![CircleCI](https://circleci.com/gh/cliixtech/bigorna.svg?style=svg)](https://circleci.com/gh/cliixtech/bigorna)

Tasks are simple commands with extra parameters, defined by a configuration file. It was built to
be integrated with other tools (eg.: bots) to fire recurrent operation tasks,
such as deployments and so on.

Bigorna takes care of executing the tasks, controlling how many tasks can run simultaneously
and tracking all submitted jobs.

Bigorna is dead-simple, so it uses an sqlite db to track the jobs and keeps jobs output on simple
txt files on the disc.

# Getting start

**Bigorna** is a Python3 software.

To install it you can do:

    python setup.py install

After installing the command *bigorna*  will be available.

But before run you need a configuration file. Take a look on the `config-example.yml` file.

Finally, before starting firing tasks, do a `bigorna create_db` to setup the database.

You can run jobs in standalone mode with `bigorna execute <task> <params>` or run the server mode
with `bigorna runserver`.

## Standalone mode

It executes the task directly, skipping all the scheduling and tracking management, that means
that no record will be kept and out the output will be send to stout.

## Server mode

It runs a simple webserver that provides an REST API and a very simple webview.

Currently isn't possible to submit jobs through the webview - just see task history, status and
output.

To submit a job you need to do a POST call to `/api/jobs/<job_type>` passing the parameters as
a json object to the call.

Please, note that if you include on the json content a property called `submitter` with your name
the jobtracker will register, otherwise it will assume `anonymous` task. Specifying the *submitter*
is a good practice to allow better tracking.

# Development

To setup your bigorna deve environment we recommend you to create a **virtualenv** with *Python3.5+*.

After creating the virtualenv, install the development requirements with
`pip install -r dev_requirements` and then install bigorna as development mode using
`python setup.py develop`.

To run the test do `nosetests -s -v -d` and `flake8 tests/ bigorna/` to check code style.

# License

This software is release unde **GPLv3** license. You can find more about on the LICENSE file.

