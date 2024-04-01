EML Module
==========

Reading a ``eml.xml`` file
--------------------------

An EML file, or a Ecological Metadata Language (see specification on `this link <https://eml.ecoinformatics.org/>`_, use the method ``from_xml`` of the ``EML`` class, there are also the method ``from_string`` to read from a text string directly.

.. code-block:: python

    from eml import EML

    eml_file = EML.from_xml("eml.xml")

    # To see a summary of the content of the metadata file:
    print(eml_file)

.. code-block::

    EML:
        Resource Type: DATASET
        Title: Example for Darwin Core Archive
        Creator: Creator Organization
        MetadataProvider: Metadata Manager at Metadata Provider Organization
        Custodian Steward: Doe, J. (Custodian Steward)
        Originator: Doe, J.
        Author: Example, J.

Writing a EML
-------------

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
