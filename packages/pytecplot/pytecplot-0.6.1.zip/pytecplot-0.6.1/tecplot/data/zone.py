import logging

from functools import reduce
from textwrap import dedent

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from ..tecutil import Index, inherited_property, lock, log_setattr
from .array import Array
from .face_neighbors import FaceNeighbors
from .facemap import Facemap
from .nodemap import Nodemap

log = logging.getLogger(__name__)


@log_setattr
class Zone(object):
    def __init__(self, uid, dataset):
        self.uid = uid
        self.dataset = dataset

    def __str__(self):
        """Brief string representation.

        Returns:
            `string <str>`: Brief representation of this `Zone <data_access>`,
            showing a list of associated `Variables <Variable>`.

        Example::

            >>> rect_zone = dataset.zone('Rectangular zone')
            >>> print(rect_zone)
            Zone: 'Rectangular zone'
              Dataset: 'My Dataset'
              Type: Ordered
              Shape: (10, 10, 10)
              Variables: ['x', 'y', 'z']
        """
        fmt = dedent('''\
            Zone: '{}'
              Dataset: '{}'
              Type: {}
              Shape: {}
              Variables: {}''')
        vnames = [str(v.name) for v in self.dataset.variables()]
        return fmt.format(self.name, self.dataset.title, self.zone_type.name,
                          self._shape, vnames)

    def __repr__(self):
        """Executable string representation.

        Returns:
            `string <str>`: Internal representation of this `Zone
            <data_access>`.

        The string returned can be executed to generate a clone of this
        `Zone <data_access>` object::

            >>> rectzone = dataset.zone('Rectangular zone')
            >>> print(repr(rectzone))
            Zone(uid=31, Dataset(uid=21, frame=Frame(uid=11, page=Page(uid=1)))
            >>> exec('rectzone_clone = '+repr(rectzone))
            >>> rectzone_clone
            Zone(uid=31, Dataset(uid=21, frame=Frame(uid=11, page=Page(uid=1)))
            >>> rectzone == rectzone_clone
            True
        """
        return 'Zone(uid={uid}, dataset={dataset})'.format(
            uid=self.uid, dataset=repr(self.dataset))

    def __eq__(self, other):
        """Checks for equality in the |Tecplot Engine|.

        Returns:
            `bool`: `True` if the unique ID numbers are the same for both
            `Zones <data_access>`.
        """
        return self.uid == other.uid

    def __ne__(self, other):
        return not (self == other)

    @property
    def index(self):
        """Zero-based position within the parent `Dataset`.

        :type: `Index`

        This is the value used to obtain a specific zone if you have
        duplicately named zones in the dataset::

            >>> tp.new_layout()
            >>> frame = tp.active_frame()
            >>> dataset = frame.create_dataset('Dataset', ['x', 'y'])
            >>> dataset.add_ordered_zone('Zone', (10,10,10))
            >>> dataset.add_ordered_zone('Zone', (3,3,3))
            >>> # getting zone by name always returns first match
            >>> print(dataset.zone('Zone').index)
            0
            >>> # use index to get specific zone
            >>> print(dataset.zone(1).dimensions)
            (3, 3, 3)
        """
        return Index(_tecutil.ZoneGetNumByUniqueID(self.uid) - 1)

    @property
    def strand(self):
        """The strand ID number.

        :type: `integer <int>`

        Example usage::

            >>> dataset.zone('My Zone').strand = 2
        """
        with self.dataset.frame.activated():
            return _tecutil.ZoneGetStrandID(self.index + 1)

    @strand.setter
    @lock()
    def strand(self, value):
        with self.dataset.frame.activated():
            _tecutil.ZoneSetStrandID(self.index + 1, int(value))

    @property
    def solution_time(self):
        """The solution time for this zone.

        :type: `float`

        Example usage::

            >>> dataset.zone('My Zone').solution_time = 3.14
        """
        return _tecutil.ZoneGetSolutionTime(self.index + 1)

    @solution_time.setter
    @lock()
    def solution_time(self, value):
        with self.dataset.frame.activated():
            _tecutil.ZoneSetSolutionTime(self.index + 1, float(value))

    @property
    def zone_type(self):
        with self.dataset.frame.activated():
            return _tecutil.ZoneGetType(self.index + 1)

    @property
    def name(self):
        """The name of the zone.

        :type: `string <str>`

        Example usage::

            >>> dataset.zone(0).name = 'Zone 0'
        """
        res, zname = _tecutil.ZoneGetNameByDataSetID(self.dataset.uid,
                                                     self.index + 1)
        if not res:
            raise TecplotSystemError()
        return zname

    @name.setter
    @lock()
    def name(self, name):
        _tecutil.ZoneRenameByDataSetID(self.dataset.uid, self.index + 1, name)

    @property
    def num_variables(self):
        """Number of `Variables <Variable>` in the parent `Dataset`.

        :type: `integer <int>`

        Example usage, iterating over all variables by index::

            >>> for i in range(dataset.num_variables):
            ...     variable = dataset.variable(i)
        """
        return self.dataset.num_variables

    def values(self, pattern):
        """Returns an `Array` by index or string pattern.

        Parameters:
            pattern (`integer <int>` or `string <str>`):  Zero-based index or
                `glob-style pattern <fnmatch.fnmatch>` in which case, the
                first match is returned.

        The `Variable.name` attribute is used to match the *pattern* to the
        desired `Array` though this is not necessarily unique::

            >>> ds = frame.dataset
            >>> print(ds)
            Dataset:
              Zones: ['Rectangular zone']
              Variables: ['x', 'y', 'z']
            >>> zone = ds.zone('Rectangular zone')
            >>> x = zone.values('x')
            >>> x == zone.values(0)
            True
        """
        return Array(self, self.dataset.variable(pattern))

    def copy(self):
        """Duplicate this `Zone <data_access>` in the parent `Dataset`.

        The name is copied as well but can be set after duplication::

            >>> new_zone = dataset.zone('My Zone').copy()
            >>> print(new_zone.name)
            My Zone
            >>> new_zone.name = 'My Zone Copy'
            >>> print(new_zone.name)
            My Zone Copy
        """
        return self.dataset.copy_zones(self)[0]

    @property
    def _shape(self):
        return _tecutil.ZoneGetIJKByUniqueID(self.dataset.uid, self.index + 1)


class OrderedZone(Zone):
    """An ordered ``(i, j, k)`` zone within a `Dataset`.

    Ordered zones contain nodal or cell-centered arrays where the connectivity
    is implied by the dimensions and ordering of the data.

    `Zones <data_access>` can be identified (uniquely) by the index with their
    parent `Dataset` or (non-uniquely) by name. In general, a `Variable` must
    be selected to access the underlying data array. This object is used by
    fieldmaps and linemaps to apply style to specific zones. Here we obtain the
    fieldmap associated with the zone named 'My Zone'::

        >>> fmap = plot.fieldmap(dataset.zone('My Zone'))
    """

    @property
    def dimensions(self):
        """Nodal dimensions along ``(i, j, k)``.

        Returns:
            `tuple` of `integers <int>`: ``(i, j, k)`` for ordered data.

        Example usage::

            >>> print(zone.dimensions)
            (128, 128, 128)
        """
        return self._shape

    @property
    def rank(self):
        """Number of dimensions of the data array.

        :type: `integer <int>`

        This will return the number of dimensions which contain more than one
        value::

            >>> zone = dataset.zone('My Zone')
            >>> print(zone.dimensions)
            (10, 10, 1)
            >>> print(zone.rank)
            2
        """
        return sum(s > 1 for s in self.dimensions)

    @property
    def num_points(self):
        """Total number of nodes within this zone.

        :type: `integer <int>`

        This is number of nodes within the zone and is equivalent to the
        product of the values in `OrderedZone.dimensions`. Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> print(zone.dimensions)
            (128, 128, 128)
            >>> print(zone.num_points)
            2097152
        """
        return reduce(lambda x, y: x * y, self.dimensions, 1)

    @property
    def num_elements(self):
        """Number of cells in this zone.

        :type: `integer <int>`

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> print(zone.dimensions)
            (128, 128, 128)
            >>> print(zone.num_elements)
            2048383
        """
        reduced_shape = list(filter(lambda x: x > 1, self.dimensions))
        return reduce(lambda x, y: x * (y - 1), reduced_shape or [1], 1)

    @property
    def num_points_per_element(self):
        """Points per cell for ordered zones.

        :type: `integer <int>`

        For ordered zones, this is :math:`2^{d}` where :math:`d` is the number
        of dimensions::

            >>> zone = dataset.zone('My Zone')
            >>> print(zone.dimensions)
            (10, 10, 1)
            >>> print(zone.rank)
            2
            >>> print(zone.num_points_per_element)
            4
        """
        ndim = self.rank
        return 2**ndim if ndim > 0 else 0

    @inherited_property(Zone)
    def zone_type(self):
        """The `ZoneType` indicating structure of the data contained.

        :type: `ZoneType`

        The specific type of zone this object represents::

            >>> print(dataset.zone(0).zone_type)
            ZoneType.Ordered
        """


class FEZone(Zone):
    @property
    def num_points(self):
        """Total number of nodes within this zone.

        :type: `integer <int>`

        This is the total number of nodes in the zone. Example usage::

            >>> print(dataset.zone('My Zone').num_points)
            2048
        """
        return self._shape[0]

    @property
    def num_elements(self):
        """Number of cells in this finite-element zone.

        :type: `integer <int>`

        Example usage::

            >>> print(dataset.zone('My Zone').num_elements)
            1048576
        """
        return self._shape[1]


class ClassicFEZone(FEZone):
    """A classic finite-element zone within a `Dataset`.

    Classic finite-element zones are arrays of nodes that are connected
    explicitly into pre-defined geometric shapes called "elements." The
    geometry is consistent across the whole zone so that the number of nodes
    per element is constant.

    `Zones <data_access>` can be identified (uniquely) by the index with their
    parent `Dataset` or (non-uniquely) by name. In general, a `Variable` must
    be selected to access the underlying data array. This object is used by
    fieldmaps and linemaps to apply style to specific zones. Here we obtain the
    fieldmap associated with the zone named 'My Zone'::

        >>> fmap = plot.fieldmap(dataset.zone('My Zone'))
    """

    @property
    def num_points_per_element(self):
        """Points per element for classic finite-element zones.

        :type: `integer <int>`

        The number of points (also known as nodes) per finite-element is
        determined from the ``zone_type`` parameter. The follow table shows the
        number of points per element for the available zone types along with
        the resulting shape of the nodemap based on the number of points
        specified (:math:`N`):

            ============== ============== ========================
            Zone Type      Points/Element Nodemap Shape
            ============== ============== ========================
            ``FELineSeg``  2              (:math:`N`, :math:`2 N`)
            ``FETriangle`` 3              (:math:`N`, :math:`3 N`)
            ``FEQuad``     4              (:math:`N`, :math:`4 N`)
            ``FETetra``    4              (:math:`N`, :math:`4 N`)
            ``FEBrick``    8              (:math:`N`, :math:`8 N`)
            ============== ============== ========================

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> print(zone.zone_type)
            ZoneType.FETriangle
            >>> print(zone.num_points_per_element)
            3
        """
        return self.nodemap.num_points_per_element

    @property
    def nodemap(self):
        """The connectivity `Nodemap` for this classic finite-element zone.

        :type: `Nodemap`

        Example usage::

            >>> zone = dataset.zone(0)
            >>> print(zone.nodemap.num_points_per_element)
            4
        """
        return Nodemap(self)

    @inherited_property(Zone)
    def zone_type(self):
        """The `ZoneType` indicating structure of the data contained.

        :type: `ZoneType`

        The specific type of zone this object represents::

            >>> print(dataset.zone(0).zone_type)
            ZoneType.FEBrick
        """

    @property
    def rank(self):
        """Number of dimensions of the data array.

        :type: `integer <int>`

        This indicates the dimensionality of the data and is dependent on the
        type of element this zone contains:

            ============== ====
            Zone Type      Rank
            ============== ====
            ``FELineSeg``  1
            ``FETriangle`` 2
            ``FEQuad``     2
            ``FETetra``    3
            ``FEBrick``    3
            ============== ====

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> print(zone.zone_type)
            ZoneType.FEBrick
            >>> print(zone.rank)
            3
        """
        _rank = {ZoneType.FELineSeg: 1,
                 ZoneType.FETriangle: 2,
                 ZoneType.FEQuad: 2,
                 ZoneType.FETetra: 3,
                 ZoneType.FEBrick: 3}
        return _rank[self.zone_type]


class PolyFEZone(FEZone):
    """A polygonal finite-element zone within a `Dataset`.

    A polygonal zone consists of arrays of nodes which are connected explicitly
    into arbitrary and varying geometric elements. These elements are 2D or 3D
    in nature and have a number of faces (connections between nodes) which hold
    the concept of a left and right neighbor.

    `Zones <data_access>` can be identified (uniquely) by the index with their
    parent `Dataset` or (non-uniquely) by name. In general, a `Variable` must
    be selected to access the underlying data array. This object is used by
    fieldmaps and linemaps to apply style to specific zones. Here we obtain the
    fieldmap associated with the zone named 'My Zone'::

        >>> fmap = plot.fieldmap(dataset.zone('My Zone'))
    """

    @property
    def num_faces(self):
        """Number of faces in this finite-element zone.

        :type: `integer <int>`

        The number of faces may be ``0`` if unknown or facemap creation is
        deferred. Example usage::

            >>> print(dataset.zone('My Zone').num_faces)
            1048576
        """
        return self._shape[2]

    @property
    def rank(self):
        """Number of dimensions of the data array.

        :type: `integer <int>`

        This indicates the dimensionality of the data and is dependent on the
        type of element this zone contains:

            ================ ====
            Zone Type        Rank
            ================ ====
            ``FEPolygon``    2
            ``FEPolyhedron`` 3
            ================ ====

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> print(zone.zone_type)
            ZoneType.FEPolygon
            >>> print(zone.rank)
            2
        """
        _rank = {ZoneType.FEPolygon: 2,
                 ZoneType.FEPolyhedron: 3}
        return _rank[self.zone_type]

    @lock()
    def create_facemap(self, face_nodes, boundary_faces, boundary_connections):
        """Allocate space for the facemap.

        Parameters:
            face_nodes (`int`):  Total number of nodes for all faces. This is
                not the number of unique nodes but the total number. For
                example if a facemap defines two triangle polygons that share a
                common face, ``faces`` would be 5 and ``face_nodes`` would be
                6, not 4.
            boundary_faces (`int`): Total number of boundary faces.
            boundary_connections (`int`): Total number of boundary face
                elements or boundary face element/zone pairs.

        If the zone does not already have space allocated for a facemap, then
        this must be called before accessing it::

            >>> zone.create_facemap(400, 25, 50)
            >>> facemap = zone.facemap
        """
        if not _tecutil.DataFaceMapAlloc(self.index + 1, self.num_faces,
                                         face_nodes, boundary_faces,
                                         boundary_connections):
            raise TecplotSystemError()
        return self.facemap

    @property
    def facemap(self):
        """The connectivity `Facemap` for this polygonal finite-element zone.

        :type: `Facemap`

        Example usage::

            >>> zone = dataset.zone(0)
            >>> print(zone.facemap.num_faces)
            4500
        """
        return Facemap(self)

    @property
    def face_neighbors(self):
        """The face neighbor list for this polygonal finite-element zone.

        :type: `FaceNeighbors`

        Example usage::

            >>> zone = dataset.zone(0)
            >>> print(zone.face_neighbors.mode)
            FaceNeighborMode.LocalOneToMany
        """
        return FaceNeighbors(self)

    @inherited_property(Zone)
    def zone_type(self):
        """The `ZoneType` indicating structure of the data contained.

        :type: `ZoneType`

        The specific type of zone this object represents::

            >>> print(dataset.zone(0).zone_type)
            ZoneType.FEPolygon
        """
