# coding: utf-8

"""
Tests for ES marc.
"""

import unittest
import marcx

DOC_03692895X = {u'_id': u'03692895X',
 u'_index': u'bsz',
 u'_score': 1.0,
 u'_source': {u'content': {u'001': u'03692895X',
   u'003': u'DE-576',
   u'005': u'20100313023318.0',
   u'007': u'tu',
   u'008': u'940120s1850    xx       m    000 0 lat c',
   u'016': [{u'a': u'(OCoLC)253442902', u'ind1': u' ', u'ind2': u' '}],
   u'035': [{u'a': u'(DE-599)BSZ03692895X', u'ind1': u' ', u'ind2': u' '}],
   u'040': [{u'a': u'DE-576',
     u'b': u'ger',
     u'c': u'DE-576',
     u'e': u'rakwb',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'041': [{u'a': u'lat', u'ind1': u'0', u'ind2': u' '},
    {u'a': u'lat.', u'ind1': u'0', u'ind2': u'7'}],
   u'046': [{u'2': u'DE-576', u'ind1': u' ', u'ind2': u' ', u'j': u'a19a'}],
   u'100': [{u'0': u'(DE-576)171604253',
     u'a': u'Nahmer, Friedrich Wilhelm V. D.',
     u'ind1': u'1',
     u'ind2': u' '}],
   u'245': [{u'a': u'De hydrophobia nonnulla /',
     u'c': u'Friedrich Wilhelm V. D. Nahmer',
     u'ind1': u'1',
     u'ind2': u'0'}],
   u'260': [{u'a': u'Gryphiae,', u'c': u'1850', u'ind1': u' ', u'ind2': u' '}],
   u'502': [{u'a': u'Greifswald, Univ., Diss., 1850.',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'751': [{u'4': u'uvp', u'a': u'Greifswald', u'ind1': u' ', u'ind2': u' '}],
   u'935': [{u'b': u'druck', u'ind1': u' ', u'ind2': u' '},
    {u'c': u'hs', u'ind1': u' ', u'ind2': u' '}]},
  u'meta': {u'date': u'2014-03-04'}},
 u'_type': u'title'}

DOC_091849799 = {u'_id': u'091849799',
 u'_index': u'bsz',
 u'_score': 1.8562834,
 u'_source': {u'content': {u'001': u'091849799',
   u'003': u'DE-576',
   u'005': u'20101119034051.0',
   u'007': u'tu',
   u'008': u'010619s2001    xx             00 0 eng c',
   u'010': [{u'a': u'   000103127', u'ind1': u' ', u'ind2': u' '}],
   u'016': [{u'a': u'(OCoLC)64655014', u'ind1': u' ', u'ind2': u' '}],
   u'020': [{u'9': u'0-262-03293-7',
     u'a': u'0262032937',
     u'ind1': u' ',
     u'ind2': u' '},
    {u'9': u'0-07-013151-1',
     u'a': u'0070131511',
     u'ind1': u' ',
     u'ind2': u' '},
    {u'9': u'0-262-53196-8',
     u'a': u'0262531968',
     u'ind1': u' ',
     u'ind2': u' '},
    {u'9': u'978-0-262-03293-3',
     u'a': u'9780262032933',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'024': [{u'a': u'9780262032933', u'ind1': u'3', u'ind2': u' '},
    {u'a': u'9780262531962', u'ind1': u'8', u'ind2': u' '}],
   u'035': [{u'a': u'(DE-599)BSZ091849799', u'ind1': u' ', u'ind2': u' '}],
   u'040': [{u'a': u'DE-576',
     u'b': u'ger',
     u'c': u'DE-576',
     u'e': u'rakwb',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'041': [{u'a': u'eng', u'ind1': u'0', u'ind2': u' '}],
   u'082': [{u'a': u'005.1', u'ind1': u'0', u'ind2': u' '}],
   u'084': [{u'2': u'rvk', u'a': u'ST 130', u'ind1': u' ', u'ind2': u' '},
    {u'2': u'rvk', u'a': u'ST 134', u'ind1': u' ', u'ind2': u' '}],
   u'245': [{u'a': u'Introduction to algorithms /',
     u'c': u'Thomas H. Cormen ...',
     u'ind1': u'1',
     u'ind2': u'0'}],
   u'250': [{u'a': u'2. ed.', u'ind1': u' ', u'ind2': u' '}],
   u'260': [{u'a': u'Cambridge, Mass. [u.a.] :',
     u'b': u'MIT Press [u.a.],',
     u'c': u'2001',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'300': [{u'a': u'XXI, 1180 S. :',
     u'b': u'graph. Darst.',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'591': [{u'a': u'720 ddsu/sos; 721 ddsu/sfu\u0308 ; 720 ff. (DDC): GBV/LOC',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'650': [{u'a': u'Computer',
     u'ind1': u' ',
     u'ind2': u'0',
     u'x': u'Programming'},
    {u'a': u'Computer algorithms', u'ind1': u' ', u'ind2': u'0'}],
   u'689': [{u'0': [u'(DE-588c)4200409-3', u'(DE-576)210135271'],
     u'2': u'swd',
     u'A': u's',
     u'a': u'Algorithmentheorie',
     u'ind1': u'0',
     u'ind2': u'0'},
    {u'5': u'DE-576', u'ind1': u'0', u'ind2': u' '}],
   u'700': [{u'0': [u'(DE-588a)12942661X', u'(DE-576)166909602'],
     u'a': u'Cormen, Thomas H.',
     u'd': u'1989-',
     u'ind1': u'1',
     u'ind2': u' '}],
   u'780': [{u'i': u'1. Aufl. u.d.T.',
     u'ind1': u'0',
     u'ind2': u'0',
     u't': u'Cormen, Thomas H.: Introduction to algorithms'}],
   u'935': [{u'b': u'druck', u'ind1': u' ', u'ind2': u' '}],
   u'936': [{u'0': u'200877461',
     u'a': u'ST 130',
     u'b': u'Allgemeines',
     u'ind1': u'r',
     u'ind2': u'v'},
    {u'0': u'202612511',
     u'a': u'ST 134',
     u'b': u'Algorithmen-, Komplexita\u0308tstheorie',
     u'ind1': u'r',
     u'ind2': u'v'}]},
  u'meta': {u'date': u'2014-03-04'}},
 u'_type': u'title'}


class MarcDocTest(unittest.TestCase):

    def test_DOC_03692895X(self):
        em = marcx.marcdoc(DOC_03692895X)
        self.assertNotEquals(None, em)
        self.assertEquals(em.titles(), [u'De hydrophobia nonnulla /'])
        self.assertEquals(em.subtitles(), [])
        self.assertEquals(em.authors(), [u'Nahmer, Friedrich Wilhelm V. D.'])
        self.assertEquals(em.additional_authors(), [])
        self.assertEquals(em.isbns(), [])

    def test_DOC_03692895X(self):
        em = marcx.marcdoc(DOC_091849799)
        self.assertNotEquals(None, em)
        self.assertEquals(list(em.isbns()), [u'0262032937',
                                             u'0070131511',
                                             u'0262531968',
                                             u'9780262032933',
                                             u'0-262-03293-7',
                                             u'0-07-013151-1',
                                             u'0-262-53196-8',
                                             u'978-0-262-03293-3'])

        self.assertEquals(em.x700a, [u'Cormen, Thomas H.'])
        self.assertEquals(em.x935b, [u'druck'])
        self.assertEquals(em.x650x, [u'Programming'])
        self.assertEquals(em.x650x, [u'Programming'])