#
# RGBImage.py -- Abstraction of an generic data image.
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
from ginga import trcalc
from ginga.util import io_rgb
from ginga.misc import Bunch
from ginga.BaseImage import BaseImage, ImageError, Header

import numpy

class RGBImage(BaseImage):

    def __init__(self, data_np=None, metadata=None,
                 logger=None, name=None, order=None,
                 ioclass=io_rgb.RGBFileHandler):

        BaseImage.__init__(self, data_np=data_np, metadata=metadata,
                           logger=logger, name=name)

        self.io = ioclass(self.logger)
        self._calc_order(order)
        self.hasAlpha = 'A' in self.order

    def get_slice(self, ch):
        data = self._get_data()
        return data[..., self.order.index(ch.upper())]

    def has_slice(self, ch):
        return ch.upper() in self.order

    def get_order(self):
        return self.order

    def get_order_indexes(self, cs):
        cs = cs.upper()
        return [ self.order.index(c) for c in cs ]

    def get_array(self, order):
        order = order.upper()
        if order == self.order:
            return self._get_data()
        l = [ self.get_slice(c) for c in order ]
        return numpy.dstack(l)

    def _calc_order(self, order):
        if order is not None:
            self.order = order.upper()
        else:
            # TODO; need something better here than a guess!
            depth = self.get_depth()
            if depth == 1:
                self.order = 'M'
            elif depth == 2:
                self.order = 'AM'
            elif depth == 3:
                self.order = 'RGB'
            elif depth == 4:
                self.order = 'RGBA'

    def set_data(self, data_np, order=None, **kwdargs):
        super(RGBImage, self).set_data(data_np, **kwdargs)

        self._calc_order(order)

    def set_color(self, r, g, b):
        # TODO: handle other sizes
        ch_max = 255
        red = self.get_slice('R')
        red[:] = int(ch_max * r)
        grn = self.get_slice('G')
        grn[:] = int(ch_max * g)
        blu = self.get_slice('B')
        blu[:] = int(ch_max * b)

    def load_file(self, filepath):
        kwds = Header()
        metadata = { 'header': kwds, 'path': filepath }

        # TODO: ideally we would be informed by channel order
        # in result by io_rgb
        data_np = self.io.load_file(filepath, kwds)

        self.set_data(data_np, metadata=metadata)

        if not (self.name is None):
            self.set(name=self.name)

    def save_as_file(self, filepath):
        data = self._get_data()
        hdr = self.get_header()
        self.io.save_file_as(filepath, data, hdr)

    def get_buffer(self, format, output=None):
        """Get image as a buffer in (format).
        Format should be 'jpeg', 'png', etc.
        """
        return self.io.get_buffer(self._get_data(), self.get_header(),
                                  format, output=output)

    def copy(self, astype=None):
        other = RGBImage()
        self.transfer(other, astype=astype)
        return other

    def has_alpha(self):
        order = self.get_order()
        return 'A' in order

    def insert_alpha(self, pos, alpha):
        if not self.has_alpha():
            order = list(self.order)
            l = [ self.get_slice(c) for c in order ]
            wd, ht = self.get_size()
            a = numpy.zeros((ht, wd), dtype=numpy.uint8)
            a[:] = int(alpha)
            l.insert(pos, a)
            self._data = numpy.dstack(l)
            order.insert(pos, 'A')
            self.order = ''.join(order)

    def get_scaled_cutout_wdht(self, x1, y1, x2, y2, new_wd, new_ht,
                                  method='basic'):
        newdata, (scale_x, scale_y) = trcalc.get_scaled_cutout_wdht(
            self._get_data(), x1, y1, x2, y2, new_wd, new_ht,
            interpolation=method, logger=self.logger)

        res = Bunch.Bunch(data=newdata, scale_x=scale_x, scale_y=scale_y)
        return res

    def get_scaled_cutout(self, x1, y1, x2, y2, scale_x, scale_y,
                          method='basic'):
        newdata, (scale_x, scale_y) = trcalc.get_scaled_cutout_basic(
            self._get_data(), x1, y1, x2, y2, scale_x, scale_y,
            interpolation=method, logger=self.logger)

        res = Bunch.Bunch(data=newdata, scale_x=scale_x, scale_y=scale_y)
        return res


#END
