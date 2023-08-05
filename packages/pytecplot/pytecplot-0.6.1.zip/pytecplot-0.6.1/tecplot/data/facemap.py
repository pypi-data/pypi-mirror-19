import itertools as it
import logging

from ctypes import c_int32, c_int64, c_void_p, POINTER
from textwrap import dedent

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from ..tecutil import lock, log_setattr

log = logging.getLogger(__name__)


@log_setattr
class Facemap(c_void_p):
    """Connectivity list definition and control.

    Facemap access in PyTecplot is a work in progress. While we provide
    some functionality, it sould be considered "beta" quality at best.
    """
    def __init__(self, zone):
        self.zone = zone
        super().__init__(self._native_reference())

    @lock()
    def _native_reference(self, writable=False):
        try:
            _dispatch = {
                True: _tecutil.DataFaceMapGetWritableRef,
                False: _tecutil.DataFaceMapGetReadableRef}
            with self.zone.dataset.frame.activated():
                return _dispatch[writable](self.zone.index + 1)
        except TecplotLogicError:
            raise TecplotLogicError(dedent('''\
                A facemap must first be created with
                PolyFEZone.create_facemap()'''))

    def __eq__(self, other):
        self_addr = addressof(cast(self, POINTER(c_int64)).contents)
        other_addr = addressof(cast(other, POINTER(c_int64)).contents)
        return self_addr == other_addr

    def __ne__(self, other):
        return not (self == other)

    def __len__(self):
        return self.num_faces

    @property
    def num_faces(self):
        return _tecutil.DataFaceMapGetNFaces(self)

    @property
    def node_c_type(self):
        _ctypes = {
            OffsetDataType.OffsetDataType_32Bit: c_int32,
            OffsetDataType.OffsetDataType_64Bit: c_int64}
        data_type = _tecutil.DataFaceMapGetNodeRawItemType(self)
        return _ctypes[data_type]

    @property
    def element_c_type(self):
        _ctypes = {
            OffsetDataType.OffsetDataType_32Bit: c_int32,
            OffsetDataType.OffsetDataType_64Bit: c_int64}
        data_type = _tecutil.DataFaceMapGetElementRawItemType(self)
        return _ctypes[data_type]

    @lock()
    def assign_mapping(self, facemap, elements):
        nfaces = len(facemap)
        nfacenodes = [len(n) for n in facemap]
        faces = (c_int32*nfaces)(*nfacenodes)
        nodes = (c_int32*sum(nfacenodes))(*[n+1 for n in it.chain(*facemap)])
        left_elems = (c_int32*len(elements))(*[e[0] for e in elements])
        right_elems = (c_int32*len(elements))(*[e[1] for e in elements])
        if self.zone.zone_type is ZoneType.FEPolygon:
            faces = None
            if __debug__:
                if not all(n==2 for n in nfacenodes):
                    msg = dedent('''Polygon zone facemaps must have only two
                    nodes per element.''')
                    raise TecplotLogicError(msg)
        _tecutil.DataFaceMapAssignNodes(self, nfaces, faces, nodes)
        _tecutil.DataFaceMapAssignElems(self, len(elements), left_elems, right_elems)
