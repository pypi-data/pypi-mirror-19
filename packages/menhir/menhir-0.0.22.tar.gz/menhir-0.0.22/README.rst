======
Menhir
======

.. image:: https://circleci.com/gh/dialoguemd/menhir.svg?circle-token=56c5301ac8a026188f52c86ee1522709e5d103cb
   :target: https://circleci.com/gh/dialoguemd/menhir

.. image:: https://codecov.io/gh/dialoguemd/menhir/branch/master/graph/badge.svg?token=Fl2ObQ8DC6
   :target: https://codecov.io/gh/dialoguemd/menhir


Menhir is a build tool for monolithic repositories.  Unlike existing
monolithic build tools, it does not aim at being prescriptive about
how (sub-)projects are built.  It prefers to use established single
project build tools at the project level.

Usage
-----

Menhir is zero configuration.

At the root of the repository, menhir can have a `menhir_root.yaml`
file.  This file configures a set of build tools for menhir to use,
using a list on the `tools` key.  If this file is not present, all
built in tools are used.  The file can specify add-in tools that are
maintained outside of menhir itself.

Currently the supported build tools are `setup_py`, `pyenv`, `pytest`
and `script`.

The `menhir` command line provides the `exec` command to execute a
build phase on the monorepo.  The build phases are implemented by the
build tools.

`codecov` - uploads coverage to coverage.io

`docker` - `build`, `push`, `publish`

`dynamodb` - `put`

`setup_py` - `sdist`, `lambda-package`

`pyenv` - `requirements`

`pytest` - `test`

`script` - any phase for which `bin/<phase-name>` exists and is
           executable

`terraform` - `plan`, `apply`, `destroy`

When executing the script tools, the following environment variables
are set if the condition is true:

    MENHIR_CHANGED
    MENHIR_CHANGED_DEP
    MENHIR_CHANGED

Installation
------------

Install using `pip`.

    pip install menhir


Cross project dependencies
--------------------------

The cross project dependencies are discovered by the build tools.
Currently only the `setup_py` tool contributes dependencies.
