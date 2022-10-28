# pymemuc

[![GitHub](https://img.shields.io/github/license/marmig0404/pymemuc)](LICENSE) [![CodeFactor](https://www.codefactor.io/repository/github/marmig0404/pymemuc/badge)][codefactor_link] [![PyPI](https://img.shields.io/pypi/v/pymemuc) ![PyPI - Downloads](https://img.shields.io/pypi/dm/pymemuc)][pypi_link] [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymemuc)][python_link]

A wrapper for [MEmu Command (MEMUC)][memuc_docs] in python.

Allows for easy interaction with MEmu VMs, including management, configuration, direct control and ADB interaction.

## Installation

```bash
pip install pymemuc
```

## Example usage

```python
# import the PyMemuc class
from pymemuc import PyMemuc

# create a PyMemuc instance, doing so will automatically link to the MEMUC executable
memuc = PyMemuc()

# create a new vm
memuc.create_vm()

# list out all vms, get the index of the first one
index = memuc.list_vm_info()[0][0]

# start the vm
memuc.start_vm(index)

# stop the vm
memuc.stop_vm(index)
```

See [the demo notebook][demo_notebook] for more examples.

## Documentation

See the [API documentation][full_doc].

[python_link]: https://www.python.org/
[pypi_link]: https://pypi.org/project/pymemuc/
[codefactor_link]: https://www.codefactor.io/repository/github/marmig0404/pymemuc
[memuc_docs]: https://www.memuplay.com/blog/memucommand-reference-manual.html
[demo_notebook]: demo/demo.ipynb
[full_doc]: https://pymemuc.readthedocs.io
