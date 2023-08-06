import os
import re
import shlex
from collections import defaultdict
import logging

class IncompatibleRootfsBackendError(NotImplementedError):
    pass

class LXCConfigBase(list):
    def __init__(self, lines, recursive=False):
        self[:] = (self.parse_lxc_recursive if recursive else
                   self.parse_lxc)(lines)

    @classmethod
    def from_file(cls, filename, *args, **kwargs):
        logging.debug("parsing lxc config {!r}".format(filename))
        with open(filename) as lines:
            r = cls(lines, *args, **kwargs)
            r.filename = filename
        return r

    @classmethod
    def parse_lxc(cls, lines):
        for line in lines:
            line = line.strip()
            if line.startswith("#") or not line:
                yield ('#', line)
            else:
                k, v = line.split("=", 2)
                k = k.strip()
                v = v.strip()
                yield (k, v)

    @classmethod
    def parse_lxc_recursive(cls, lines):
        for k,v in cls.parse_lxc(lines):
            if k == 'lxc.include':
                if os.path.isdir(v):
                    fs = (os.path.join(v, f) for f in sorted(os.listdir(v)))
                    fs = (f for f in fs
                          if f.endswith('.conf') and not os.path.isdir(f))
                else:
                    fs = (v,)
                for f in fs:
                    yield from cls.from_file(f)
            else:
                yield (k, v)

    def __str__(self):
        return "".join(("{1}\n" if k=='#' else "{0} = {1}\n").format(k,v)
                       for k, v in self)

_INVALID = []
class LXCConfig(LXCConfigBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dict = defaultdict(list)
        self.recompute()

    def recompute(self):
        self.dict.clear()
        for k,v in self:
            self.dict[k].append(v)

    ipv4_key_re = re.compile(r'lxc\.network\.(?:\d+\.)?ipv4')
    def get_ipv4s(self):
        for k,v in self:
            if self.ipv4_key_re.fullmatch(k):
                yield v

    ipv4_re = re.compile(r'(\d+)\.(\d+)\.(\d+)\.(\d+)/(\d+)')
    @classmethod
    def parse_ipv4(cls, s):
        m = cls.ipv4_re.match(s)
        return (tuple(int(m.group(i)) for i in range(1, 5)),
                int(m.group(5)))

    def get_id_maps(self):
        for v in self.dict.get('lxc.id_map', ()):
            t, *xs = shlex.split(v, posix=True)
            guest, host, length = map(int, xs)
            yield (t, guest, host, length)

    def get1(self, key, default=_INVALID):
        vs = self.dict.get(key, ())
        if not len(vs):
            if default is _INVALID:
                raise KeyError("{!r}".format(key))
            return default
        elif len(vs) > 1:
            raise ValueError("{!r} has more than one value: {!r}".format(key, vs))
        return vs[0]

    def del_by_key(self, key):
        for i in reversed(range(len(self))):
            if self[i][0] == key:
                del self[i]

    def del_by_predicate(self, func):
        for i in reversed(range(len(self))):
            if func(self[i][0], self[i][1]):
                del self[i]

    def get_rootfs_dir(self):
        backend = self.get1('lxc.rootfs.backend')
        if backend not in ('dir', 'btrfs', 'zfs'):
            raise UnsupportedRootfsBackendError(
                "unsupported rootfs backend {!r}".format(backend))
        return self.get1('lxc.rootfs')

