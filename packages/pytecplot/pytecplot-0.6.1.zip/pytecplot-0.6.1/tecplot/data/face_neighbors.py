import logging

from ctypes import c_int32, c_int64, c_void_p, POINTER

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from ..tecutil import lock, log_setattr

log = logging.getLogger(__name__)


@log_setattr
class FaceNeighbors(c_void_p):
    """Face neighbor definition and control.

    Face neighbor access in PyTecplot is a work in progress. While we provide
    some functionality, it sould be considered "beta" quality at best.
    """
    def __init__(self, zone):
        self.zone = zone
        super().__init__(self._native_reference())

    @lock()
    def _native_reference(self):
        return _tecutil.DataFaceNbrGetReadableRef(self.zone.index + 1)

    def __eq__(self, other):
        self_addr = addressof(cast(self, POINTER(c_int64)).contents)
        other_addr = addressof(cast(other, POINTER(c_int64)).contents)
        return self_addr == other_addr

    def __ne__(self, other):
        return not (self == other)

    @property
    def c_type(self):
        _ctypes = {
            OffsetDataType.OffsetDataType_32Bit: c_int32,
            OffsetDataType.OffsetDataType_64Bit: c_int64}
        data_type = _tecutil.DataFaceNbrRawItemType(self)
        return _ctypes[data_type]

    @property
    def mode(self):
        """Face neighbor mode.

        :type: `FaceNeighborMode`

        Possible values: `FaceNeighborMode.LocalOneToOne`,
            `FaceNeighborMode.LocalOneToMany`,
            `FaceNeighborMode.GlobalOneToOne`,
            `FaceNeighborMode.GlobalOneToMany`.

        Example usage::

            >>> print(zone.face_neighbors.mode)
            FaceNeighborMode.LocalOneToMany
        """
        return FaceNeighborMode(_tecutil.DataFaceNbrGetModeByRef(self))

    def set_connection(element, face, neighbors, zones=None, obscure=False):
        """Connect boundary of an element's face to a neighboring face.

        This sets the boundary connection face neighbors within an open face
        neighbor assignment sequence for the specified element and face.

        Parameters:
            element (`int`): The element number (zero-based).
            face (`int`): The face number on the element (zero-based).
            neighbors (`list` of `integers <int>`): List of zero-based indices
                of the neighboring faces.
            zones (`list` of `PolyFEZone` objects, optional): List of zones for
                global neighbors. This must be the same length as
                ``neighbors``. Use `None` to indicate these are local
                neighbors. (default: `None`)
            obscure (`boolean <bool>`, optional): Indicates that the neighbors
                completely obscure the face. (default: `False`)
        """
        if __debug__:
            if zones is not None:
                if len(neighbors) != len(zones):
                    msg = 'neighbors and zones must be the same length'
                    raise TecplotLogicError(msg)
        _dispatch = {
            c_int32: _tecutil.DataFaceNbrAssignByRef,
            c_int64: _tecutil.DataFaceNbrAssignByRef64}
        int_type = self.c_type
        n = len(neighbors)
        neighbors_arr = (int_type*n)(neighbors)
        zones_arr = None if zones is None else (c_int32*n)(zones)
        if not _dispatch[int_type](self, element, face, obscure, n,
                                   neighbors_arr, zones_arr):
            raise TecplotSystemError()
