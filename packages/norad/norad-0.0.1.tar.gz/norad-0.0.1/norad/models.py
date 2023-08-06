"""
Use Python objects to abstract the Norad HTTP API.
"""
import base64

class Model(object):
    """ The base class for Norad models, like machines and organizations.
    """

    def __init__(self, http, **info):
        """ Initialize a Norad HTTP client.

        `http` is an initialized `norad.client.HttpClient`.
        `name` is an object's identifier (`id`, `slug`, etc.)
        """
        self.http = http
        self.info = info

    def __getitem__(self, name):
        """ Provide dictionary-like access to a model.
        """
        return self.info[name]

    def __contains__(self, name):
        """ Check if a name is in this object's `info`.
        """
        return name in self.info

    def __repr__(self):
        """ Display any information attached to this model.
        """
        template = '{cls}({info})'
        return template.format(cls=self.__class__.__name__, info=self.info)


class Scannable(Model):
    """ A common base class for organizations and machines.
    """

    def _list_container_configs(self, api_path):
        """ List security container configs for a machine.
        """
        template = 'machines/{name}/security_container_configs'
        path = template.format(name=self['id'])
        configs = self.http.get(api_path)
        return [SecurityContainerConfig(self.http, **config) for config in configs]

    def _create_container_config(self, api_path, container_name, settings,
                                 enabled_outside_of_requirement):
        """ Configure a security container by name (not ID).
        """
        identifier = self._find_security_container(container_name)
        if identifier is None:
            raise ValueError('No container named {0}.'.format(container_name))
        else:
            data = {
                'security_container_config': {
                    'security_container_id':identifier,
                    'enabled_outside_of_requirement': enabled_outside_of_requirement,
                    'values': settings
                }
            }
            result = self.http.post(api_path, data)
            return SecurityContainerConfig(self.http, **result)

    def _find_security_container(self, container_name):
        """ Look up a security container by ID.
        """
        # FIXME: cache list of security containers?
        containers = self.http.get('security_containers')
        for container in containers:
            full_name = container['name']
            name = full_name.rsplit('/')[-1]
            name, version = name.split(':')
            if name == container_name:
                return container['id']


class Organization(Scannable):
    """ An object to query Norad organizations.
    """

    def get(self):
        """ Fetch information about an organization.
        """
        path = 'organizations/{name}'.format(name=self['uid'])
        self.info = self.http.get(path)
        return self

    def create(self):
        """ Create a new organization.
        """
        path = 'organizations'
        data = {'organization': {'uid': self['uid']}}
        info = self.http.post(path, data)
        return Organization(self.http, **info)

    def delete(self):
        """ Delete an existing organization.
        """
        path = 'organizations/{name}'.format(name=self['uid'])
        return self.http.delete(path)

    def scan(self):
        """ Start a scan for an organization.
        """
        path = 'organizations/{name}/scan'.format(name=self['uid'])
        return self.http.post(path)

    def list_machines(self):
        """ List all machines in this organization.
        """
        path = 'organizations/{name}/machines'.format(name=self['uid'])
        result = self.http.get(path)
        return [Machine(self.http, **info) for info in result]

    def create_machine(self, ip=None, fqdn=None, description=None):
        """ Create a new machine within this organization.

        If no organization token is cached, make an initial HTTP request
        to fetch it.
        """
        if 'token' not in self:
            self.get()
        path = 'organizations/{name}/machines'.format(name=self['uid'])
        config = {'ip': ip, 'fqdn': fqdn, 'description': description}
        data = {'organization_token': self['token'], 'machine': config}
        info = self.http.post(path, data)
        return Machine(self.http, **info)

    def list_container_configs(self):
        """ List security container configs for an organization.
        """
        template = 'organizations/{name}/security_container_configs'
        path = template.format(name=self['uid'])
        return self._list_container_configs(path)

    def enable_test(self, test_name, extra_config=None, enabled_outside_of_requirement=True):
        template = 'organizations/{name}/security_container_configs'
        path = template.format(name=self['uid'])
        return self._create_container_config(path, test_name, extra_config,
                                             enabled_outside_of_requirement)

    def list_ssh_key_pairs(self):
        """ List all key pairs in this organization.
        """
        path = 'organizations/{name}/ssh_key_pairs'.format(name=self['uid'])
        result = self.http.get(path)
        return [SshKeyPair(self.http, **info) for info in result]

    def create_ssh_key_pair(self, name, username, path_to_key, description=None):
        """ Create a new SSH key pair within this organization.

        Expects a path to an SSH private key file.
        """
        path = 'organizations/{name}/ssh_key_pairs'.format(name=self['uid'])
        key = base64.encodestring(open(path_to_key, 'r').read())
        print key
        config = {'name': name, 'username': username, 'key': key, 'description': description}
        data = {'ssh_key_pair': config}
        info = self.http.post(path, data)
        return SshKeyPair(self.http, **info)


class Machine(Scannable):
    """ An object to represent a machine in Norad.
    """
    
    def get(self):
        """ Fetch information about a machine.
        """
        path = 'machines/{name}'.format(name=self['id'])
        self.info = self.http.get(path)
        return self
    
    def update(self, description):
        """ Update a machine's information.
        """
        path = 'machines/{name}'.format(name=self['id'])
        data = {'machine': {'description': description}}
        self.info = self.http.put(path, data=data)
        return self

    def delete(self):
        """ Delete a machine.
        """
        path = 'machines/{name}'.format(name=self['id'])
        return self.http.delete(path)

    def scan(self):
        """ Start a scan for a machine.
        """
        path = 'machines/{name}/scan'.format(name=self['id'])
        return self.http.post(path)

    def black_box(self, latest=False):
        """ View black-box scan data for a machine.

        If `latest` is true, limit results to the most recent scans.
        """
        path = 'machines/{name}/black_box_assessments'.format(name=self['id'])
        if latest:
            path += '/latest'
        return self.http.get(path)

    def list_container_configs(self):
        """ List security container configs for a machine.
        """
        template = 'machines/{name}/security_container_configs'
        path = template.format(name=self['id'])
        return self._list_container_configs(path)

    def enable_test(self, test_name, extra_config=None, enabled_outside_of_requirement=True):
        """ Create a security container configs for a machine.
        """
        template = 'machines/{name}/security_container_configs'
        path = template.format(name=self['id'])
        return self._create_container_config(path, test_name, extra_config,
                                             enabled_outside_of_requirement)

    def list_services(self):
        """ List all services for this machine.
        """
        path = 'machines/{id}/services'.format(id=self['id'])
        result = self.http.get(path)
        return [Service(self.http, **info) for info in result]

    def create_ssh_service(self, name, port=22, description=None, port_type='tcp', encryption_type='ssh', allow_brute_force=False):
        self._create_service(name, port, description, port_type, encryption_type, 'SshService', allow_brute_force)

    def create_web_application_service(self, name, port=80, description=None, port_type='tcp', encryption_type='cleartext', allow_brute_force=False):
        self._create_service(name, port, description, port_type, encryption_type, 'WebApplicationService', allow_brute_force)

    def create_generic_service(self, name, port, description=None, port_type='tcp', encryption_type='cleartext', allow_brute_force=False):
        self._create_service(name, port, description, port_type, encryption_type, 'GenericService', allow_brute_force)

    def ssh_key_pair(self):
        """ The key pair associated with this machine.
        """
        return SshKeyPair(None, **self['ssh_key_pair'])

    def associate_key_pair(self, keypair):
        """ Associate an SSH key pair with this machine.
        """
        path = 'machines/{id}/ssh_key_pair_assignment'.format(id=self['id'])
        config = {'ssh_key_pair_id': keypair['id']}
        info = self.http.post(path, config)
        return SshKeyPairAssignment(self.http, **info)

    def _create_service(self, name, port, description, port_type, encryption_type, type, allow_brute_force):
        """ Create a new service for this machine.
        """
        path = 'machines/{id}/services'.format(id=self['id'])
        config = {'name': name, 'port': port, 'description': description, 'port_type': port_type, 'encryption_type': encryption_type, 'type': type, 'allow_brute_force': allow_brute_force}
        data = {'service': config}
        info = self.http.post(path, data)
        return Service(self.http, **info)


class SecurityContainerConfig(Model):
    """ An object to represent a Norad security container configuration.
    """

    def delete(self):
        """ Delete a security container config by ID.
        """
        path = 'security_container_configs/{id}'.format(id=self['id'])
        return self.http.delete(path)

    def update(self, settings=None, enabled_outside_of_requirement=True):
        """ Update a security container config in-place.
        """
        data = {
            'security_container_config': {
                'values': settings,
                'enabled_outside_of_requirement': enabled_outside_of_requirement
            }
        }
        path = 'security_container_configs/{id}'.format(id=self['id'])
        result = self.http.put(path, data)
        self.info = result
        return self

class Service(Model):
    """ An object to represent a Norad service.
    """

    def delete(self):
        """ Remove a service by ID.
        """
        path = 'services/{id}'.format(id=self['id'])
        return self.http.delete(path)

class SshKeyPair(Model):
    """ An object to represent an SSH Key Pair in Norad.
    """
    def delete(self):
        """ Remove a key pair by ID.
        """
        path = 'ssh_key_pairs/{id}'.format(id=self['id'])
        return self.http.delete(path)

class SshKeyPairAssignment(Model):
    """ An object to represent an SSH Key Pair associated with a Machine in Norad.
    """
    def delete(self):
        """ Remove an association by ID.
        """
        path = 'ssh_key_pair_assignment/{id}'.format(id=self['id'])
        return self.http.delete(path)
