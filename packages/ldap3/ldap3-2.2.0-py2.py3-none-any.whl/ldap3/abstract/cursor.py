"""
"""

# Created on 2014.01.06
#
# Author: Giovanni Cannata
#
# Copyright 2014, 2015, 2016, 2017 Giovanni Cannata
#
# This file is part of ldap3.
#
# ldap3 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ldap3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ldap3 in the COPYING and COPYING.LESSER files.
# If not, see <http://www.gnu.org/licenses/>.

from copy import deepcopy
from datetime import datetime
from os import linesep
from time import sleep

from .. import SUBTREE, LEVEL, DEREF_ALWAYS, DEREF_NEVER, BASE, SEQUENCE_TYPES, STRING_TYPES, get_config_parameter
from .attribute import Attribute, OperationalAttribute, WritableAttribute
from .attrDef import AttrDef
from .objectDef import ObjectDef
from .entry import Entry, WritableEntry
from ..core.exceptions import LDAPCursorError
from ..core.results import RESULT_SUCCESS
from ..utils.ciDict import CaseInsensitiveDict
from ..utils.dn import safe_dn, safe_rdn
from . import STATUS_VIRTUAL, STATUS_READ, STATUS_WRITABLE


def _ret_search_value(value):
    return value[0] + '=' + value[1:] if value[0] in '<>~' and value[1] != '=' else value


def _create_query_dict(query_text):
    """
    Create a dictionary with query key:value definitions
    query_text is a comma delimited key:value sequence
    """
    query_dict = dict()
    if query_text:
        for arg_value_str in query_text.split(','):
            if ':' in arg_value_str:
                arg_value_list = arg_value_str.split(':')
                query_dict[arg_value_list[0].strip()] = arg_value_list[1].strip()

    return query_dict


class Cursor(object):
    # entry_class and attribute_class define the type of entry and attribute used by the cursor
    # entry_initial_status defines the initial status of a entry
    # entry_class = Entry, must be defined in subclasses
    # attribute_class = Attribute, must be defined in subclasses
    # entry_initial_status = STATUS, must be defined in subclasses

    def __init__(self, connection, object_def, get_operational_attributes=False, attributes=None, controls=None):
        self.connection = connection

        if connection._deferred_bind or connection._deferred_open:  # probably a lazy connection, tries to bind
            connection._fire_deferred()

        if isinstance(object_def, STRING_TYPES):
            object_def = ObjectDef(object_def, connection.server.schema)
        self.definition = object_def
        if attributes:  # checks if requested attributes are defined in ObjectDef
            not_defined_attributes = []
            if isinstance(attributes, STRING_TYPES):
                attributes = [attributes]

            for attribute in attributes:
                if attribute not in self.definition._attributes:
                    not_defined_attributes.append(attribute)

            if not_defined_attributes:
                raise LDAPCursorError('Attributes \'%s\' non in definition' % ', '.join(not_defined_attributes))

        self.attributes = set(attributes) if attributes else set([attr.name for attr in self.definition])
        self.get_operational_attributes = get_operational_attributes
        self.controls = controls
        self.execution_time = None
        self.entries = []
        self.schema = self.connection.server.schema
        self._do_not_reset = False  # used for refreshing entry in entry_refresh() without removing all entries from the Cursor

    def __repr__(self):
        r = 'CURSOR : ' + self.__class__.__name__ + linesep
        r += 'CONN   : ' + str(self.connection) + linesep
        r += 'DEFS   : ' + repr(self.definition._object_class) + ' ['
        for attr_def in sorted(self.definition):
            r += (attr_def.key if attr_def.key == attr_def.name else (attr_def.key + ' <' + attr_def.name + '>')) + ', '
        if r[-2] == ',':
            r = r[:-2]
        r += ']' + linesep
        r += 'ATTRS  : ' + repr(sorted(self.attributes)) + (' [OPERATIONAL]' if self.get_operational_attributes else '') + linesep
        if isinstance(self, Reader):
            r += 'BASE   : ' + repr(self.base) + (' [SUB]' if self.sub_tree else ' [LEVEL]') + linesep
            if self._query:
                r += 'QUERY  : ' + repr(self._query) + ('' if '(' in self._query else (' [AND]' if self.components_in_and else ' [OR]')) + linesep
            if self.validated_query:
                r += 'PARSED : ' + repr(self.validated_query) + ('' if '(' in self._query else (' [AND]' if self.components_in_and else ' [OR]')) + linesep
            if self.query_filter:
                r += 'FILTER : ' + repr(self.query_filter) + linesep

        if self.execution_time:
            r += 'ENTRIES: ' + str(len(self.entries))
            r += ' [executed at: ' + str(self.execution_time.isoformat()) + ']' + linesep
        return r

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return self.entries.__iter__()

    def __getitem__(self, item):
        return self.entries[item]

    def __len__(self):
        return len(self.entries)

    if str != bytes:  # python 3
        def __bool__(self):  # needed to make the cursor appears as existing in "if cursor:" even if there are no entries
            return True
    else:  # python 2
        def __nonzero__(self):
            return True

    def _get_attributes(self, response, attr_defs, entry):
        """Assign the result of the LDAP query to the Entry object dictionary.

        If the optional 'post_query' callable is present in the AttrDef it is called with each value of the attribute and the callable result is stored in the attribute.

        Returns the default value for missing attributes.
        If the 'dereference_dn' in AttrDef is a ObjectDef then the attribute values are treated as distinguished name and the relevant entry is retrieved and stored in the attribute value.

        """
        attributes = CaseInsensitiveDict()
        used_attribute_names = set()
        for attr_def in attr_defs:
            attribute_name = None
            for attr_name in response['attributes']:
                if attr_def.name.lower() == attr_name.lower():
                    attribute_name = attr_name
                    # if isinstance(response['attributes'][name], list) and len(response['attributes'][name]) == 0:  # empty attributes returned as empty list with the return_empty_attributes of the Connection object
                    #    name = None
                    break

            if attribute_name or attr_def.default is not NotImplemented:  # attribute value found in result or default value present - NotImplemented allows use of None as default
                attribute = self.attribute_class(attr_def, entry, self)
                attribute.response = response
                attribute.raw_values = response['raw_attributes'][attribute_name] if attribute_name else None
                if attr_def.post_query and attr_def.name in response['attributes'] and response['raw_attributes'] != list():
                    attribute.values = attr_def.post_query(attr_def.key, response['attributes'][attribute_name])
                else:
                    if attr_def.default is NotImplemented or (attribute_name and response['raw_attributes'][attribute_name] != list()):
                        attribute.values = response['attributes'][attribute_name]
                    else:
                        attribute.values = attr_def.default if isinstance(attr_def.default, SEQUENCE_TYPES) else [attr_def.default]
                if not isinstance(attribute.values, list):  # force attribute values to list (if attribute is single-valued)
                    attribute.values = [attribute.values]
                if attr_def.dereference_dn:  # try to get object referenced in value
                    if attribute.values:
                        temp_reader = Reader(self.connection, attr_def.dereference_dn, base='', get_operational_attributes=self.get_operational_attributes, controls=self.controls)
                        temp_values = []
                        for element in attribute.values:
                            temp_values.append(temp_reader.search_object(element))
                        del temp_reader  # remove the temporary Reader
                        attribute.values = temp_values
                attributes[attribute.key] = attribute
                used_attribute_names.add(attribute_name)

        if self.attributes:
            used_attribute_names.update(self.attributes)

        for attribute_name in response['attributes']:
            if attribute_name not in used_attribute_names:
                if attribute_name not in attr_defs:
                    raise LDAPCursorError('attribute \'%s\' not in object class \'%s\' for entry %s' % (attribute_name, ', '.join(entry.entry_definition._object_class), entry.entry_dn))
                attribute = OperationalAttribute(AttrDef(get_config_parameter('ABSTRACTION_OPERATIONAL_ATTRIBUTE_PREFIX') + attribute_name), entry, self)
                attribute.raw_values = response['raw_attributes'][attribute_name]
                attribute.values = response['attributes'][attribute_name]
                if (get_config_parameter('ABSTRACTION_OPERATIONAL_ATTRIBUTE_PREFIX') + attribute_name) not in attributes:
                    attributes[get_config_parameter('ABSTRACTION_OPERATIONAL_ATTRIBUTE_PREFIX') + attribute_name] = attribute

        return attributes

    def _create_entry(self, response):
        if not response['type'] == 'searchResEntry':
            return None

        entry = self.entry_class(response['dn'], self)  # define an Entry (writable or readonly), as specified in the cursor definition
        entry._state.attributes = self._get_attributes(response, self.definition, entry)
        entry._state.entry_raw_attributes = deepcopy(response['raw_attributes'])

        entry._state.response = response
        entry._state.read_time = datetime.now()
        entry._state.set_status(self.entry_initial_status)
        for attr in entry:  # returns the whole attribute object
            entry.__dict__[attr.key] = attr

        return entry

    def _execute_query(self, query_scope, attributes):
        if not self.connection:
            raise LDAPCursorError('no connection established')
        old_query_filter = None
        if query_scope == BASE:  # requesting a single object so an always-valid filter is set
            if hasattr(self, 'query_filter'):  # only Reader has a query filter
                old_query_filter = self.query_filter
            self.query_filter = '(objectclass=*)'
        else:
            self._create_query_filter()
        with self.connection:
            result = self.connection.search(search_base=self.base,
                                            search_filter=self.query_filter,
                                            search_scope=query_scope,
                                            dereference_aliases=self.dereference_aliases,
                                            attributes=attributes if attributes else self.attributes,
                                            get_operational_attributes=self.get_operational_attributes,
                                            controls=self.controls)
            if not self.connection.strategy.sync:
                response, _ = self.connection.get_response(result)
            else:
                response = self.connection.response

        if self._do_not_reset:  # trick to not remove entries when using _refresh()
            return self._create_entry(response[0])

        self.entries = []
        for r in response:
            entry = self._create_entry(r)
            self.entries.append(entry)

        self.execution_time = datetime.now()

        if old_query_filter:  # requesting a single object so an always-valid filter is set
            self.query_filter = old_query_filter

    def remove(self, entry):
        self.entries.remove(entry)


class Reader(Cursor):
    """Reader object to perform searches:

    :param connection: the LDAP connection object to use
    :type connection: LDAPConnection
    :param object_def: the ObjectDef of the LDAP object returned
    :type object_def: ObjectDef
    :param query: the simplified query (will be transformed in an LDAP filter)
    :type query: str
    :param base: starting base of the search
    :type base: str
    :param components_in_and: specify if assertions in the query must all be satisfied or not (AND/OR)
    :type components_in_and: bool
    :param sub_tree: specify if the search must be performed ad Single Level (False) or Whole SubTree (True)
    :type sub_tree: bool
    :param get_operational_attributes: specify if operational attributes are returned or not
    :type get_operational_attributes: bool
    :param controls: controls to be used in search
    :type controls: tuple

    """
    entry_class = Entry  # entries are read_only
    attribute_class = Attribute  # attributes are read_only
    entry_initial_status = STATUS_READ

    def __init__(self, connection, object_def, base, query='', components_in_and=True, sub_tree=True, get_operational_attributes=False, attributes=None, controls=None):
        Cursor.__init__(self, connection, object_def, get_operational_attributes, attributes, controls)
        self._components_in_and = components_in_and
        self.sub_tree = sub_tree
        self._query = query
        self.base = base
        self.dereference_aliases = DEREF_ALWAYS
        self.validated_query = None
        self._query_dict = dict()
        self._validated_query_dict = dict()
        self.query_filter = None
        self.reset()

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        self._query = value
        self.reset()

    @property
    def components_in_and(self):
        return self._components_in_and

    @components_in_and.setter
    def components_in_and(self, value):
        self._components_in_and = value
        self.reset()

    def clear(self):
        """Clear the Reader search parameters

        """
        self.dereference_aliases = DEREF_ALWAYS

    def reset(self):
        """Clear all the Reader parameters

        """
        self.clear()
        self.validated_query = None
        self._query_dict = dict()
        self._validated_query_dict = dict()
        self.execution_time = None
        self.query_filter = None
        self.entries = []
        self._create_query_filter()

    def _validate_query(self):
        """Processes the text query and verifies that the requested friendly names are in the Reader dictionary
        If the AttrDef has a 'validate' property the callable is executed and if it returns False an Exception is raised

        """
        if not self._query_dict:
            self._query_dict = _create_query_dict(self._query)

        query = ''
        for d in sorted(self._query_dict):
            attr = d[1:] if d[0] in '&|' else d
            for attr_def in self.definition:
                if ''.join(attr.split()).lower() == attr_def.key.lower():
                    attr = attr_def.key
                    break
            if attr in self.definition:
                vals = sorted(self._query_dict[d].split(';'))

                query += (d[0] + attr if d[0] in '&|' else attr) + ': '
                for val in vals:
                    val = val.strip()
                    val_not = True if val[0] == '!' else False
                    val_search_operator = '='  # default
                    if val_not:
                        if val[1:].lstrip()[0] not in '=<>~':
                            value = val[1:].lstrip()
                        else:
                            val_search_operator = val[1:].lstrip()[0]
                            value = val[1:].lstrip()[1:]
                    else:
                        if val[0] not in '=<>~':
                            value = val.lstrip()
                        else:
                            val_search_operator = val[0]
                            value = val[1:].lstrip()

                    if self.definition[attr].validate:
                        validated = self.definition[attr].validate(self.definition[attr].key, value)  # returns True, False or a value to substitute to the actual values
                        if validated is False:
                            raise LDAPCursorError('validation failed for attribute %s and value %s' % (d, val))
                        elif validated is not True:  # a valid LDAP value equivalent to the actual values
                                value = validated
                    if val_not:
                        query += '!' + val_search_operator + value
                    else:
                        query += val_search_operator + value

                    query += ';'
                query = query[:-1] + ', '
            else:
                raise LDAPCursorError('attribute \'%s\' not in definition' % attr)
        self.validated_query = query[:-2]
        self._validated_query_dict = _create_query_dict(self.validated_query)

    def _create_query_filter(self):
        """Converts the query dictionary to the filter text"""
        self.query_filter = ''

        if self.definition._object_class:
            self.query_filter += '(&'
            if isinstance(self.definition._object_class, SEQUENCE_TYPES) and len(self.definition._object_class) == 1:
                self.query_filter += '(objectClass=' + self.definition._object_class[0] + ')'
            elif isinstance(self.definition._object_class, SEQUENCE_TYPES):
                self.query_filter += '(&'
                for object_class in self.definition._object_class:
                    self.query_filter += '(objectClass=' + object_class + ')'
                self.query_filter += ')'
            else:
                raise LDAPCursorError('object_class must be a string or a list')

        if self._query and self._query.startswith('(') and self._query.endswith(')'):  # query is already an LDAP filter
            if 'objectclass' not in self._query.lower():
                self.query_filter += self._query + ')'  # if objectclass not in filter adds from definition
            else:
                self.query_filter = self._query
            return
        elif self._query:  # if a simplified filter is present
            if not self.components_in_and:
                self.query_filter += '(|'
            elif not self.definition._object_class:
                self.query_filter += '(&'

            self._validate_query()

            attr_counter = 0
            for attr in sorted(self._validated_query_dict):
                attr_counter += 1
                multi = True if ';' in self._validated_query_dict[attr] else False
                vals = sorted(self._validated_query_dict[attr].split(';'))
                attr_def = self.definition[attr[1:]] if attr[0] in '&|' else self.definition[attr]
                if attr_def.pre_query:
                    modvals = []
                    for val in vals:
                        modvals.append(val[0] + attr_def.pre_query(attr_def.key, val[1:]))
                    vals = modvals
                if multi:
                    if attr[0] in '&|':
                        self.query_filter += '(' + attr[0]
                    else:
                        self.query_filter += '(|'

                for val in vals:
                    if val[0] == '!':
                        self.query_filter += '(!(' + attr_def.name + _ret_search_value(val[1:]) + '))'
                    else:
                        self.query_filter += '(' + attr_def.name + _ret_search_value(val) + ')'
                if multi:
                    self.query_filter += ')'

            if not self.components_in_and:
                self.query_filter += '))'
            else:
                self.query_filter += ')'

            if not self.definition._object_class and attr_counter == 1:  # remove unneeded starting filter
                self.query_filter = self.query_filter[2: -1]

            if self.query_filter == '(|)' or self.query_filter == '(&)':  # remove empty filter
                self.query_filter = ''
        else:  # no query, remove unneeded leading (&
            self.query_filter = self.query_filter[2:]

    def search(self, attributes=None):
        """Perform the LDAP search

        :return: Entries found in search

        """
        self.clear()
        query_scope = SUBTREE if self.sub_tree else LEVEL
        self._execute_query(query_scope, attributes)

        return self.entries

    def search_object(self, entry_dn=None, attributes=None):  # base must be a single dn
        """Perform the LDAP search operation SINGLE_OBJECT scope

        :return: Entry found in search

        """
        self.clear()
        if entry_dn:
            old_base = self.base
            self.base = entry_dn
            self._execute_query(BASE, attributes)
            self.base = old_base
        else:
            self._execute_query(BASE, attributes)

        return self.entries[0] if len(self.entries) > 0 else None

    def search_level(self, attributes=None):
        """Perform the LDAP search operation with SINGLE_LEVEL scope

        :return: Entries found in search

        """
        self.clear()
        self._execute_query(LEVEL, attributes)

        return self.entries

    def search_subtree(self, attributes=None):
        """Perform the LDAP search operation WHOLE_SUBTREE scope

        :return: Entries found in search

        """
        self.clear()
        self._execute_query(SUBTREE, attributes)

        return self.entries

    # def search_size_limit(self, size_limit, attributes=None):
    #     """Perform the LDAP search with limit of entries found
    #
    #     :param attributes: optional attriibutes to search
    #     :param size_limit: maximum number of entries returned
    #     :return: Entries found in search
    #
    #     """
    #
    #     self.clear()
    #     self.size_limit = size_limit
    #     query_scope = SUBTREE if self.sub_tree else LEVEL
    #     self._execute_query(query_scope, attributes)
    #
    #     return self.entries
    #
    # def search_time_limit(self, time_limit, attributes=None):
    #     """Perform the LDAP search with limit of time spent in searching by the server
    #
    #     :param attributes: optional attributes to search
    #     :param time_limit: maximum number of seconds to wait for a search
    #     :return: Entries found in search
    #
    #     """
    #     self.clear()
    #     self.time_limit = time_limit
    #     query_scope = SUBTREE if self.sub_tree else LEVEL
    #     self._execute_query(query_scope, attributes)
    #
    #     return self.entries
    #
    # def search_types_only(self, attributes=None):
    #     """Perform the search returning attribute names only.
    #
    #     :return: Entries found in search
    #
    #     """
    #     self.clear()
    #     self.types_only = True
    #     query_scope = SUBTREE if self.sub_tree else LEVEL
    #     self._execute_query(query_scope, attributes)
    #
    #     return self.entries

    def search_paged(self, paged_size, paged_criticality=True, generator=True, attributes=None):
        """Perform a paged search, can be called as an Iterator

        :param attributes: optional attributes to search
        :param paged_size: number of entries returned in each search
        :type paged_size: int
        :param paged_criticality: specify if server must not execute the search if it is not capable of paging searches
        :type paged_criticality: bool
        :param generator: if True the paged searches are executed while generating the entries,
                          if False all the paged searches are execute before returning the generator
        :type generator: bool
        :return: Entries found in search

        """
        if not self.connection:
            raise LDAPCursorError('no connection established')

        self.clear()
        self._create_query_filter()
        self.entries = []
        self.execution_time = datetime.now()
        for response in self.connection.extend.standard.paged_search(search_base=self.base,
                                                                     search_filter=self.query_filter,
                                                                     search_scope=SUBTREE if self.sub_tree else LEVEL,
                                                                     dereference_aliases=self.dereference_aliases,
                                                                     attributes=attributes if attributes else self.attributes,
                                                                     get_operational_attributes=self.get_operational_attributes,
                                                                     controls=self.controls,
                                                                     paged_size=paged_size,
                                                                     paged_criticality=paged_criticality,
                                                                     generator=generator):
            yield self._create_entry(response)


class Writer(Cursor):
    entry_class = WritableEntry
    attribute_class = WritableAttribute
    entry_initial_status = STATUS_WRITABLE

    @staticmethod
    def from_cursor(cursor, connection=None, object_def=None, custom_validator=None):
        if connection is None:
            connection = cursor.connection
        if object_def is None:
            object_def = cursor.definition
        writer = Writer(connection, object_def, attributes=cursor.attributes)
        for entry in cursor.entries:
            if isinstance(cursor, Reader):
                entry.entry_writable(object_def, writer, custom_validator=custom_validator)
            elif isinstance(cursor, Writer):
                pass
            else:
                raise LDAPCursorError('unknown cursor type %s' % str(type(cursor)))
        writer.execution_time = cursor.execution_time
        return writer

    @staticmethod
    def from_response(connection, object_def, response=None):
        if response is None:
            if not connection.strategy.sync:
                raise LDAPCursorError(' with async strategies response must be specified')
            elif connection.response:
                response = connection.response
            else:
                raise LDAPCursorError('response not present')
        writer = Writer(connection, object_def)
        # for entry in connection._get_entries(response):
        #     entry.entry_writable(object_def, writer, custom_validator=custom_validator)
        # return writer

        for resp in response:
            if resp['type'] == 'searchResEntry':
                entry = writer._create_entry(resp)
                writer.entries.append(entry)
        return writer

    def __init__(self, connection, object_def, get_operational_attributes=False, attributes=None, controls=None):
        Cursor.__init__(self, connection, object_def, get_operational_attributes, attributes, controls)
        self.dereference_aliases = DEREF_NEVER

    def commit(self, refresh=True):
        for entry in self.entries:
            entry.entry_commit_changes(refresh=refresh, controls=self.controls)
        self.execution_time = datetime.now()

    def discard(self):
        for entry in self.entries:
            entry.entry_discard_changes()

    def _refresh_object(self, entry_dn, attributes=None, tries=4, seconds=2, controls=None):  # base must be a single dn
        """Performs the LDAP search operation SINGLE_OBJECT scope

        :return: Entry found in search

        """
        if not self.connection:
            raise LDAPCursorError('no connection established')

        response = []
        with self.connection:
            counter = 0
            while counter < tries:
                result = self.connection.search(search_base=entry_dn,
                                                search_filter='(objectclass=*)',
                                                search_scope=BASE,
                                                dereference_aliases=DEREF_NEVER,
                                                attributes=attributes if attributes else self.attributes,
                                                get_operational_attributes=self.get_operational_attributes,
                                                controls=controls)
                if not self.connection.strategy.sync:
                    response, result = self.connection.get_response(result)
                else:
                    response = self.connection.response
                    result = self.connection.result

                if result['result'] in [RESULT_SUCCESS]:
                    break
                sleep(seconds)
                counter += 1

        if len(response) == 1:
            return self._create_entry(response[0])
        elif len(response) == 0:
            return None

        raise LDAPCursorError('Too many entries returned for a single object search')

    def new(self, dn):
        dn = safe_dn(dn)
        for entry in self.entries:  # checks if dn is already used in an cursor entry
            if entry.entry_dn == dn:
                raise LDAPCursorError('dn already present in cursor')
        rdns = safe_rdn(dn, decompose=True)
        entry = self.entry_class(dn, self)  # defines a new empty Entry
        for attr in entry.entry_mandatory_attributes:  # defines all mandatory attributes as virtual
                entry._state.attributes[attr] = self.attribute_class(entry._state.definition[attr], entry, self)
                entry.__dict__[attr] = entry._state.attributes[attr]
        entry.objectclass.set(self.definition._object_class)
        for rdn in rdns:  # adds virtual attributes from rdns in entry name (should be more than one with + syntax)
            if rdn[0] in entry._state.definition._attributes:
                rdn_name = entry._state.definition._attributes[rdn[0]].name  # normalize case folding
                if rdn_name not in entry._state.attributes:
                    entry._state.attributes[rdn_name] = self.attribute_class(entry._state.definition[rdn_name], entry, self)
                    entry.__dict__[rdn_name] = entry._state.attributes[rdn_name]
                entry.__dict__[rdn_name].set(rdn[1])
            else:
                raise LDAPCursorError('rdn type \'%s\' not in objectclass definition' % rdn[0])
        entry._state.set_status(STATUS_VIRTUAL)
        self.entries.append(entry)
        return entry

    def refresh_entry(self, entry, tries=4, seconds=2):
        self._do_not_reset = True
        temp_entry = self._refresh_object(entry.entry_dn, entry.entry_attributes, tries, seconds=seconds)  # if any attributes is added adds only to the entry not to the definition
        self._do_not_reset = False
        if temp_entry:
            temp_entry._state.origin = entry._state.origin
            entry.__dict__.clear()
            entry.__dict__['_state'] = temp_entry._state
            for attr in entry._state.attributes:  # returns the attribute key
                entry.__dict__[attr] = entry._state.attributes[attr]

            for attr in entry.entry_attributes:  # if any attribute of the class was deleted make it virtual
                if attr not in entry._state.attributes and attr in entry.entry_definition._attributes:
                    entry._state.attributes[attr] = WritableAttribute(entry.entry_definition[attr], entry, self)
                    entry.__dict__[attr] = entry._state.attributes[attr]
            entry._state.set_status(entry._state._initial_status)
            return True
        return False
