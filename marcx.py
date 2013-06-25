#!/usr/bin/env python
# coding: utf-8

"""
Few extensions on `pymarc.Record` to make certain
checks and manipulations a bit easier.

"""

from pymarc.record import Record, Field
from pymarc.exceptions import FieldNotFound
import pyisbn
import re


def isbn_convert(self, isbn_10_or_13):
    """ Return the *other* ISBN representation. Returns `None`
    if conversion fails.
    """
    try:
        return pyisbn.convert(isbn_10_or_13)
    except pyisbn.IsbnError as isbnerr:
        pass


def _equals(value):
    """ equality """
    return lambda v: value == v


def _not(value):
    """ usage example: `_not(_equal(...))` """
    if hasattr(value, '__call__'):
        return lambda v: not value(v)
    else:
        return lambda v: not v


def _match(value):
    """ maps to `re.match` (match at the beginning of `v`) """
    return lambda v: re.match(value, v)


def _search(value):
    """ maps to `re.search` (match anywhere in `v`) """
    return lambda v: re.search(value, v)


def _startwith(value):
    """ maps to `string.startswith` """
    return lambda v: v.startswith(value)


def _endswith(value):
    """ maps to `string.endswith` """
    return lambda v: v.endswith(value)


def valuegetter(*fieldspecs, **kwargs):
    """ Modelled after `operator.itemgetter`; takes a variable
    number of specs and returns a function, which applied to
    any `pymarc.Record` returns the matching values.

    Specs are in the form `field` or `field.subfield`, e.g.
    `020` or `020.9`.

    Example:

    >>> from fatrecord import FatRecord, valuegetter
    >>> with open("~/code/edsu/pymarc/test/marc.dat") as handle:
    ...    record = FatRecord(data=handle.read())

    In two steps:

    >>> getter = valuegetter('020.a')
    >>> getter(record)
    <generator object values at 0x2d97690>

    >>> set(getter(record))
    set(['020161622X'])

    Or in one line:

    >>> set(valuegetter('020.a')(record))
    set(['020161622X'])

    A variable number of specs can be passed:

    >>> set(valuegetter('001', '005', '700.a')(record))
    set(['20040816084925.0', 'Thomas, David,', '11778504'])

    Non-existent field tags can be passed - they are ignored:
    >>> set(valuegetter('002')(record))
    set([])

    @see also: `FatRecord.vg`

    """
    combine_subfields = kwargs.get('combine_subfields', False)
    pattern = r'(?P<field>[^.]+)(.(?P<subfield>[^.]+))?'

    def values(record):
        for s in fieldspecs:
            match = re.match(pattern, s)
            if not match:
                continue
            gd = match.groupdict()
            for field in record.get_fields(gd['field']):
                if gd['subfield']:
                    for value in field.get_subfields(gd['subfield']):
                        yield value
                else:
                    if combine_subfields:
                        yield field.value()
                    else:
                        if int(gd['field']) < 10:
                            yield field.value()
                        else:
                            for value in field.subfields[1::2]:
                                yield value
    return values


def fieldgetter(*fieldspecs):
    """ Similar to `valuegetter`, except this returns
    (`pymarc.Field`, value) tuples.
    Takes any number of fieldspecs.
    """
    pattern = r'(?P<field>[^.]+)(.(?P<subfield>[^.]+))?'

    def fields(record):
        for s in fieldspecs:
            match = re.match(pattern, s)
            if not match:
                continue
            grp = match.groupdict()
            for field in record.get_fields(grp['field']):
                if grp['subfield']:
                    for value in field.get_subfields(grp['subfield']):
                        yield field, value
                else:
                    if int(grp['field']) < 10:
                        yield field, field.value()
                    else:
                        for value in field.subfields[1::2]:
                            yield field, value
    return fields


class FatRecord(Record):
    """ A record with some extras.
    """

    CONTROL_FIELDS = set(
        ('001', '002', '003', '004', '005', '006', '007', '008', '009'))

    E_NO_INDICATORS = """control fields take no indicators
    see: http://www.loc.gov/marc/bibliographic/bd00x.html"""
    E_NO_SUBFIELDS = """control fields take no subfields
    see: http://www.loc.gov/marc/bibliographic/bd00x.html"""
    E_NO_DATA = "non-control fields take no data"
    E_EMPTY = "data must not be empty"
    E_INVALID_INDICATOR = "invalid indicator"

    def __init__(self, *args, **kwargs):
        super(FatRecord, self).__init__(*args, **kwargs)
        self.sigels = set()
        self.source_id = None
        self.record_id = None

    @classmethod
    def from_doc(cls, doc, **kwargs):
        """ Create a FatRecord from a dictionary as it is
        stored in Elasticsearch.

        Elasticsearch JSON > dict > FatRecord
        """
        assert(isinstance(doc, dict))
        encoding = kwargs.get('encoding', 'utf-8')
        to_unicode = kwargs.get('to_unicode', True)
        force_utf8 = kwargs.get('force_utf8', True)
        if not 'original' in doc:
            raise ValueError('document without `original` key')
        original = doc.get('original', '').encode(encoding)
        return FatRecord(data=original, to_unicode=to_unicode,
                         force_utf8=force_utf8)

    def add(self, tag, data=None, indicators=None, **kwargs):
        """ Add a field to a record. Example:

        marc.add('020', a='0201657880', z='0201802398')
        """
        if data:
            if indicators:
                raise ValueError(SlimRecord.E_NO_INDICATORS)
            if not tag in SlimRecord.CONTROL_FIELDS:
                raise ValueError(SlimRecord.E_NO_DATA)
        else:
            if tag in SlimRecord.CONTROL_FIELDS:
                raise ValueError(SlimRecord.E_EMPTY)

        if tag in SlimRecord.CONTROL_FIELDS and kwargs:
            raise ValueError(SlimRecord.E_NO_SUBFIELDS)

        if indicators is None:
            indicators = [' ', ' ']
        if isinstance(indicators, basestring):
            if len(indicators) == 2:
                indicators = [indicators[0], indicators[1]]
            else:
                raise ValueError(E_INVALID_INDICATOR)

        if data:  # == control field (001 -- 009)
            field = Field(tag, data=data)
        else:     # == non-control field (010 -- 999)
            subfields = [e for sl in list(kwargs.items()) for e in sl]
            field = Field(tag, indicators, subfields=subfields)
        self.add_field(field)

    def remove(self, tag):
        """ Removes **all** fields with tag `tag`. """
        for f in self.get_fields(tag):
            self.remove_field(f)

    def get_control_number(self):
        """ Return the control number value.
        Raises `AttributeError` on missing value.
        """
        return self['001'].value()

    def set_control_number(self, value):
        """ Set the control number.
        """
        current = self['001']
        try:
            self.remove_field(current)
        except FieldNotFound as fnf:
            pass
        self.add('001', data=value)

    # alias control_number to finc_id
    control_number = property(get_control_number, set_control_number)
    finc_id = control_number

    def isbn_candidates(self, *fieldspecs):
        """ Class `pymarc.Record` only has an `isbn` attribute
        (returns the first 020.a value). The fat record can take
        a fieldspec. If no fieldspec is given, use `020.a`.

        Returns a `set` of candidates.
        """
        if not fieldspecs:
            fieldspecs = ('020.a',)
        return set(valuegetter(*fieldspecs)(self))

    def isbns(self, *fieldspecs):
        """ Return checked ISBN candidates as `set`.
        """
        result = set()
        for candidate in self.isbn_candidates(*fieldspecs):
            candidate = (candidate.split() or [""])[0]
            candidate = candidate.replace('-', '')
            if len(candidate) in (10, 13):
                if pyisbn.validate(candidate):
                    result.add(candidate)
        return result

    def grow_isbns(self):
        """ Special routine to grow ISBN from various fields and to complement
        all 10-char versions with their 13-char versions and vice versa.

        An ISBN can be found in:

            020.a   International Standard Book Number (R)
                    http://www.loc.gov/marc/bibliographic/bd020.html

            020.z   $z - Canceled/invalid ISBN (R)

            020.9   unspecified

            776.z   776 - Additional Physical Form Entry (R)
                    $z - International Standard Book Number (R)

        """
        isbns = self.isbns('020.a')

        for isbn in isbns.copy():
            alt = isbn_convert(isbn)
            if alt and alt not in isbns:
                self.add('020', a=alt)
                isbns.add(alt)

        # stash cancelled isbns add additional entries into 020.z
        cancelled = self.isbns('020.z', '020.9')
        additional = self.isbns('776.z')
        isbns.update(cancelled | additional)

        for isbn in cancelled | additional:
            alt = isbn_convert(isbn)
            if alt and alt not in isbns:
                self.add('020', z=alt)
                isbns.add(alt)

        return isbns

    def vg(self, *fieldspecs):
        """ Apply valuegetter on self.
        """
        return valuegetter(*fieldspecs)(self)

    def fg(self, *fieldspecs):
        """ Shortcut for `fieldgetter(*fieldspecs)(self)`
        """
        return fieldgetter(*fieldspecs)(self)

    def remove_field_if(self, fieldspecstr, fun):
        """ Remove a field from this record, if
        `fun(value)` evaluates to `True`.

        Example:

        Iterate over all 710.a fields and remove the
        710 field, if any subfield value startswith
        'Naxos Digital Services.'

        Returns a list of removed fields.

        >>> record.remove_field_if('710.a',
            _startswith('Naxos Digital Services.'))

        """
        fieldspecs = fieldspecstr.split()
        removed = []
        for field, value in fieldgetter(*fieldspecs)(self):
            if fun(value):
                removed.append(field)
                self.remove_field(field)
        return removed

    def test(self, fieldspecstr, fun, all=False):
        """ Test whether the function
        evaluated on the field values matched
        by fieldspecstr returns `True`.

        `fieldspecstr` contains on ore more
        fieldspecs separated by whitespace, e.g.

        >>> def _is_valid_isbn(value):
        ...     ''' poor man's isbn validator '''
        ...     return len(value) in (10, 13)
        >>> record.test('020.a', _is_valid_isbn)
        True

        If `all` is set to `True`, the test only
        returns `True`, when all values pass the given
        check, e.g.:

        >>> record.test('020.a 020.z', _is_valid_isbn, all=True)

        means that for each field and every value the ISBN check
        is performed. Defaults to `False`.

        """
        fieldspecs = fieldspecstr.split()
        if all:
            return min([fun(value) in valuegetter(*fieldspecs)(self)])
        else:
            for value in valuegetter(*fieldspecs)(self):
                if fun(value):
                    return True
        return False

    def t(self, *args, **kwargs):
        """ shorter that `test` """
        return self.test(*args, **kwargs)