### -*- coding: utf-8 -*- ####################################################
##############################################################################
#
# Copyright (c) 2012 Thierry Florac <tflorac AT ulthar.net>
# Based on wffmpeg
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

# import standard library
import json
import logging
logger = logging.getLogger('ztfy.media')

import mimetypes
import re
import tempfile

from os.path import dirname, basename
from os import sep, remove
from subprocess import Popen, PIPE

# import interfaces
from zope.app.file.interfaces import IFile

# import packages
from ztfy.extfile import getMagicContentType
from ztfy.media.ffexception import FFException

__all__ = ['FFmpeg', 'FFVideoEffect', 'FFAudioEffect']


INPUT_BLOCK_SIZE = 1024 ** 2


class FFmpeg(object):
    """
    FFmpeg Wrapper
    """

    # thanks to pyxcoder http://code.google.com/p/pyxcoder for
    # the main idea
    re_mainline = re.compile("^\s*Input #(\d+?), (.*?), from \'(.*?)\':$")
    re_infoline = re.compile("^\s*Duration: (.*?), start: 0\.000000, bitrate: (\d+?) kb\/s$")
    re_videoline = re.compile("^\s*Stream #(\d+:\d+?)\(?([A-Za-z]*)\)?: Video: (.*?), (.*?), (.*?), (.*?)$")
    re_audioline = re.compile("^\s*Stream #(\d+:\d+?)\(?([A-Za-z]*)\)?: Audio: (.*?), (\d+?) Hz, (.*?), (.*?), (\d+?) kb\/s$")

    def __init__(self, cmd="avconv"):
        self.__ffmpeg__ = cmd

    def __exec__(self, *args, **kwargs):
        """Build and execute a command line"""

        def createTempFile(arg):
            suffix = '.tmp'
            if IFile.providedBy(arg):
                # IFile object
                content_type = getMagicContentType(arg.data)
                if content_type:
                    suffix = mimetypes.guess_extension(content_type) or suffix
                output = tempfile.NamedTemporaryFile(prefix='media_', suffix=suffix)
                output.write(arg.data)
            elif hasattr(arg, 'read'):  # StringIO or any file like object
                # file-like object
                arg.reset()
                content_type = getMagicContentType(arg.read())
                if content_type:
                    suffix = mimetypes.guess_extension(content_type) or suffix
                output = tempfile.NamedTemporaryFile(prefix='media_', suffix=suffix)
                try:
                    arg.reset()
                except:
                    pass
                data = arg.read(INPUT_BLOCK_SIZE)
                while data:
                    output.write(data)
                    data = arg.read(INPUT_BLOCK_SIZE)
            else:
                # string or bytes
                content_type = getMagicContentType(arg)
                if content_type:
                    suffix = mimetypes.guess_extension(content_type) or suffix
                output = tempfile.NamedTemporaryFile(prefix='media_', suffix=suffix)
                output.write(arg)
            output.file.flush()
            return output

        cmdline = [self.__ffmpeg__]
        if self.__ffmpeg__ == 'avconv':
            cmdline.extend(['-y', '-loglevel', 'error'])
        allow_stdin = kwargs.get('allow_stdin', True)
        use_stdin = None
        for arg in args:
            if IFile.providedBy(arg):
                if len(args) == 2:
                    # FFmpeg can't get media info from an input pipe
                    # We have to write media content to temporary file
                    output = createTempFile(arg)
                    cmdline.append(output.name)
                else:
                    if allow_stdin:
                        use_stdin = arg
                        cmdline.append('-')
                    else:
                        output = createTempFile(arg)
                        cmdline.append(output.name)
            elif hasattr(arg, 'read'):  # StringIO or any file like object
                if len(args) == 2:
                    # FFmpeg can't get media info from an input pipe
                    # We have to write media content to temporary file
                    output = createTempFile(arg)
                    cmdline.append(output.name)
                else:
                    if allow_stdin:
                        use_stdin = arg
                        cmdline.append('-')
                    else:
                        output = createTempFile(arg)
                        cmdline.append(output.name)
            else:
                cmdline.append(arg)
        logger.warning("Running libAV command line: {0}".format(cmdline))
        p = Popen(cmdline, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        if use_stdin is not None:
            if IFile.providedBy(use_stdin):
                stdout, stderr = p.communicate(use_stdin.data)
            else:
                use_stdin.reset()
                stdout, stderr = p.communicate(use_stdin.read())
            if 'partial file' in stderr:
                # the video file can't be converted through pipe...
                logger.debug("Can't use piped conversion. Switch to temporary file...")
                return self.__exec__(*args, allow_stdin=False)
        else:
            stdout, stderr = p.communicate()
        if stderr:
            logger.warning("Error on libAV command line: {0}".format(cmdline))
            logger.warning(stderr)
        return stdout, stderr

    def render(self, effectchain, output):
        """Create a new file by chaining audio/video effects"""
        inputs = []
        cmds = [[]]
        outputs = []
        # we want to operate on more objects that use the same file
        # source, So, we have to split the effect chain in various
        # intermediate jobs, then rebuild all
        for index, effect in enumerate(effectchain):
            if index == 1 and not effect in inputs:
                inputs.append(effect)
                cmds[len(cmds)-1].append(effect)
            else:
                outputs.append("%s%s%s-%s" % (dirname(output), sep, len(cmds), basename(output)))
                cmds.append([])
                input = []
        # prcessing intermediate outputs
        for index, output in enumerate(outputs):
            cmd = ["-y", ]
            cmd.extend(inputs[index].cmdline())
            cmd.append(output)
            self.__exec__(*cmd)
        # procesing final output
        cmd = ["-y", ]
        for index, output in enumerate(outputs):
            doc = FFEffect(output)
            if index == 0 and inputs[index].offset():
                doc.offset(inputs[index].offset())
            cmd.extend(doc.cmdline())
        cmd.append(output)
        self.__exec__(*cmd)
        # removing intermediate outputs
        for tmp in outputs:
            remove(tmp)

    def info(self, input):
        """Retrieve file information parsing command output"""
        metadata = []
        if IFile.providedBy(input) or isinstance(input, (str, unicode)) or hasattr(input, 'read'):
            input = [input, ]
        if self.__ffmpeg__ == 'avconv':
            for i in range(0, len(input) * 2, 2):
                input.insert(i, "-i")
        if self.__ffmpeg__ == 'avprobe':
            input.extend(['-show_format', '-show_streams', '-of', 'json'])
            probe = self.__exec__(*input)[0]  # stdout
            try:
                metadata = json.loads(probe.decode())
            except UnicodeDecodeError:
                metadata = json.loads(probe.decode('utf-8'))
        else:
            lines = self.__exec__(*input)[1] # stderr
            for line in lines.split('\n'):
                if isinstance(line, str):
                    try:
                        line = line.decode()
                    except UnicodeDecodeError:
                        logger.debug("Unicode decode error: {0}".format(line))
                        continue
                if FFmpeg.re_mainline.match(line):
                    clip, vtype, filename = FFmpeg.re_mainline.match(line).groups()
                    metadata.append({"vtype": vtype, "filename": filename, "video": [], "audio": []})
                elif FFmpeg.re_infoline.match(line):
                    current = len(metadata) - 1
                    metadata[current]["duration"], metadata[current]["bitrate"] = FFmpeg.re_infoline.match(line).groups()
                elif FFmpeg.re_audioline.match(line):
                    clip, lang, codec, freq, chan, freqbit, bitrate = FFmpeg.re_audioline.match(line).groups()
                    audiostream = {"codec": codec, "lang": lang, "freq": freq, "chan": chan, "freqbit": freqbit, "bitrate": bitrate}
                    metadata[len(metadata) - 1]["audio"].append(audiostream)
                elif FFmpeg.re_videoline.match(line):
                    clip, lang, codec, pix_fmt, size, framerate = FFmpeg.re_videoline.match(line).groups()
                    size = size.split(" ")
                    videostream = {"codec": codec, "lang": lang, "pix_fmt": pix_fmt, "size": size, "framerate": framerate}
                    metadata[len(metadata) - 1]["video"].append(videostream)
        return metadata


class FFEffect:
    """
        effect for a specified input file
        each "set" method has an unset_* method 
        to clear the effect of the former (e.g.
        crop() and unset_crop() ), and a general
        unset() method 
    """

    def __init__(self, inputfile, **args):
        self.__file__ = inputfile
        for opt in args.keys():
            if not opt in ["b", "vframes", "r", "s", "aspect", "croptop",
                            "cropbottom", "cropleft", "cropright", "padtop",
                            "padbottom", "padleft", "padright", "padcolor",
                            "vn", "bt", "maxrate", "minrate", "bufsize",
                            "vcodec", "sameq", "pass", "newvideo", "pix_fmt",
                            "sws_flag", "g", "intra", "vdt", "qscale",
                            "qmin", "qmax", "qdiff", "qblur", "qcomp", "lmin",
                            "lmax", "mblmin", "mblmax", "rc_init_cplx",
                            "b_qfactor", "i_qfactor", "b_qoffset",
                            "i_qoffset", "rc_eq", "rc_override", "me_method",
                            "dct_algo", "idct_algo", "er", "ec", "bf", "mbd",
                            "4mv", "part", "bug", "strict", "aic", "umv",
                            "deinterlace", "ilme", "psnr", "vhook", "top",
                            "dc", "vtag", "vbsf", "aframes", "ar", "ab", "ac",
                            "an", "acodec", "newaudio", "alang", "t",
                            "itsoffset", "ss", "dframes"]:
                raise FFException("Error parsing option: %s" % opt)
        self.__effects__ = args
        self.__default__ = self.__effects__.copy()

    def cmdline(self):
        """ return a list of arguments """
        cmd = ["-i", self.__file__]
        for opt, value in self.__effects__.items():
            cmd.append("-%s" % opt)
            if value is not True:
                cmd.append("%s" % value)
        return cmd

    def getOutput(self, format=None, target='-'):
        if (format is None) and hasattr(self, '__metadata__'):
            format = self.__metadata__.get('vtype')
        cmdline = self.cmdline() + ['-f', format, target]
        stdout, stderr = FFmpeg().__exec__(*cmdline)
        return {'output': stdout,
                'errors': stderr,
                'cmdline': ' '.join(map(str, cmdline))}

    def restore(self):
        """
            restore initial settings
        """
        self.__effects__ = self.__default__.copy()

    def unset(self):
        """
            clear settings
        """
        self.__effects__ = {}

    def duration(self, t=None):
        """ restrict transcode sequence to duration specified """
        if t:
            self.__effects__["t"] = float(t)
        return self.__effects__.get("t")

    def unset_duration(self):
        del self.__effects__["duration"]

    def seek(self, ss=None):
        """ seek to time position in seconds """
        if ss:
            self.__effects__["ss"] = float(ss)
        return self.__effects__.get("ss")

    def unset_seek(self):
        del self.__effects__["ss"]

    def offset(self, itsoffset=None):
        """ Set the input time offset in seconds """
        if itsoffset:
            self.__effects__["itsoffset"] = itsoffset
        return self.__effects__.get("itsoffset")

    def unset_offset(self):
        del self.__effects__["itsoffset"]

    def dframes(self, dframes=None):
        """ number of data frames to record """
        if dframes:
            self.__effects__["dframes"] = dframes
        return self.__effects__.get("dframes")

    def unset_dframes(self):
        del self.__effects__["dframes"]


class FFVideoEffect(FFEffect):
    """
        video effect
    """

    def __init__(self, inputfile=None, **args):
        FFEffect.__init__(self, inputfile, **args)

    def bitrate(self, b=None):
        """ set video bitrate """
        if b:
            self.__effects__["b:v"] = "%sk" % int(b)
        return self.__effects__.get("b:v")

    def unset_bitrate(self):
        del self.__effects__["b:v"]

    def vframes(self, vframes=None):
        """ set number of video frames to record """
        if vframes:
            self.__effects__["vframes"] = int(vframes)
        return self.__effects__.get("vframes")

    def unset_vframes(self):
        del self.__effects__["vframes"]

    def rate(self, r=None):
        """ set frame rate """
        if r:
            self.__effects__["r"] = int(r)
        return self.__effects__.get("r")

    def unset_rate(self):
        del self.__effects__["r"]

    def size(self, s=None):
        """ set frame size """
        if s in ["sqcif", "qcif", "cif", "4cif", "qqvga", "qvga", "vga", "svga",
                "xga", "uxga", "qxga", "sxga", "qsxga", "hsxga", "wvga", "wxga",
                "wsxga", "wuxga", "wqxga", "wqsxga", "wquxga", "whsxga",
                "whuxga", "cga", "ega", "hd480", "hd720", "hd1080"]:
            self.__effects__["s"] = s
        elif s:
            wh = s.split("x")
            if len(wh) == 2 and int(wh[0]) and int(wh[1]):
                self.__effects__["s"] = s
            else:
                raise FFException("Error parsing option: size")
        return self.__effects__.get("s")

    def unset_size(self):
        del  self.__effects__["s"]

    def aspect(self, aspect=None):
        """ set aspect ratio """
        if aspect:
            self.__effects__["aspect"] = aspect
        return self.__effects__.get("aspect")

    def unset_aspect(self):
        del self.__effects__["aspect"]

    def crop(self, top=0, bottom=0, left=0, right=0):
        """ set the crop size """
        if top % 2:
            top = top - 1
        if bottom % 2:
            bottom = bottom - 1
        if left % 2:
            left = left - 1
        if right % 2:
            right = right - 1
        if top:
            self.__effects__["croptop"] = top
        if bottom:
            self.__effects__["cropbottom"] = bottom
        if left:
            self.__effects__["cropleft"] = left
        if right:
            self.__effects__["cropright"] = right
        return self.__effects__.get("croptop"), self.__effects__.get("cropbottom"), self.__effects__.get("cropleft"), self.__effects__.get("cropright")

    def unset_crop(self):
        del self.__effects__["croptop"]
        del self.__effects__["cropbottom"]
        del self.__effects__["cropleft"]
        del self.__effects__["cropright"]

    def pad(self, top=0, bottom=0, left=0, right=0, color="000000"):
        """ set the pad band size and color as hex value """
        if top:
            self.__effects__["padtop"] = top
        if bottom:
            self.__effects__["padbottom"] = bottom
        if left:
            self.__effects__["padleft"] = left
        if right:
            self.__effects__["padright"] = right
        if color:
            self.__effects__["padcolor"] = color
        return self.__effects__.get("padtop"), self.__effects__.get("padbottom"), self.__effects__.get("padleft"), self.__effects__.get("padright"), self.__effects__.get("padcolor")

    def unset_pad(self):
        del self.__effects__["padtop"]
        del self.__effects__["padbottom"]
        del self.__effects__["padleft"]
        del self.__effects__["padright"]

    def vn(self):
        """ disable video recording """
        self.__effects__["vn"] = True

    def unset_vn(self):
        del self.__effects__["vn"]

    def bitratetolerance(self, bt=None):
        """ set bitrate tolerance """
        if bt:
            self.__effects__["bt"] = "%sk" % int(bt)
        return self.__effects__.get("bt")

    def unset_bitratetolerance(self):
        del self.__effects__["bt"]

    def bitraterange(self, minrate=None, maxrate=None):
        """ set min/max bitrate (bit/s) """
        if minrate or maxrate and not self.__effects__["bufsize"]:
            self.__effects__["bufsize"] = 4096
        if minrate:
            self.__effects__["minrate"] = minrate
        if maxrate:
            self.__effects__["maxrate"] = maxrate

        return self.__effects__.get("minrate"), self.__effects__.get("maxrate")

    def unset_bitraterange(self):
        del self.__effects__["maxrate"]
        del self.__effects__["minrate"]

    def bufsize(self, bufsize=4096):
        """ set buffer size (bits) """
        self.__effects__["bufsize"] = int(bufsize)
        return self.__effects__["bufsize"]

    def unset_bufsize(self):
        del self.__effects__["bufsize"]

    def vcodec(self, vcodec="copy"):
        """ set video codec """
        self.__effects__["vcodec"] = vcodec
        return self.__effects__["vcodec"]

    def unset_vcodec(self):
        del self.__effects__["vcodec"]

    def sameq(self):
        """ use same video quality as source """
        self.__effects__["sameq"] = True

    def unset_sameq(self):
        del self.__effects__["sameq"]

    def passenc(self, p=1):
        """ select pass number (1 or 2)"""
        self.__effects__["pass"] = (int(p) % 3 + 1) % 2 + 1 #!!!
        return self.__effects__["pass"]

    def unset_passenc(self):
        del self.__effects__["pass"]

    def pixelformat(self, p=None):
        """ set pixelformat """
        if p:
            self.__effects__["pix_fmt"] = p
        return self.__effects__.get("pix_fmt")

    def unset_pixelformat(self):
        del self.__effects__["pix_fmt"]

    #TODO: sws_flag

    def picturesize(self, gop=None):
        """ set of group pictures size """
        if gop:
            self.__effects__["gop"] = int(gop)
        return self.__effects__.get("gop")

    def unset_picturesize(self):
        del self.__effects__["gop"]

    def intra(self):
        """ use only intra frames """
        self.__effects__["intra"] = True

    def unset_intra(self):
        del self.__effects__["intra"]

    def vdthreshold(self, vdt=None):
        """ discard threshold """
        if vdt:
            self.__effects__["vdt"] = int(vdt)
        return self.__effects__.get("vdt")

    def unset_vdthreshold(self):
        del self.__effects__["vdt"]

    def quantizerscale(self, qscale=None):
        """ Fixed quantizer scale """
        if qscale:
            self.__effects__["qscale"] = int(qscale)
        return self.__effects__.get("qscale")

    def unset_quantizerscale(self):
        del self.__effects__["qscale"]

    def quantizerrange(self, qmin=None, qmax=None, qdiff=None):
        """ define min/max quantizer scale """
        if qdiff:
            self.__effects__["qdiff"] = int(qdiff)
        else:
            if qmin:
                self.__effects__["qmin"] = int(qmin)
            if qmax:
                self.__effects__["qmax"] = int(qmax)
        return self.__effects__.get("qmin"), self.__effects__.get("qmax"), self.__effects__.get("qdiff"),

    def unset_quantizerrange(self):
        del self.__effects__["qdiff"]

    def quantizerblur(self, qblur=None):
        """ video quantizer scale blur """
        if qblur:
            self.__effects__["qblur"] = float(qblur)
        return self.__effects__.get("qblur")

    def unset_quantizerblur(self):
        del self.__effects__["qblur"]

    def quantizercompression(self, qcomp=0.5):
        """ video quantizer scale compression """
        self.__effects__["qcomp"] = float(qcomp)
        return self.__effects__["qcomp"]

    def unset_quantizercompression(self):
        del self.__effects__["qcomp"]

    def lagrangefactor(self, lmin=None, lmax=None):
        """ min/max lagrange factor """
        if lmin:
            self.__effects__["lmin"] = int(lmin)
        if lmax:
            self.__effects__["lmax"] = int(lmax)
        return self.__effects__.get("lmin"), self.__effects__.get("lmax")

    def unset_lagrangefactor(self):
        del self.__effects__["lmin"]
        del self.__effects__["lmax"]

    def macroblock(self, mblmin=None, mblmax=None):
        """ min/max macroblock scale """
        if mblmin:
            self.__effects__["mblmin"] = int(mblmin)
        if mblmax:
            self.__effects__["mblmax"] = int(mblmax)
        return self.__effects__.get("mblmin"), self.__effects__.get("mblmax")

    def unset_macroblock(self):
        del self.__effects__["mblmin"]
        del self.__effects__["mblmax"]

    #TODO: read man pages !


class FFAudioEffect(FFEffect):
    """
        Audio effect
    """

    def __init__(self, inputfile, **args):
        FFEffect.__init__(self, inputfile, **args)

    def aframes(self, aframes=None):
        """ set number of audio frames to record """
        if aframes:
            self.__effects__["aframes"] = int(aframes)
        return self.__effects__.get("aframes")

    def unset_aframes(self):
        del self.__effects__["aframes"]

    def audiosampling(self, ar=44100):
        """ set audio sampling frequency (Hz)"""
        self.__effects__["ar"] = int(ar)
        return self.__effects__["ar"]

    def unset_audiosampling(self):
        del self.__effects__["ar"]

    def audiobitrate(self, ab=64):
        """ set audio bitrate (kbit/s)"""
        self.__effects__["b:a"] = "%sk" % int(ab)
        return self.__effects__["b:a"]

    def unset_audiobitrate(self):
        del self.__effects__["b:a"]

    def audiochannels(self, ac=1):
        """ set number of audio channels """
        self.__effects__["ac"] = int(ac)
        return self.__effects__["ac"]

    def unset_audiochannels(self):
        del self.__effects__["ac"]

    def audiorecording(self):
        """ disable audio recording """
        self.__effects__["an"] = True

    def unset_audiorecording(self):
        del self.__effects__["an"]

    def acodec(self, acodec="copy"):
        """ select audio codec """
        self.__effects__["acodec"] = acodec
        return self.__effects__["acodec"]

    def unset_acodec(self):
        del self.__effects__["acodec"]

    def newaudio(self):
        """ add new audio track """
        self.__effects__["newaudio"] = True

    def unset_newaudio(self):
        del self.__effects__["newaudio"]
