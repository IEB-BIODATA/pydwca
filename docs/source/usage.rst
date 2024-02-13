Usage
=====

.. contents:: Contents
    :depth: 2
    :local:

DWCA Module
-----------

Reading a DwCA file
~~~~~~~~~~~~~~~~~~~

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
        filename: taxon.txt
        content: 98 species

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
        filename: identifier.txt
        content: 98 species

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
~~~~~~~~~~~~~~~~~~~~~~

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

EML Module
----------

Reading a ``eml.xml`` file
~~~~~~~~~~~~~~~~~~~~~~~~~~

An EML file, or a Ecological Metadata Language (see specification on `this link <https://eml.ecoinformatics.org/>`_, use the method ``from_xml`` of the ``EML`` class, there are also the method ``from_string`` to read from a text string directly.

.. code-block:: python

    from eml import EML

    eml_file = EML.from_xml("eml.xml")

    # To see a summary of the content of the metadata file:
    print(eml_file)

.. code-block:: python

    Pending..

Writing a EML
~~~~~~~~~~~~~

To write a new EML with the information you need about your resource, build starting with the EML class:

.. code-block:: python

    import datetime as dt

    from eml import EML
    from eml.resources import EMLResource
    from eml.types import ResponsibleParty, IndividualName, OrganizationName

    eml_file = EML(
        package_id="Example package",
        system="http://my.system",
        resource_type=EMLResource.DATASET,
    )
    eml_file.add_title("Example for Darwin Core Archive")
    eml_file.add_creator(ResponsibleParty(
        individual_name=IndividualName(
            last_name="Doe",
            first_name="John",
            salutation="Mr."
        )
    ))
    eml_file.add_metadata_provider(ResponsibleParty(
        organization_name=OrganizationName("Metadata Provider Organization")
    ))
    eml_file.set_publication_date(dt.date(2024, 2, 9))

    # For other possible information to add check the full documentation of the module.

    # To write the XML file
    with open("eml.xml", "w", encoding="utf-8") as file:
        file.write(eml_file.to_xml())
