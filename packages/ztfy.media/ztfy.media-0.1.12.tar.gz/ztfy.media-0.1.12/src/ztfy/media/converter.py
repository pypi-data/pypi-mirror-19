### -*- coding: utf-8 -*- ####################################################
##############################################################################
#
# Copyright (c) 2012 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################


# import standard packages
from cStringIO import StringIO
from tempfile import NamedTemporaryFile

import mimetypes

# import Zope3 interfaces

# import local interfaces
from ztfy.media.interfaces import IMediaAudioConverter, IMediaVideoConverter

# import Zope3 packages
from zope.interface import implements

# import local packages
from ztfy.media.ffbase import INPUT_BLOCK_SIZE
from ztfy.media.ffdocument import FFDocument

from ztfy.media import _


class BaseMediaConverter(object):
    """Base media converter"""

    require_temp_file = False

    def requireInputFile(self, media):
        """Check if a physical file is required to handle conversion"""
        return media.contentType == 'video/quicktime'

    def convert(self, media):
        """Convert media"""
        if self.requireInputFile(media):
            input = NamedTemporaryFile(bufsize=INPUT_BLOCK_SIZE, prefix='input_', suffix=mimetypes.guess_extension(media.contentType))
            if isinstance(media, (str, unicode)):
                input.write(media)
            else:
                input.write(media.data)
            input.file.flush()
            document = FFDocument(input.name)
        else:
            if isinstance(media, (str, unicode)):
                media = StringIO(media)
            document = FFDocument(media)
        self.addFilters(document)
        if self.require_temp_file:
            output = NamedTemporaryFile(bufsize=INPUT_BLOCK_SIZE, prefix='media_', suffix='.%s' % self.format)
            converted = document.getOutput(self.format, target=output.name)
            output.file.seek(0)
            converted['output'] = output.file.read()
            return converted
        else:
            return document.getOutput(self.format)

    def addFilters(self, document):
        pass


class BaseAudioConverter(BaseMediaConverter):
    """Base audio converter"""

    def addFilters(self, document):
        document.audiosampling(22050)
        document.audiobitrate(128)


class WavAudioConverter(BaseAudioConverter):
    """Default WAV media converter"""

    implements(IMediaAudioConverter)

    label = _("WAV audio converter")
    format = 'wav'


class Mp3AudioConverter(BaseAudioConverter):
    """Default MP3 media converter"""

    implements(IMediaAudioConverter)

    label = _("MP3 audio converter")
    format = 'mp3'
    require_temp_file = True


class OggAudioConverter(BaseAudioConverter):
    """Default OGG audio converter"""

    implements(IMediaAudioConverter)

    label = _("OGG audio converter")
    format = 'ogg'


class BaseVideoConverter(BaseMediaConverter):
    """Base video converter"""

    def addFilters(self, document):
        document.size('hd480')
        document.bitrate(1200)
        document.quantizerscale(5)
        document.audiosampling(22050)
        document.audiobitrate(128)


class FlvVideoConverter(BaseVideoConverter):
    """Default FLV media converter"""

    implements(IMediaVideoConverter)

    label = _("FLV (Flash Video) video converter")
    format = 'flv'


class Mp4VideoConverter(BaseVideoConverter):
    """Default MP4 media converter"""

    implements(IMediaVideoConverter)

    label = _("MP4 (HTML5) video converter")
    format = 'mp4'
    require_temp_file = True

    def addFilters(self, document):
        super(Mp4VideoConverter, self).addFilters(document)
        effects = document.__effects__
        effects['filter:v'] = 'setsar=1/1'
        effects['pix_fmt'] = 'yuv420p'
        effects['preset:v'] = 'slow'
        effects['profile:v'] = 'baseline'
        effects['x264-params'] = 'level=3.0:ref=1'
        effects['r:v'] = '25/1'
        effects['movflags'] = '+faststart'
        effects['strict'] = 'experimental'


class OggVideoConverter(BaseVideoConverter):
    """OGG media converter"""

    implements(IMediaVideoConverter)

    label = _("OGG video converter")
    format = 'ogg'


class WebmVideoConverter(BaseVideoConverter):
    """WebM Media converter"""

    implements(IMediaVideoConverter)

    label = _("WebM video converter")
    format = 'webm'
    require_temp_file = True

    def addFilters(self, document):
        super(WebmVideoConverter, self).addFilters(document)
        effects = document.__effects__
        effects['c:a'] = 'libvorbis'
        effects['filter:v'] = 'setsar=1/1'
        effects['pix_fmt'] = 'yuv420p'
        effects['r:v'] = '25/1'
