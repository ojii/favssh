# -*- coding: utf-8 -*-
import os


class Host(object):
    def __init__(self, name, configuration, start=None, end=None):
        self.name = name
        self.configuration = configuration
        self.start = start
        self.end = end
    
    def __str__(self):
        return ''.join(self.get_lines())
        
    def update(self, key, value):
        self.configuration[key.lower()] = value
    
    def get_lines(self):
        lines = ['Host %s\n' % self.name]
        for key, value in sorted(self.configuration.items()):
            lines.append('    %s %s\n' % (key, value))
        return lines


class Configuration(object):
    def __init__(self, path):
        self.path = path
        self.hosts = {}
        self.delete_cache = []
        self.lines = []
        if os.path.exists(self.path):
            self.read()
    
    @classmethod
    def from_argument(cls, path):
        return cls(os.path.expanduser(path))
            
    def read(self):
        with open(self.path) as fobj:
            current_host = None
            current_host_start = 0
            current_config = {}
            # strip whitespace and remove empty lines
            for index, line in enumerate(fobj.readlines()):
                self.lines.append(line)
                line = line.strip()
                # comment
                if line.startswith('#'):
                    continue
                # comment
                elif not line:
                    continue
                # key = value style
                elif '=' in line:
                    key, value = map(str.strip, line.split('=', 1))
                # key value style
                else:
                    key, value = map(str.strip, line.split(' ', 1))
                # lower keys
                key = key.lower()
                # it's a host!
                if key == 'host':
                    if current_host:
                        host = Host(current_host, current_config, current_host_start, index)
                        self.hosts[current_host] = host
                    current_config = {}
                    current_host_start = index
                    current_host = value
                # it's a random other config!
                else:
                    current_config[key] = value
            if current_host:
                host = Host(current_host, current_config, current_host_start, index + 1)
                self.hosts[current_host] = host
    
    def all_hosts(self):
        return sorted(self.hosts.values(), key=lambda obj: getattr(obj, 'name'))
    
    def add_host(self, host, **config):
        if host in self.hosts:
            raise Exception("Host %r is already in config, use favssh update")
        else:
            self.hosts[host] = Host(host, config)
    
    def update_host(self, host, key, value):
        if host in self.hosts:
            self.hosts[host].update(key, value)
        else:
            raise Exception('Host %r is not in config, use favssh add' % host)
    
    def remove_host(self, host):
        if host in self.hosts:
            self.delete_cache.append((self.hosts[host].start, self.hosts[host].end))
            del self.hosts[host]
        else:
            raise Exception('Host %r is not in config' % host)
    
    def write(self):
        lines = list(self.lines)
        def write_host(host):
            if host.start:
                lines[host.start:host.end] = host.get_lines()
            else:
                for line in host.get_lines():
                    lines.append(line)
        def remove_host(start, end):
            lines[start:end] = []
        mutations = []
        for host in self.hosts.values():
            mutations.append((host.start, write_host, (host,)))
        for start, end in self.delete_cache:
            mutations.append((start, remove_host, (start, end)))
        for _, action, args in sorted(mutations, reverse=True):
            action(*args)
        with open(self.path, 'w') as fobj:
            fobj.writelines(lines)
