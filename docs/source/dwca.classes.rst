dwca.classes package
====================

This module corresponds to the "class" type terms defined in the https://dwc.tdwg.org/list/#31-index-by-term-name "Classes" section, excluding the deprecated ones. These Python classes represent a complete file in a Darwin Core Archive.

This classes are the ones listed in the description of `rowType` in the `Attributes section <https://dwc.tdwg.org/text/#221-attributes>`_ for a `<core>` or `<extension>` element. Presented below:

    (...) For convenience the URIs for classes defined by the Darwin Core are: dwc:Occurrence: http://rs.tdwg.org/dwc/terms/Occurrence, dwc:Organism: http://rs.tdwg.org/dwc/terms/Organism, dwc:MaterialEntity: http://rs.tdwg.org/dwc/terms/MaterialEntity, dwc:MaterialSample: http://rs.tdwg.org/dwc/terms/MaterialSample, dwc:Event: http://rs.tdwg.org/dwc/terms/Event, dcterms:Location: http://purl.org/dc/terms/Location, dwc:GeologicalContext: http://purl.org/dc/terms/GeologicalContext, dwc:Identification: http://rs.tdwg.org/dwc/terms/Identification, dwc:Taxon: http://rs.tdwg.org/dwc/terms/Taxon, dwc:ResourceRelationship: http://rs.tdwg.org/dwc/terms/ResourceRelationship, dwc:MeasurementOrFact: http://rs.tdwg.org/dwc/terms/MeasurementOrFact, chrono:ChronometricAge: http://rs.tdwg.org/chrono/terms/ChronometricAge,

DataFile Class
--------------

.. automodule:: dwca.classes.data_file
   :members:
   :undoc-members:
   :show-inheritance:

OutsideClass Class
------------------

This is a special class, and its idea is to represent any data file that is not defined in the standard.

.. automodule:: dwca.classes.outside_class
   :members:
   :undoc-members:
   :show-inheritance:

ChronometricAge Class
---------------------

This particular "class" term was extracted from http://rs.tdwg.org/dwc/doc/chrono/ (https://chrono.tdwg.org/list/#31-index-by-term-name "Classes" section).

.. automodule:: dwca.classes.chronometric_age
   :members:
   :undoc-members:
   :show-inheritance:


Event Class
-----------

.. automodule:: dwca.classes.event
   :members:
   :undoc-members:
   :show-inheritance:

GeologicalContext Class
-----------------------

.. automodule:: dwca.classes.geological_context
   :members:
   :undoc-members:
   :show-inheritance:

Identification Class
--------------------

.. automodule:: dwca.classes.identification
   :members:
   :undoc-members:
   :show-inheritance:

Location Class
--------------

.. automodule:: dwca.classes.location
   :members:
   :undoc-members:
   :show-inheritance:

MaterialEntity Class
--------------------

.. automodule:: dwca.classes.material_entity
   :members:
   :undoc-members:
   :show-inheritance:

MaterialSample Class
--------------------

.. automodule:: dwca.classes.material_sample
   :members:
   :undoc-members:
   :show-inheritance:

MeasurementOrFact Class
-----------------------

.. automodule:: dwca.classes.measurement_or_fact
   :members:
   :undoc-members:
   :show-inheritance:

Occurrence Class
----------------

.. automodule:: dwca.classes.occurrence
   :members:
   :undoc-members:
   :show-inheritance:

Organism Class
--------------

.. automodule:: dwca.classes.organism
   :members:
   :undoc-members:
   :show-inheritance:

ResourceRelationship Class
--------------------------

.. automodule:: dwca.classes.resource_relationship
   :members:
   :undoc-members:
   :show-inheritance:

Taxon Class
-----------

.. automodule:: dwca.classes.taxon
   :members:
   :undoc-members:
   :show-inheritance:
