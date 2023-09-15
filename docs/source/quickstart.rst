Quick Start
===========

.. _installation:

Installation
------------

To use pymemuc, first install it using pip:

.. code-block:: console

   $ pip install pymemuc


.. _example_usage:

Example Usage
-------------

.. code-block:: python

    # import the PyMemuc class
    from pymemuc import PyMemuc

    # create a PyMemuc instance, doing so will automatically link to the MEMUC executable
    memuc = PyMemuc()

    # create a new vm, saving the index
    index = memuc.create_vm()

    # start the vm
    memuc.start_vm(index)

    # stop the vm
    memuc.stop_vm(index)

    # delete the vm
    memuc.delete_vm(index)
