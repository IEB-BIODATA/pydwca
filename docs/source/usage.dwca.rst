DWCA Module
===========

Reading a DwCA file
-------------------

A Darwin Core Archive file is a compress ``zip`` or ``tar.gz`` file containing the component files in a star scheme and the descriptor files. Whole documentation of Darwin Core in the `text guide <https://dwc.tdwg.org/text/>`_.

Assuming the archive is inside a ``DwCArchive.zip`` file containing:

- ``meta.xml``: Mandatory descriptor file.
- ``eml.xml``: Metadata file.
- ``taxon.txt``: Core component.
- ``identifier.txt``: Identifier extension component.
- ``speciesprofile.txt``: Species profile extension component.
- ``reference.txt``: Reference extension component.

All of these files must be specified in the ``meta.xml`` file as described in the `text guide, section metafile content <https://dwc.tdwg.org/text/#2-metafile-content>`_.

To read this file you can:

.. code-block:: python

    from dwca import DarwinCoreArchive

    darwin_core = DarwinCoreArchive.from_archive("DwCArchive.zip")

To check the components on it:

.. code-block:: python

    print(darwin_core.core)

.. code-block:: python

    Core:
        class: Taxon
        filename: taxon.txt
        content: 163461 entries

The extensions component are stores in a ``Python list`` and can be access in the same way:

.. code-block:: python

    print(len(darwin_core.extension))

.. code-block:: python

    3

Check the first one:

.. code-block:: python

    print(darwin_core.extension[0])

.. code-block:: python

    Extension:
        class: SpeciesProfile
        filename: speciesprofile.txt
        content: 153622 entries

And you can work with this data as an array of ``Python objects``, as ``numpy arrays` or as ``pandas DataFrames``

.. code-block:: python

    darwin_core.core.data

.. code-block:: python

    [<Taxon urn:lsid:example.org:taxname:1>, <Taxon urn:lsid:example.org:taxname:2>, ...]

.. code-block:: python

    darwin_core.core.data.as_pandas()

.. code-block:: python

    Pending...

Writing a DwCA archive
----------------------

To generate a new Darwin Core Archive file you can use the same class and build that starting point:

.. code-block:: python

    from dwca import DarwinCoreArchive
    from eml.resources import EMLResource
    from eml.types import ResponsibleParty, IndividualName

    # Define the metadata file future location
    darwin_core = DarwinCoreArchive(metadata="eml.xml")

The `guidelines <https://dwc.tdwg.org/text/#211-attributes>`_ suggest to add a metadata file in a standardized form. Alternatives suggest EML (Ecological Metadata Language), FGDC (Federal Geographic Data Committee) or ISO 19115.

For this package, we implemented EML support (`Next section <#eml-module>`_) for the metadata, and can be added and worked like this:

.. code-block:: python

    darwin_core.metadata.define_resource(EMLResource.DATASET)
    darwin_core.metadata.add_title("Example for Darwin Core Archive")
    darwin_core.metadata.add_creator(ResponsibleParty(
        individual_name=IndividualName(
            last_name="Doe",
            first_name="John",
            salutation="Mr."
        )
    ))

    # Add core data
    darwin_core.set_core("taxon.txt")
    # Add an extension
    darwin_core.add_extension("identifier.txt")

    # Write the archive
    with open("example.zip", "wb") as example_file:
        darwin_core.to_file(example_file)


There are other ways to add data. Check the whole documentation for more information.
