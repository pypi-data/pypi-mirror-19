# Copyright (c) 2016, Science and Technology Facilities Council
# This software is distributed under a BSD licence. See LICENSE.txt.
"""
mrcmemmap
---------

"""

# Import Python 3 features for future-proofing
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

import numpy as np

import mrcfile.utils as utils
from .mrcfile import MrcFile
from .constants import IMAGE_STACK_SPACEGROUP


class MrcMemmap(MrcFile):
    
    """TODO: docs, try using our own mmap instead of numpy memmap class
    
    """
    
#     def __init__(self, name, mode='r', **kwargs):
#         super(MrcMemmap, self).__init__(name, mode, **kwargs)
    
    def __repr__(self):
        return "MrcMemmap('{0}', mode='{1}')".format(self._iostream.name,
                                                     self._mode)
    
    def set_extended_header(self, extended_header):
        """Replace the file's extended header.
        
        Note that the file's entire data block must be moved if the extended
        header size changes. Setting a new extended header can therefore be
        very time consuming with large files, if the new extended header
        occupies a different number of bytes than the previous one.
        """
        self.check_writeable()
        if extended_header.nbytes != self._extended_header.nbytes:
            data_copy = self._data.copy()
            self._close_data()
            self._extended_header = extended_header
            self.header.nsymbt = extended_header.nbytes
            header_nbytes = self.header.nbytes + extended_header.nbytes
            self._iostream.truncate(header_nbytes + data_copy.nbytes)
            self._open_memmap(data_copy.dtype, data_copy.shape)
            np.copyto(self._data, data_copy)
        else:
            self._extended_header = extended_header
    
    def flush(self):
        """Flush the header and data arrays to the file buffer."""
        if not self._read_only:
            self._iostream.seek(0)
            self._iostream.write(self.header)
            self._iostream.write(self.extended_header)
            
            # Flushing the file before the mmap makes the mmap flush faster
            self._iostream.flush()
            self._data.flush()
            self._iostream.flush()
            
            # Seek to end so stream is left in the same position as normal
            self._iostream.seek(0, os.SEEK_END)
    
    def _read_data(self):
        """Read the data block from the file.
        
        This method first calculates the parameters needed to read the data
        (block start position, endian-ness, file mode, array shape) and then
        opens the data as a numpy memmap array.
        """
        
        mode = self.header.mode
        dtype = utils.dtype_from_mode(mode).newbyteorder(mode.dtype.byteorder)
        
        # convert data dimensions from header into array shape
        nx = self.header.nx
        ny = self.header.ny
        nz = self.header.nz
        mz = self.header.mz
        ispg = self.header.ispg
        
        if utils.spacegroup_is_volume_stack(ispg):
            shape = (nz // mz, mz, ny, nx)
        elif ispg == IMAGE_STACK_SPACEGROUP and nz == 1:
            # Use a 2D array for a single image
            shape = (ny, nx)
        else:
            shape = (nz, ny, nx)
        
        self._open_memmap(dtype, shape)
    
    def _open_memmap(self, dtype, shape):
        """Open a new memmap array pointing at the file's data block."""
        acc_mode = 'r' if self._read_only else 'r+'
        header_nbytes = self.header.nbytes + self.header.nsymbt
        
        self._iostream.flush()
        self._data = np.memmap(self._iostream,
                               dtype=dtype,
                               mode=acc_mode,
                               offset=header_nbytes,
                               shape=shape)
    
    def _close_data(self):
        """Delete the existing memmap array, if it exists.
        
        The array is flagged as read-only before deletion, so if a reference to
        it has been kept elsewhere, changes to it should no longer be able to
        change the file contents.
        """
        if self._data is not None:
            self._data.flush()
            self._data.flags.writeable = False
            self._data = None
    
    def _set_new_data(self, data):
        """Override of _set_new_data() to handle opening a new memmap and
        copying data into it."""
        file_size = self.header.nbytes + self.header.nsymbt + data.nbytes
        self._iostream.truncate(file_size)
        self._open_memmap(data.dtype, data.shape)
        np.copyto(self._data, data, casting='no')
