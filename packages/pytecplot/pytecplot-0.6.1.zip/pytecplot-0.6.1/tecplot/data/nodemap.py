import itertools as it
import logging

from ctypes import addressof, cast, c_int32, c_int64, c_void_p, POINTER

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from ..tecutil import lock, log_setattr

log = logging.getLogger(__name__)


@log_setattr
class Nodemap(c_void_p):
    """Connectivity list definition and control.

    Nodemap access in PyTecplot is a work in progress. While we provide
    some functionality, it sould be considered "beta" quality at best.
    """
    def __init__(self, zone):
        self.zone = zone
        super().__init__(self._native_reference())

    @lock()
    def _native_reference(self, writable=False):
        _dispatch = {
            True: _tecutil.DataNodeGetWritableRef,
            False: _tecutil.DataNodeGetReadableRef}
        with self.zone.dataset.frame.activated():
            return _dispatch[writable](self.zone.index + 1)

    @lock()
    def _raw_pointer(self, writable=False):
        _dispatch = {
            True: {
                c_int32: _tecutil.DataNodeGetWritableRawPtrByRef,
                c_int64: _tecutil.DataNodeGetWritableRawPtrByRef64},
            False: {
                c_int32: _tecutil.DataNodeGetReadableRawPtrByRef,
                c_int64: _tecutil.DataNodeGetReadableRawPtrByRef64}
            }
        return _dispatch[writable][self.c_type](self)

    def __eq__(self, other):
        self_addr = addressof(cast(self, POINTER(c_int64)).contents)
        other_addr = addressof(cast(other, POINTER(c_int64)).contents)
        return self_addr == other_addr

    def __ne__(self, other):
        return not (self == other)

    def __len__(self):
        return self.zone.num_elements

    def __iter__(self):
        self.current_index = -1
        self.current_length = self.size
        return self

    def __next__(self):
        self.current_index += 1
        if self.current_index < self.current_length:
            return self.__getitem__(self.current_index)
        else:
            del self.current_index
            del self.current_length
            raise StopIteration

    def next(self): # if sys.version_info < (3,)
        return self.__next__()

    @property
    def shape(self):
        return (len(self), self.points_per_element)

    @property
    def c_type(self):
        _ctypes = {
            OffsetDataType.OffsetDataType_32Bit: c_int32,
            OffsetDataType.OffsetDataType_64Bit: c_int64}
        data_type = _tecutil.DataNodeGetRawItemType(self)
        return _ctypes[data_type]

    @property
    def num_points_per_element(self):
        """Points per element for classic finite-element zones.

        :type: `integer <int>`

        The number of points (also known as nodes) per finite-element is
        determined from the ``zone_type`` parameter. The following table shows
        the number of points per element for the available zone types along
        with the resulting shape of the nodemap based on the number of points
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
            >>> print(zone.nodemap.num_points_per_element)
            3
        """
        return _tecutil.DataNodeGetNodesPerElem(self)

    def copy(self):
        #npts, nelems, _ = self.shape
        #size = (npts - 1) * nelems
        #arr = (self.c_type * size)()
        #ref = self._native_reference()
        #_tecutil.DataNodeArrayGetByRef(ref, 1, size, arr)
        #for i in range(len(arr)):
        #    arr[i] -= 1
        #nodemap_list = list(list(x) for x in zip(*([iter(arr)] * nelems)))
        #return nodemap_list
        raise TecplotNotImplementedError

    @lock()
    def __setitem__(self, nodemap):
        #_dispatch = {
        #    c_int32: DataNodeArraySetByRef,
        #    c_int64: DataNodeArraySetByRef64}
        #with self.dataset.frame.activated():
        #    npts, nelems, _ = self.shape
        #    ppe = self.num_points_per_element
        #    assert len(nodemap) == nelems
        #    assert len(nodemap[0]) == ppe
        #    size = self.num_points_per_element * nelems
        #    arr = (c_int32 * size)()
        #    for i, v in enumerate(it.chain(*nodemap)):
        #        arr[i] = v + 1
        #    ref = _tecutil.DataNodeGetWritableRef(self.index + 1)
        #    _tecutil.DataNodeArraySetByRef(ref, 1, size, arr)
        #    session.state_changed(StateChange.NodeMapsAltered)
        raise TecplotNotImplementedError
