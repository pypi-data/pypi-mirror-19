import argparse
import io
import json
import logging
import os
import pkg_resources
import re
import shutil
import subprocess
from itertools import chain as ichain
from .fsutil import atomic_open_for_write_with_backup
from .subid import (parse_subugid_file, find_free_contiguous_range,
                    get_subugid_ranges_for_user, invert_ranges)
from .lxcconfig import LXCConfig
from .log_call import log_call

class IdRemap:
    '''do NOT call .finalize() before you've saved the information that
the IDs have indeed been remapped'''

    @property
    def acl_filename(self):
        return os.path.join(self.state_directory, "getfacl.dump")

    @property
    def state_filename(self):
        return os.path.join(self.state_directory, "state.json")

    def __init__(self, root, state_directory, old_idmap, new_idmap):
        self.state_directory = state_directory
        os.makedirs(state_directory, exist_ok=True)
        if os.path.exists(self.state_filename):
            with open(self.state_filename) as h:
                self.state = json.load(h)
            for k, v1 in (("root", root),
                          ("old_idmap", old_idmap),
                          ("new_idmap", new_idmap)):
                v2 = self.state[k]
                if v1 != v2:
                    logging.warning("mismatching key {!r} in state file; {!r}!={!r}"
                                    .format(k, v1, v2))
        else:
            self.state = dict(root=root,
                              old_idmap=old_idmap,
                              new_idmap=new_idmap,
                              stage="getfacl")

    def save_state(self):
        with atomic_open_for_write_with_backup(self.state_filename, 'w') as h:
            json.dump(self.state, h)

    def lxc_usernsexec_command(self, idmap):
        l = ["lxc-usernsexec"]
        necessary = False
        for t,guest,host,length in idmap:
            if guest==host:
                continue # null mapping
            l.append("-m")
            l.append("{:s}:{:d}:{:d}:{:d}".format(t,guest,host,length))
            necessary = True
        l.append("--")
        return l if necessary else []

    @staticmethod
    def get_idmap_root_uid_gid(idmap):
        r = {}
        for t,guest,host,length in idmap:
            if guest == 0 and length >= 1:
                r[t] = host
        return (r['u'], r['g'])

    def run(self):
        state = self.state
        while 1:
            stage = state['stage']
            logging.info("IdRemap at stage {!r}".format(stage))
            if   stage == 'getfacl':
                with atomic_open_for_write_with_backup(self.acl_filename, 'wb') as h:
                    log_call(logging.debug, subprocess.check_call, None,
                             self.lxc_usernsexec_command(state['old_idmap'])
                             + ["getfacl", "-n", "-R", "."], stdout=h,
                             cwd=state['root'])
                state['stage'] = 'chown-host-root'
                self.save_state()
            elif stage == 'chown-host-root':
                u0, g0 = self.get_idmap_root_uid_gid(state['new_idmap'])
                log_call(logging.debug, subprocess.check_call, None,
                         ["chown", "{:d}:{:d}".format(u0, g0),
                          "-R", state['root']])
                state['stage'] = 'setfacl'
                self.save_state()
            elif stage == 'setfacl':
                with open(self.acl_filename, "rb") as h:
                    log_call(logging.debug, subprocess.check_call, None,
                             self.lxc_usernsexec_command(state['new_idmap'])
                             + ["setfacl", "--restore=-"], stdin=h,
                             cwd=state['root'])
                state['stage'] = 'done'
                self.save_state()
            elif stage == 'done':
                break
            else:
                raise ValueError("invalid stage {!r}".format(stage))

    def finalize(self):
        shutil.rmtree(self.state_directory)

def lxc_command(name, command):
    return ["lxc-start", "-n", name, "--foreground", "--"] + command

class Main:
    LXC_CONF_PATH = "/etc/cgc1/"
    LXC_NET_PATH = "/etc/default/lxc-net"
    NET_INTERFACES_PATH = "/etc/network/interfaces"
    SUBID_ALIGN = 100000
    MAX_ID = 2**31-1
    def __init__(self):
        self.init_argparser()
        self.init_lxc_vars()
    def init_lxc_vars(self):
        self.lxcpath = subprocess.check_output(
            ["lxc-config", "lxc.lxcpath"]).decode('utf-8').rstrip('\n')
    def init_argparser(self):
        self.argparser = parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(title='subcommands', dest="subparser")
        parser.add_argument('-q', '--quiet', action='store_true',
                            help="be less verbose")
        p_cfg = subparsers.add_parser('configure')
        p_cfg.set_defaults(callback=self.cmd_configure)
        p_cfg.add_argument('-n', '--name', required=True,
                            help='LXC container name')
        p_cfg.add_argument('-t', '--type',
                            help='make LXC config use cgc config file; '
                           'this will erase most config options. "-t ." '
                           'to get the list of cgc config files')
        p_cfg.add_argument('--purge-include', action='store_true',
                            help='delete include keys and replace with appropriate '
                           'one specified in --type')
        p_cfg.add_argument('--purge-net', action='store_true',
                            help='delete all network-related keys from config '
                           'and replace with defaults')
        p_cfg.add_argument('--rootfs-purge-net', action='store_true',
                            help="replace {!r}".format(self.NET_INTERFACES_PATH))
        p_cfg.add_argument('--net-link', default="lxcbr0",
                            help='only active with --purge-net; what to '
                           'put in lxc.network.0.link')
        p_cfg.add_argument('--ipaddr',
                            help='set the ip address to '
                           'the first ip address available after this one '
                           '(e.g., "--ipaddr 10.3.0.2/16"); addresses ending '
                           'in .0 or .255 are skipped. use "auto" here to '
                           'pick one in the current subnet.')
        p_cfg.add_argument(
            '--auto-idmap', action='store_true',
            help="shorthand for '-m b:0:auto:65536'")
        p_cfg.add_argument(
            '-m', '--idmap', action='append', help=(
                'set id map; format is type:guest:host:count '
                '(where type is one of u(ser), g(roup), or b(oth)). '
                'set host=auto to find an unused range automatically'''))
        p_cfg.add_argument('--lxc-set', nargs=2, action='append',
                            help='set option in lxc config file')
        p_stp = subparsers.add_parser('setup')
        p_stp.set_defaults(callback=self.cmd_setup)
        p_stp.add_argument('--install-conf', action='store_true',
                           help="install LXC config files to {!r}".format(
                               self.LXC_CONF_PATH))
        p_stp.add_argument(
            '--install-lxc-net', action='store_true',
            help="(over)write {!r} with default config".format(self.LXC_NET_PATH))
        p_stp.add_argument(
            '--add-subids', action='store_true',
            help="look for and add a free subordinate id range by "
            "calling usermod --add-sub[ug]ids")
        p_stp.add_argument(
            '--subid-count', type=int, default=100000*1000,
            help="how many subids to add (default: %(default)d)")

    def main(self):
        parser = self.argparser
        args = parser.parse_args()
        logging.basicConfig(level=logging.INFO if args.quiet else logging.DEBUG)
        callback = getattr(args, 'callback', None)
        if not callback:
            parser.error("missing command")
        if os.getuid() != 0:
            logging.warning("this program requires root access, "
                            "did you forget to sudo?")
        args.callback(args)

    def config_path(self, name):
        return os.path.join(self.lxcpath, name, "config")
        
    def parse_all_lxc_config_recursive(self):
        d = {}
        for name in os.listdir(self.lxcpath):
            path = self.config_path(name)
            if not os.path.isdir(os.path.dirname(path)): continue
            try:
                d[path] = LXCConfig.from_file(path, recursive=True)
            except FileNotFoundError:
                pass
        return d

    def find_empty_id_range(self, lxc_configs, extra_ranges, length):
        # TODO: allow for nonmatching uid/gid
        ranges = list(extra_ranges)
        # ranges used by other lxcs are bad
        for l in lxc_configs:
            for t,guest,host,le in l.get_id_maps():
                ranges.append((host, le))
        # ranges NOT allocated to the root user are bad
        for rs in get_subugid_ranges_for_user('root'):
            ranges.extend(invert_ranges(rs, 0, self.MAX_ID))
        base, length = find_free_contiguous_range(
            ranges, length, align=self.SUBID_ALIGN)
        if base + length > self.MAX_ID:
            raise ValueError("could not find empty id range")
        return (base, length)

    def find_unused_ip(self, lxc_configs, initial_guess, subnet_size):
        # FIXME: check that subnet hasn't changed
        def next_ip(ipv4_tuple, increment=True):
            l = list(ipv4_tuple)
            for k in (3, 2, 1, 0):
                last = k==3
                l[k] = max(l[k] + (0 if last and not increment else 1),
                           2 if last else 0)
                if l[k] >= (254 if last else 256):
                    l[k] = 2 if last else 0
                else:
                    break
            return tuple(l)
        ips = set()
        for c in lxc_configs:
            ips.update(tuple(c.parse_ipv4(oip)[0]) for oip in c.get_ipv4s())
        ip = next_ip(initial_guess, increment=False)
        while ip in ips:
            ip = next_ip(ip)
        return ip

    def usage(self, *args, **kwargs):
        return self.argparser.error(*args, **kwargs)
    
    def cmd_configure(self, args):
        path = self.config_path(args.name)
        lxc = LXCConfig.from_file(path)

        def save_lxc():
            with atomic_open_for_write_with_backup(lxc.filename, 'w') as h:
                os.fchmod(h.fileno(), 0o644)
                h.write(str(lxc))

        all_lxcs = self.parse_all_lxc_config_recursive()
        other_lxcs = all_lxcs.copy()
        del other_lxcs[path]

        if args.auto_idmap:
            if args.idmap:
                self.usage("--auto-idmap and --idmap are mutually exclusive")
            args.idmap = ['b:0:auto:65536']
        idmap = args.idmap
        if args.idmap:
            idmap = [m.split(':') for m in idmap]
            extra_ranges = []
            for e in idmap: # t,guest,host,length
                t,guest,host,length = e
                e[1], e[3] = int(guest), int(length)
                if host != 'auto':
                    e[2] = int(host)
                    extra_ranges.append((host, length))
            for e in idmap:
                t,guest,host,length = e
                if host == 'auto':
                    e[2:4] = self.find_empty_id_range(
                        other_lxcs.values(), extra_ranges, length)
                    extra_ranges.append(tuple(e[2:4]))
            logging.info("new idmap {!r}".format(idmap))
            idmap = list(ichain.from_iterable(
                [(['u']+e[1:], ['g']+e[1:]) if e[0]=='b' else (e,)
                 for e in idmap]))
            old_idmap = list(map(list,lxc.get_id_maps()))
            rootfs = lxc.get_rootfs_dir()
            rootfs_parent = os.path.dirname(rootfs)
            os.chmod(rootfs_parent, 0o775)
            statedir = os.path.join(rootfs_parent, '.cgc1-idremap')
            remapper = IdRemap(rootfs, statedir, old_idmap, idmap)
            remapper.run()
            lxc.del_by_key('lxc.id_map')
            for e in idmap:
                lxc.append(('lxc.id_map', "{} {} {} {}".format(*e)))
            lxc.recompute()
            save_lxc()
            remapper.finalize()

        if args.purge_include:
            lxctype = args.type
            lxctypes = dict(self.lxc_types())
            incpath = lxctypes.get(lxctype, None)
            if incpath is None:
                self.usage("must specify --type; valid types are {!r}".format(
                    list(sorted(k for k,v in lxctypes.items()))))
            lxc.del_by_key('lxc.include')
            lxc.insert(0, ('lxc.include', incpath))
            save_lxc()

        if args.purge_net:
            if not args.ipaddr:
                self.usage("must specify --ipaddr when using --purge-net")
            lxc.del_by_predicate(lambda k,v: k.startswith('lxc.network.'))
            pre = 'lxc.network.0.'
            lxc.append((pre+'type', 'veth'))
            lxc.append((pre+'flags', 'up'))
            lxc.append((pre+'link', args.net_link))
            lxc.append((pre+'ipv4.gateway', 'auto'))
            lxc.recompute()
        
        if args.ipaddr:
            if args.ipaddr == 'auto':
                initial_guess, subnet_size = lxc.parse_ipv4(next(lxc.get_ipv4s()))
                assert subnet_size % 8 == 0 # FIXME
                ssmod8 = (subnet_size//8)
                initial_guess = initial_guess[:ssmod8] + (0,)*(4-ssmod8)
            else:
                initial_guess, subnet_size = LXCConfig.parse_ipv4(args.ipaddr)
            ip = self.find_unused_ip(other_lxcs.values(), initial_guess, subnet_size)
            lxc.del_by_predicate(lambda k,v: lxc.ipv4_key_re.fullmatch(k))
            ip_string = '{}/{}'.format('.'.join(map(str,ip)), subnet_size)
            print("IP={}".format(ip_string))
            lxc.append(('lxc.network.0.ipv4', ip_string))
            lxc.recompute()
            save_lxc()

        if args.lxc_set:
            l = args.lxc_set
            for key in set(k for k,v in l):
                lxc.del_by_key(key)
            for key, value in l:
                lxc.append((key, value))
            save_lxc()

        if args.rootfs_purge_net:
            proc = log_call(
                logging.debug, subprocess.Popen, None,
                lxc_command(args.name,
                            ['tee', self.NET_INTERFACES_PATH]),
                stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            proc.communicate(input='''\
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet manual
'''.encode('ascii'))
            logging.debug("process exited {}".format(proc.wait()))

    lxc_types_re = re.compile(r'(.+)\.type\.conf')
    def lxc_types(self):
        for k in os.listdir(self.LXC_CONF_PATH):
            m = self.lxc_types_re.fullmatch(k)
            if m:
                yield (m.group(1), os.path.join(self.LXC_CONF_PATH, k))

    def lxc_confs(self):
        d = "conf"
        for f in pkg_resources.resource_listdir(__name__, d):
            yield (f, d+'/'+f)

    def cmd_setup(self, args):
        if args.install_conf:
            os.makedirs(self.LXC_CONF_PATH, exist_ok=True)
            for f, fpath in self.lxc_confs():
                with pkg_resources.resource_stream(
                        __name__, fpath) as f_src:
                    with atomic_open_for_write_with_backup(
                            os.path.join(self.LXC_CONF_PATH, f), 'w+b') as f_dst:
                        os.fchmod(f_dst.fileno(), 0o644)
                        shutil.copyfileobj(f_src, f_dst)
        if args.add_subids:
            us, gs = (parse_subugid_file(open('/etc/sub{}id'.format(c)))
                      for c in 'ug')
            base, length = find_free_contiguous_range(
                ((b,l) for _,b,l in ichain(us, gs)),
                args.subid_count, align=self.SUBID_ALIGN)
            for c in 'ug':
                subprocess.check_call(["usermod", "--add-sub{}ids".format(c),
                                       "{:d}-{:d}".format(base, base+length-1),
                                       "root"])
        if args.install_lxc_net:
            with atomic_open_for_write_with_backup("/etc/default/lxc-net", "w") as h:
                os.fchmod(h.fileno(), 0o644)
                h.write('''\
USE_LXC_BRIDGE="true"
LXC_BRIDGE="lxcbr0"
LXC_ADDR="10.3.0.1"
LXC_NETMASK="255.255.0.0"
LXC_NETWORK="10.3.0.0/16"
# LXC_DHCP_RANGE="10.0.3.2,10.0.255.254"
# LXC_DHCP_MAX="253"
# LXC_DHCP_CONFILE=""
LXC_DOMAIN=""
''')

def main():
    Main().main()

if __name__=='__main__':
    main()
