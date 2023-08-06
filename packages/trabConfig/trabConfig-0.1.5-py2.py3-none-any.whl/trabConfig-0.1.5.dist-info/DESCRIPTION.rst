trabConfig
==========

A simple Config file parser that supports json, and yaml formats with auto-save feature.


Installation
------------

from pip ::

    pip install trabConfig

or the old fashioned way ::

    python setup.py install

*NOTE: wheels and source dists also available on pypi*


Usage
-----

Example -

.. code-block:: python

    from trabconfig import trabConfig

    # load file verbatim
    config = trabConfig("config.json", autosave=False, data='json')

    # or just
    config = trabConfig("config.json")

    # for yaml
    config = trabConfig("config.yml", data='yaml)

    # autosave capability (saves on changes)
    config.autosave = True

    # or during instantiation
    config = trabConfig("config.json", autosave=True)

    # usage example
    health = config['health']
    config['health'] = 9999

    mana = config.get('mana', None)
    if mana is not None:
        config['mana'] = 999

    lvl = config.get('lvl')
    config.set('lvl', 99)

    config.new('items', [])
    config['items'].append('gold')

    config.delete('cloth')
    config.save()


Notes
-----

Created by - traBpUkciP 2016-2017

