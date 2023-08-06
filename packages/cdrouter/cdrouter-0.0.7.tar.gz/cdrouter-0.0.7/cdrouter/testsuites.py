#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Testsuites."""

from marshmallow import Schema, fields, post_load

class Group(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.index = kwargs.get('index', None)
        self.test_count = kwargs.get('test_count', None)
        self.modules = kwargs.get('modules', None)

class GroupSchema(Schema):
    id = fields.Int(missing=None)
    name = fields.Str()
    index = fields.Int()
    test_count = fields.Int()
    modules = fields.List(fields.Str())

    @post_load
    def post_load(self, data):
        return Group(**data)

class Module(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.index = kwargs.get('index', None)
        self.group = kwargs.get('group', None)
        self.description = kwargs.get('description', None)
        self.test_count = kwargs.get('test_count', None)
        self.tests = kwargs.get('tests', None)
        self.labels = kwargs.get('labels', None)
        self.aliases = kwargs.get('aliases', None)

class ModuleSchema(Schema):
    id = fields.Int(missing=None)
    name = fields.Str()
    index = fields.Int()
    group = fields.Str()
    description = fields.Str()
    test_count = fields.Int()
    tests = fields.List(fields.Str())
    labels = fields.List(fields.Str())
    aliases = fields.List(fields.Str())

    @post_load
    def post_load(self, data):
        return Module(**data)

class Test(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.index = kwargs.get('index', None)
        self.group = kwargs.get('group', None)
        self.module = kwargs.get('module', None)
        self.synopsis = kwargs.get('synopsis', None)
        self.description = kwargs.get('description', None)
        self.labels = kwargs.get('labels', None)
        self.aliases = kwargs.get('aliases', None)
        self.testvars = kwargs.get('testvars', None)

class TestSchema(Schema):
    id = fields.Int(missing=None)
    name = fields.Str()
    index = fields.Int()
    group = fields.Str()
    module = fields.Str()
    synopsis = fields.Str()
    description = fields.Str()
    labels = fields.List(fields.Str())
    aliases = fields.List(fields.Str())
    testvars = fields.List(fields.Str())

    @post_load
    def post_load(self, data):
        return Test(**data)

class Label(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.index = kwargs.get('index', None)
        self.reason = kwargs.get('reason', None)
        self.description = kwargs.get('description', None)
        self.modules = kwargs.get('modules', None)
        self.tests = kwargs.get('tests', None)

class LabelSchema(Schema):
    id = fields.Int(missing=None)
    name = fields.Str()
    index = fields.Int()
    reason = fields.Str()
    description = fields.Str()
    modules = fields.List(fields.Str())
    tests = fields.List(fields.Str())

    @post_load
    def post_load(self, data):
        return Label(**data)

class Error(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.index = kwargs.get('index', None)
        self.description = kwargs.get('description', None)

class ErrorSchema(Schema):
    id = fields.Int(missing=None)
    name = fields.Str()
    index = fields.Int()
    description = fields.Str()

    @post_load
    def post_load(self, data):
        return Error(**data)

class Testvar(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.index = kwargs.get('index', None)
        self.humanname = kwargs.get('humanname', None)
        self.display = kwargs.get('display', None)
        self.dataclass = kwargs.get('dataclass', None)
        self.addedin = kwargs.get('addedin', None)
        self.deprecatedin = kwargs.get('deprecatedin', None)
        self.obsoletedin = kwargs.get('obsoletedin', None)
        self.min = kwargs.get('min', None)
        self.max = kwargs.get('max', None)
        self.length = kwargs.get('length', None)
        self.description = kwargs.get('description', None)
        self.default = kwargs.get('default', None)
        self.defaultdisabled = kwargs.get('defaultdisabled', None)
        self.dyndefault = kwargs.get('dyndefault', None)
        self.keywords = kwargs.get('keywords', None)
        self.alsoaccept = kwargs.get('alsoaccept', None)
        self.wildcard = kwargs.get('wildcard', None)
        self.instances = kwargs.get('instances', None)
        self.parent = kwargs.get('parent', None)
        self.children = kwargs.get('children', None)
        self.tests = kwargs.get('tests', None)

class TestvarSchema(Schema):
    id = fields.Int(missing=None)
    name = fields.Str()
    index = fields.Int()
    humanname = fields.Str()
    display = fields.Str()
    dataclass = fields.Str()
    addedin = fields.Str()
    deprecatedin = fields.Str()
    obsoletedin = fields.Str()
    min = fields.Str()
    max = fields.Str()
    length = fields.Str()
    description = fields.Str()
    default = fields.Str()
    defaultdisabled = fields.Bool()
    dyndefault = fields.Bool()
    keywords = fields.List(fields.Str())
    alsoaccept = fields.List(fields.Str())
    wildcard = fields.Bool()
    instances = fields.Int()
    parent = fields.Str()
    children = fields.List(fields.Str())
    tests = fields.List(fields.Str())

    @post_load
    def post_load(self, data):
        return Testvar(**data)

class TestsuitesService(object):
    """Service for accessing CDRouter Testsuites."""

    RESOURCE = 'testsuites'
    BASE = '/' + RESOURCE + '/1/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def info(self):
        """Get testsuite info."""
        return self.service.get(self.base)

    def search(self, query):
        """Perform full text search of testsuite."""
        return self.service.get(self.base+'search/', params={'q': query})

    def list_groups(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        """Get a list of groups."""
        schema = GroupSchema()
        resp = self.service.list(self.base+'groups/', filter, sort)
        return self.service.decode(schema, resp, many=True)

    def get_group(self, name):
        """Get a group."""
        schema = GroupSchema()
        resp = self.service.get(self.base+'tests/'+name+'/')
        return self.service.decode(schema, resp)

    def list_modules(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        """Get a list of modules."""
        schema = ModuleSchema(exclude=('index', 'labels'))
        resp = self.service.list(self.base+'modules/', filter, sort)
        return self.service.decode(schema, resp, many=True)

    def get_module(self, name):
        """Get a module."""
        schema = ModuleSchema()
        resp = self.service.get(self.base+'modules/'+name+'/')
        return self.service.decode(schema, resp)

    def list_tests(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        """Get a list of tests."""
        schema = TestSchema(exclude=('description', 'labels', 'testvars'))
        resp = self.service.list(self.base+'tests/', filter, sort)
        return self.service.decode(schema, resp, many=True)

    def get_test(self, name):
        """Get a test."""
        schema = TestSchema()
        resp = self.service.get(self.base+'tests/'+name+'/')
        return self.service.decode(schema, resp)

    def list_labels(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        """Get a list of labels."""
        schema = LabelSchema(exclude=('index', 'description', 'modules', 'tests'))
        resp = self.service.list(self.base+'labels/', filter, sort)
        return self.service.decode(schema, resp, many=True)

    def get_label(self, name):
        """Get a label."""
        schema = LabelSchema()
        resp = self.service.get(self.base+'labels/'+name+'/')
        return self.service.decode(schema, resp)

    def list_errors(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        """Get a list of errors."""
        schema = ErrorSchema(exclude=('index', 'description'))
        resp = self.service.list(self.base+'errors/', filter, sort)
        return self.service.decode(schema, resp, many=True)

    def get_error(self, name):
        """Get a error."""
        schema = ErrorSchema()
        resp = self.service.get(self.base+'errors/'+name+'/')
        return self.service.decode(schema, resp)

    def list_testvars(self, filter=None, sort=None): # pylint: disable=redefined-builtin
        """Get a list of testvars."""
        schema = TestvarSchema(exclude=('index', 'humanname', 'addedin', 'deprecatedin', 'obsoletedin',
                                        'min', 'max', 'length', 'dyndefault', 'keywords', 'alsoaccept',
                                        'wildcard', 'instances', 'parent', 'children', 'tests'))
        resp = self.service.list(self.base+'testvars/', filter, sort)
        return self.service.decode(schema, resp, many=True)

    def get_testvar(self, name):
        """Get a testvar."""
        schema = TestvarSchema()
        resp = self.service.get(self.base+'testvars/'+name+'/')
        return self.service.decode(schema, resp)
