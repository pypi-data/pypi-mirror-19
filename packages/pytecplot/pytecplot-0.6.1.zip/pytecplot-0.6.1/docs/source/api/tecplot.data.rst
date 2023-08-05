Data
====

..  contents::
    :local:
    :depth: 2

.. automodule:: tecplot.data

Loading Data
------------

.. autofunction:: tecplot.data.load_tecplot
.. autofunction:: tecplot.data.load_cgns
.. autofunction:: tecplot.data.load_fluent
.. autofunction:: tecplot.data.load_plot3d

Saving Data
-----------

.. autofunction:: tecplot.data.save_tecplot_binary
.. autofunction:: tecplot.data.save_tecplot_ascii

Data Queries
------------

.. autofunction:: tecplot.data.query.probe_at_position

Data Operations
---------------

.. autofunction:: tecplot.data.operate.Range
.. autofunction:: tecplot.data.operate.execute_equation

.. _data_access:

Data Access
-----------

..  contents::
    :local:
    :depth: 2

.. py:currentmodule:: tecplot.data

Dataset
^^^^^^^

.. autoclass:: Dataset

    **Attributes**

    .. autosummary::
        :nosignatures:

        VariablesNamedTuple
        num_variables
        num_zones
        title

    **Methods**

    .. autosummary::

        add_fe_zone
        add_ordered_zone
        add_poly_zone
        add_variable
        add_zone
        copy_zones
        delete_variables
        delete_zones
        variable
        variables
        zone
        zones

.. autoattribute:: Dataset.VariablesNamedTuple
.. automethod:: Dataset.add_fe_zone
.. automethod:: Dataset.add_ordered_zone
.. automethod:: Dataset.add_poly_zone
.. automethod:: Dataset.add_variable
.. automethod:: Dataset.add_zone
.. automethod:: Dataset.copy_zones
.. automethod:: Dataset.delete_variables
.. automethod:: Dataset.delete_zones
.. autoattribute:: Dataset.num_variables
.. autoattribute:: Dataset.num_zones
.. autoattribute:: Dataset.title
.. automethod:: Dataset.variable
.. automethod:: Dataset.variables
.. automethod:: Dataset.zone
.. automethod:: Dataset.zones

.. py:currentmodule:: tecplot.data

Variable
^^^^^^^^

.. autoclass:: Variable

    **Attributes**

    .. autosummary::
        :nosignatures:

        index
        name
        num_zones

    **Methods**

    .. autosummary::

        values

.. autoattribute:: Variable.index
.. autoattribute:: Variable.name
.. autoattribute:: Variable.num_zones
.. automethod:: Variable.values

Zones
^^^^^

..  contents::
    :local:
    :depth: 1

.. automodule:: tecplot.data.zone

.. py:currentmodule:: tecplot.data

OrderedZone
+++++++++++

.. autoclass:: OrderedZone

    **Attributes**

    .. autosummary::
        :nosignatures:

        dimensions
        index
        name
        num_elements
        num_points
        num_points_per_element
        num_variables
        rank
        solution_time
        strand
        zone_type

    **Methods**

    .. autosummary::

        copy
        values

.. automethod:: OrderedZone.copy
.. autoattribute:: OrderedZone.dimensions
.. autoattribute:: OrderedZone.index
.. autoattribute:: OrderedZone.name
.. autoattribute:: OrderedZone.num_elements
.. autoattribute:: OrderedZone.num_points
.. autoattribute:: OrderedZone.num_points_per_element
.. autoattribute:: OrderedZone.num_variables
.. autoattribute:: OrderedZone.rank
.. autoattribute:: OrderedZone.solution_time
.. autoattribute:: OrderedZone.strand
.. automethod:: OrderedZone.values
.. autoattribute:: OrderedZone.zone_type

.. py:currentmodule:: tecplot.data

ClassicFEZone
+++++++++++++

.. autoclass:: ClassicFEZone

    **Attributes**

    .. autosummary::
        :nosignatures:

        index
        name
        nodemap
        num_elements
        num_points
        num_points_per_element
        num_variables
        rank
        solution_time
        strand
        zone_type

    **Methods**

    .. autosummary::

        copy
        values

.. automethod:: ClassicFEZone.copy
.. autoattribute:: ClassicFEZone.index
.. autoattribute:: ClassicFEZone.name
.. autoattribute:: ClassicFEZone.nodemap
.. autoattribute:: ClassicFEZone.num_elements
.. autoattribute:: ClassicFEZone.num_points
.. autoattribute:: ClassicFEZone.num_points_per_element
.. autoattribute:: ClassicFEZone.num_variables
.. autoattribute:: ClassicFEZone.rank
.. autoattribute:: ClassicFEZone.solution_time
.. autoattribute:: ClassicFEZone.strand
.. automethod:: ClassicFEZone.values
.. autoattribute:: ClassicFEZone.zone_type

.. py:currentmodule:: tecplot.data

PolyFEZone
++++++++++

.. autoclass:: PolyFEZone

    **Attributes**

    .. autosummary::
        :nosignatures:

        face_neighbors
        facemap
        index
        name
        num_elements
        num_faces
        num_points
        num_variables
        rank
        solution_time
        strand
        zone_type

    **Methods**

    .. autosummary::

        copy
        create_facemap
        values

.. automethod:: PolyFEZone.copy
.. automethod:: PolyFEZone.create_facemap
.. autoattribute:: PolyFEZone.face_neighbors
.. autoattribute:: PolyFEZone.facemap
.. autoattribute:: PolyFEZone.index
.. autoattribute:: PolyFEZone.name
.. autoattribute:: PolyFEZone.num_elements
.. autoattribute:: PolyFEZone.num_faces
.. autoattribute:: PolyFEZone.num_points
.. autoattribute:: PolyFEZone.num_variables
.. autoattribute:: PolyFEZone.rank
.. autoattribute:: PolyFEZone.solution_time
.. autoattribute:: PolyFEZone.strand
.. automethod:: PolyFEZone.values
.. autoattribute:: PolyFEZone.zone_type

.. py:currentmodule:: tecplot.data

Array
^^^^^

.. autoclass:: Array

    **Attributes**

    .. autosummary::
        :nosignatures:

        c_type
        data_type
        location
        max
        min
        minmax
        shape
        size

    **Methods**

    .. autosummary::

        as_numpy_array
        copy

.. automethod:: Array.as_numpy_array
.. autoattribute:: Array.c_type
.. automethod:: Array.copy
.. autoattribute:: Array.data_type
.. autoattribute:: Array.location
.. autoattribute:: Array.max
.. autoattribute:: Array.min
.. autoattribute:: Array.minmax
.. autoattribute:: Array.shape
.. autoattribute:: Array.size

.. py:currentmodule:: tecplot.data

Nodemap
^^^^^^^

.. autoclass:: Nodemap

    **Attributes**

    .. autosummary::
        :nosignatures:

        c_type
        num_points_per_element
        shape

    **Methods**

    .. autosummary::

        copy

.. autoattribute:: Nodemap.c_type
.. automethod:: Nodemap.copy
.. autoattribute:: Nodemap.num_points_per_element
.. autoattribute:: Nodemap.shape

.. py:currentmodule:: tecplot.data

Facemap
^^^^^^^

.. autoclass:: Facemap

    **Attributes**

    .. autosummary::
        :nosignatures:

        element_c_type
        node_c_type
        num_faces

    **Methods**

    .. autosummary::

        assign_mapping

.. automethod:: Facemap.assign_mapping
.. autoattribute:: Facemap.element_c_type
.. autoattribute:: Facemap.node_c_type
.. autoattribute:: Facemap.num_faces

.. py:currentmodule:: tecplot.data

FaceNeighbors
^^^^^^^^^^^^^

.. autoclass:: FaceNeighbors

    **Attributes**

    .. autosummary::
        :nosignatures:

        c_type
        mode

    **Methods**

    .. autosummary::

        set_connection

.. autoattribute:: FaceNeighbors.c_type
.. autoattribute:: FaceNeighbors.mode
.. automethod:: FaceNeighbors.set_connection

Auxiliary Data
--------------

.. py:currentmodule:: tecplot.data

AuxData
^^^^^^^

.. autoclass:: AuxData

    **Methods**

    .. autosummary::

        item

.. automethod:: AuxData.item
