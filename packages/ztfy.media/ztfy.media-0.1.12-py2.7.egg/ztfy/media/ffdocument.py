from ztfy.media.ffbase import FFVideoEffect, FFAudioEffect, FFmpeg
from ztfy.media.interfaces import IMediaInfo

class FFDocument(FFVideoEffect, FFAudioEffect):
    """
        audio/video document. A FFDocument describe a higer level action set
        combining several FF[Audio|Video]Effect methods. 
    """

    def __init__(self, file, metadata=None, effects={}):
        """
            x.__init__(...) initializes x; see x.__class__.__doc__ for signature
        """
        FFAudioEffect.__init__(self, file)
        FFVideoEffect.__init__(self, file, **effects)
        if not metadata:
            info = IMediaInfo(file, None)
            if info is not None:
                self.__metadata__ = info
            else:
                info = FFmpeg('avprobe').info(file)
                if info:
                    self.__metadata__ = info
                else:
                    self.__metadata__ = {}
        else:
            self.__metadata__ = metadata

    def get_stream_info(self, codec_type=None):
        """Get metadata info for given stream"""
        for stream in self.__metadata__.get('streams', ()):
            if (not codec_type) or (stream.get('codec_type') == codec_type):
                return stream

    def __tlen__(self):
        """
            return time length
        """
        stream = self.get_stream_info()
        if stream is not None:
            t = self.__timeparse__(float(stream["duration"]))
            if self.seek():
                t = t - self.seek()
            if self.duration():
                t = t - (t - self.duration())
            return t

    def __timereference__(self, reference, time):
        if isinstance(time, (str, unicode)):
            if '%' in time:
                parsed = (reference / 100.0) * int(time.split("%")[0])
            else:
                elts = time.split(':')
                if len(elts) == 3:
                    hhn, mmn, ssn = [float(i) for i in elts]
                    parsed = hhn * 3600 + mmn * 60 + ssn
                elif len(elts) == 2:
                    hhn, mmn = [float(i) for i in elts]
                    ssn = 0
                    parsed = hhn * 3600 + mmn * 60 + ssn
                else:
                    parsed = 0
        else:
            parsed = time
        return parsed

    def __timeparse__(self, time):
        if isinstance(time, (str, unicode)):
            if ':' in time:
                hh, mm, ss = [float(i) for i in time.split(":")]
                return hh * 3600 + mm * 60 + ss
        elif isinstance(time, float):
            return time

    def __clone__(self):
        return FFDocument(self.__file__, self.__metadata__.copy(), self.__effects__.copy())

    def resample(self, width=0, height=0, vstream=0):
        """Adjust video dimensions. If one dimension is specified, the re-sampling is proportional
        """
        stream = self.get_stream_info('video')
        if stream is not None:
            w, h = stream['width'], stream['height']
            if not width:
                width = int(w * (float(height) / h))
            elif not height:
                height = int(h * (float(width) / w))
            elif not width and height:
                return

        new = self.__clone__()
        if width < w:
            cropsize = (w - width) / 2
            new.crop(0, 0, cropsize, cropsize)
        elif width > w:
            padsize = (width - w) / 2
            new.pad(0, 0, padsize, padsize)
        if height < h:
            cropsize = (h - height) / 2
            new.crop(cropsize, cropsize, 0, 0)
        elif height > h:
            padsize = (height - h) / 2
            new.pad(padsize, padsize, 0, 0)
        return new

    def resize(self, width=0, height=0, vstream=0):
        """Resize video dimensions. If one dimension is specified, the re-sampling is proportional
            
        Width and height can be pixel or % (not mixable)
        """
        stream = self.get_stream_info('video')
        if stream is not None:
            w, h = stream['width'], stream['height']
            if type(width) == str or type(height) == str:
                if not width:
                    width = height = int(height.split("%")[0])
                elif not height:
                    height = width = int(width.split("%")[0])
                elif not width and height:
                    return
                elif width and height:
                    width = int(width.split("%")[0])
                    height = int(height.split("%")[0])
                size = "%sx%s" % (int(w / 100.0 * width), int(h / 100.0 * height))
            else:
                if not width:
                    width = int(w * (float(height) / h))
                elif not height:
                    height = int(h * (float(width) / w))
                elif not width and height:
                    return
                size = "%sx%s" % (width, height)
            new = self.__clone__()
            new.size(size)
            return new

    def split(self, time):
        """Return a tuple of FFDocument splitted at a specified time.

        Allowed formats: %, sec, hh:mm:ss.mmm
        """
        stream = self.get_stream_info()
        if stream is not None:
            sectime = self.__timeparse__(stream["duration"])
            if self.duration():
                sectime = sectime - (sectime - self.duration())
            if self.seek():
                sectime = sectime - self.seek()
            cut = self.__timereference__(sectime, time)

            first = self.__clone__()
            second = self.__clone__()
            first.duration(cut)
            second.seek(cut + 0.001)
            return first, second

    def ltrim(self, time):
        """Trim leftmost side (from start) of the clip"""
        stream = self.get_stream_info()
        if stream is not None:
            sectime = self.__timeparse__(stream["duration"])
            if self.duration():
                sectime = sectime - (sectime - self.duration())
            if self.seek():
                sectime = sectime - self.seek()
            trim = self.__timereference__(sectime, time)
            new = self.__clone__()
            if self.seek():
                new.seek(self.seek() + trim)
            else:
                new.seek(trim)
            return new

    def rtrim(self, time):
        """Trim rightmost side (from end) of the clip"""
        stream = self.get_stream_info()
        if stream is not None:
            sectime = self.__timeparse__(self.__metadata__["duration"])
            if self.duration():
                sectime = sectime - (sectime - self.duration())
            if self.seek():
                sectime = sectime - self.seek()
            trim = self.__timereference__(sectime, time)
            new = self.__clone__()
            new.duration(trim)
            return new

    def trim(self, left, right):
        """Left and right trim (actually calls ltrim and rtrim)"""
        return self.__clone__().ltrim(left).rtrim(right)

    def chainto(self, ffdoc):
        """Prepare to append at the end of another movie clip"""
        offset = 0
        if ffdoc.seek():
            offset = ffdoc.seek()
        if ffdoc.duration():
            offset = offset + ffdoc.seek()
        if ffdoc.offset():
            offset = offset + ffdoc.offset()

        new = self.__clone__()
        new.offset(offset)
        return new

    #TODO: more and more effects!!!
