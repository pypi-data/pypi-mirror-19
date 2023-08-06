# -*- coding: utf-8 -*-
# =================================================================
#
# Authors: Pedro Dias <pedro.dias@ipma.pt>
#
# Copyright (c) 2016 Pedro Dias
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================
from thumbnails.bbox import LonLatBoundingBox, PixelBoundingBox
from thumbnails.image import ThumbnailImage
from thumbnails import utils, coordinates, tiles
from owslib.wms import WebMapService
from PIL import Image
import os


class ThumbnailGenerator(object):
    def __init__(self, bbox, width, height):
        if not isinstance(bbox, LonLatBoundingBox):
            msg = 'Unable to generate thumbnail, bounding box must be in latitude/longitude format.'
            raise Exception(msg)

        self.thumbnail_aspect_ratio = float(width) / float(height)
        self.width = width
        self.height = height
        self.bbox = self._validate_bbox(bbox)
        self.zoom = utils.get_zoom_level(self.bbox)
        self.bboxpx = self.bbox.to_pixels(self.zoom)
        self.tileset = None

    def _validate_bbox(self, bbox):
        return self._safe_bbox(bbox)

    def _safe_bbox(self, bbox):
        new_bbox = LonLatBoundingBox(bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax)
        if bbox.ymax > 80.0:
            new_bbox.ymax = 80.0
        if bbox.ymin < -80.0:
            new_bbox.ymin = -80.0
        if bbox.xmax > 180.0:
            new_bbox.xmax = 175.0
        if bbox.xmin < -180.0:
            new_bbox.xmin = -175.0
        return new_bbox

    def _resize_if_needed(self):
        """
        Resize the requested bounding box so it has the same aspect ratio of the
        thumbnail. This makes cropping and resizing easier later.
        """
        if self.bboxpx.aspect_ratio < self.thumbnail_aspect_ratio:
            # If the aspect ratio of the bbox is smaller we have to increase its
            # width
            center = self.bboxpx.center()
            new_width = self.thumbnail_aspect_ratio * self.bboxpx.height

            # Get the old upper left and lower right
            ul = self.bboxpx.upper_left()
            lr = self.bboxpx.lower_right()

            # Get the new upper left and lower right
            new_ul = coordinates.PixelCoordinates(
                center.x - (new_width / 2) * 1.1,
                center.y - (self.bboxpx.height / 2) * 1.1
            )
            new_lr = coordinates.PixelCoordinates(
                center.x + (new_width / 2) * 1.1,
                center.y + (self.bboxpx.height / 2) * 1.1
            )


            self.bboxpx = PixelBoundingBox.new(new_ul, new_lr, self.zoom)
            self.bbox = self.bboxpx.to_lonlat()

            # Recalculate the zoom and the pixel bounding box
            self.zoom = utils.get_zoom_level(self.bbox)
            self.bboxpx = self.bbox.to_pixels(self.zoom)

        elif self.bboxpx.aspect_ratio > self.thumbnail_aspect_ratio:
            # If the aspect ratio of the bbox is larger, it means we have to
            # increase its height, i.e., perform the same calculations that
            # are performed in the previous branch, nut noew relative to
            # the height of the bounding box
            center = self.bboxpx.center()
            new_height = self.bboxpx.width / self.thumbnail_aspect_ratio

            ul = self.bboxpx.upper_left()
            lr = self.bboxpx.lower_right()

            new_ul = coordinates.PixelCoordinates(
                center.x - (self.bboxpx.width / 2) * 1.1,
                center.y - (new_height / 2) * 1.1
            )
            new_lr = coordinates.PixelCoordinates(
                center.x + (self.bboxpx.width / 2) * 1.1,
                center.y + (new_height / 2) * 1.1
            )

            self.bboxpx = PixelBoundingBox.new(new_ul, new_lr, self.zoom)
            self.bbox = self.bboxpx.to_lonlat()

            self.zoom = utils.get_zoom_level(self.bbox)
            self.bboxpx = self.bbox.to_pixels(self.zoom)

        return self

    def _create_background(self, storage):
        self.tileset = tiles.TileSet(self.bboxpx)
        self.tileset.retrieve(storage)
        background = ThumbnailImage(self.tileset.tileset_bboxpx)

        parent_transform = self.tileset.tileset_bboxpx.upper_left()

        for tile in self.tileset.tiles.values():
            tile_transform = tile.to_pixels()
            tile_transform.x = tile_transform.x - parent_transform.x
            tile_transform.y = tile_transform.y - parent_transform.y

            background.image.paste(
                Image.open(os.path.join(storage, tile.to_filename())),
                (tile_transform.x, tile_transform.y)
            )

        return background

    def generate(self, wms_url, target, storage, **kwargs):
        """
        Generate the thumbnail for the specified WMS using the argument storage
        as a temporary file system location to store temporary files.
        """
        self._resize_if_needed()

        wms = WebMapService(
            wms_url,
            username=kwargs.pop('username', None),
            password=kwargs.pop('password', None)
        )

        # We don't check if getMap is an allowed operation because getMap is
        # already a mandatory operation for any WMS.

        img = wms.getmap(
            layers=kwargs.pop('layers', []),
            styles=kwargs.pop('styles', []),
            srs='EPSG:3857',
            bbox=tuple(self._safe_bbox(self.bbox).to_mercator().to_array()),
            size=(self.bboxpx.width, self.bboxpx.height),
            format='image/png',
            transparent=True
        )

        wms_path = os.path.join(storage, 'wms.png')
        background_path = os.path.join(storage, 'background.png')
        alpha_path = os.path.join(storage, 'alpha.png')
        final_path = os.path.join(storage, 'final.png')

        with open(wms_path, 'wb') as fp:
            fp.write(img.read())

        # Create the background
        background = self._create_background(storage)
        background.image.save(background_path)

        # Calculate the position where to put the wms image in the background
        transform = self.bboxpx.upper_left()
        transform.x -= self.tileset.tileset_bboxpx.upper_left().x
        transform.y -= self.tileset.tileset_bboxpx.upper_left().y

        # Load the WMS image and apply it to the background
        wms_image = Image.open(wms_path)
        alpha = Image.new('RGBA', background.image.size)
        alpha.paste(wms_image, (transform.x, transform.y))
        alpha.save(alpha_path)

        # Merge the alpha composite into the background
        alpha = Image.open(alpha_path)
        final = Image.alpha_composite(background.image, alpha)

        # Crop the final image using the dimensions of the original
        # wms image
        x0 = transform.x
        y0 = transform.y
        x1 = transform.x + self.bboxpx.width
        y1 = transform.y + self.bboxpx.height
        final.crop((x0, y0, x1, y1)).resize((self.width, self.height)).save(target)
