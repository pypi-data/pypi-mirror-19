# -*- coding: utf-8 -*-
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from icalendar.parser import Parameters
from icalendar.tests import unittest

import pytz


class TestProp(unittest.TestCase):

    def test_prop_vBinary(self):
        from ..prop import vBinary

        txt = b'This is gibberish'
        txt_ical = b'VGhpcyBpcyBnaWJiZXJpc2g='
        self.assertEqual(vBinary(txt).to_ical(), txt_ical)
        self.assertEqual(vBinary.from_ical(txt_ical), txt)

        # The roundtrip test
        txt = b'Binary data \x13 \x56'
        txt_ical = b'QmluYXJ5IGRhdGEgEyBW'
        self.assertEqual(vBinary(txt).to_ical(), txt_ical)
        self.assertEqual(vBinary.from_ical(txt_ical), txt)

        self.assertIsInstance(vBinary('txt').params, Parameters)
        self.assertEqual(
            vBinary('txt').params, {'VALUE': 'BINARY', 'ENCODING': 'BASE64'}
        )

        # Long data should not have line breaks, as that would interfere
        txt = b'a' * 99
        txt_ical = b'YWFh' * 33
        self.assertEqual(vBinary(txt).to_ical(), txt_ical)
        self.assertEqual(vBinary.from_ical(txt_ical), txt)

    def test_prop_vBoolean(self):
        from ..prop import vBoolean

        self.assertEqual(vBoolean(True).to_ical(), b'TRUE')
        self.assertEqual(vBoolean(0).to_ical(), b'FALSE')

        # The roundtrip test
        self.assertEqual(vBoolean.from_ical(vBoolean(True).to_ical()), True)
        self.assertEqual(vBoolean.from_ical('true'), True)

    def test_prop_vCalAddress(self):
        from ..prop import vCalAddress
        txt = b'MAILTO:maxm@mxm.dk'
        a = vCalAddress(txt)
        a.params['cn'] = 'Max M'

        self.assertEqual(a.to_ical(), txt)
        self.assertIsInstance(a.params, Parameters)
        self.assertEqual(a.params, {'CN': 'Max M'})
        self.assertEqual(vCalAddress.from_ical(txt), 'MAILTO:maxm@mxm.dk')

    def test_prop_vFloat(self):
        from ..prop import vFloat
        self.assertEqual(vFloat(1.0).to_ical(), b'1.0')
        self.assertEqual(vFloat.from_ical('42'), 42.0)
        self.assertEqual(vFloat(42).to_ical(), b'42.0')

    def test_prop_vInt(self):
        from ..prop import vInt
        self.assertEqual(vInt(42).to_ical(), b'42')
        self.assertEqual(vInt.from_ical('13'), 13)
        self.assertRaises(ValueError, vInt.from_ical, '1s3')

    def test_prop_vDDDLists(self):
        from ..prop import vDDDLists

        dt_list = vDDDLists.from_ical('19960402T010000Z')
        self.assertTrue(isinstance(dt_list, list))
        self.assertEqual(len(dt_list), 1)
        self.assertTrue(isinstance(dt_list[0], datetime))
        self.assertEqual(str(dt_list[0]), '1996-04-02 01:00:00+00:00')

        p = '19960402T010000Z,19960403T010000Z,19960404T010000Z'
        dt_list = vDDDLists.from_ical(p)
        self.assertEqual(len(dt_list), 3)
        self.assertEqual(str(dt_list[0]), '1996-04-02 01:00:00+00:00')
        self.assertEqual(str(dt_list[2]), '1996-04-04 01:00:00+00:00')

        dt_list = vDDDLists([])
        self.assertEqual(dt_list.to_ical(), b'')

        dt_list = vDDDLists([datetime(2000, 1, 1)])
        self.assertEqual(dt_list.to_ical(), b'20000101T000000')

        dt_list = vDDDLists([datetime(2000, 1, 1), datetime(2000, 11, 11)])
        self.assertEqual(dt_list.to_ical(), b'20000101T000000,20001111T000000')

    def test_prop_vDDDTypes(self):
        from ..prop import vDDDTypes

        self.assertTrue(isinstance(vDDDTypes.from_ical('20010101T123000'),
                                   datetime))

        self.assertEqual(vDDDTypes.from_ical('20010101T123000Z'),
                         pytz.utc.localize(datetime(2001, 1, 1, 12, 30)))

        self.assertTrue(isinstance(vDDDTypes.from_ical('20010101'), date))

        self.assertEqual(vDDDTypes.from_ical('P31D'), timedelta(31))

        self.assertEqual(vDDDTypes.from_ical('-P31D'), timedelta(-31))

        # Bad input
        self.assertRaises(ValueError, vDDDTypes, 42)

    def test_prop_vDate(self):
        from ..prop import vDate

        self.assertEqual(vDate(date(2001, 1, 1)).to_ical(), b'20010101')
        self.assertEqual(vDate(date(1899, 1, 1)).to_ical(), b'18990101')

        self.assertEqual(vDate.from_ical('20010102'), date(2001, 1, 2))

        self.assertRaises(ValueError, vDate, 'd')

    def test_prop_vDatetime(self):
        from ..prop import vDatetime

        dt = datetime(2001, 1, 1, 12, 30, 0)
        self.assertEqual(vDatetime(dt).to_ical(), b'20010101T123000')

        self.assertEqual(vDatetime.from_ical('20000101T120000'),
                         datetime(2000, 1, 1, 12, 0))

        dutc = pytz.utc.localize(datetime(2001, 1, 1, 12, 30, 0))
        self.assertEqual(vDatetime(dutc).to_ical(), b'20010101T123000Z')

        dutc = pytz.utc.localize(datetime(1899, 1, 1, 12, 30, 0))
        self.assertEqual(vDatetime(dutc).to_ical(), b'18990101T123000Z')

        self.assertEqual(vDatetime.from_ical('20010101T000000'),
                         datetime(2001, 1, 1, 0, 0))

        self.assertRaises(ValueError, vDatetime.from_ical, '20010101T000000A')

        utc = vDatetime.from_ical('20010101T000000Z')
        self.assertEqual(vDatetime(utc).to_ical(), b'20010101T000000Z')

        # 1 minute before transition to DST
        dat = vDatetime.from_ical('20120311T015959', 'America/Denver')
        self.assertEqual(dat.strftime('%Y%m%d%H%M%S %z'),
                         '20120311015959 -0700')

        # After transition to DST
        dat = vDatetime.from_ical('20120311T030000', 'America/Denver')
        self.assertEqual(dat.strftime('%Y%m%d%H%M%S %z'),
                         '20120311030000 -0600')

        dat = vDatetime.from_ical('20101010T000000', 'Europe/Vienna')
        self.assertEqual(vDatetime(dat).to_ical(), b'20101010T000000')

    def test_prop_vDuration(self):
        from ..prop import vDuration

        self.assertEqual(vDuration(timedelta(11)).to_ical(), b'P11D')
        self.assertEqual(vDuration(timedelta(-14)).to_ical(), b'-P14D')
        self.assertEqual(
            vDuration(timedelta(1, 7384)).to_ical(),
            b'P1DT2H3M4S'
        )
        self.assertEqual(vDuration(timedelta(1, 7380)).to_ical(), b'P1DT2H3M')
        self.assertEqual(vDuration(timedelta(1, 7200)).to_ical(), b'P1DT2H')
        self.assertEqual(vDuration(timedelta(0, 7200)).to_ical(), b'PT2H')
        self.assertEqual(vDuration(timedelta(0, 7384)).to_ical(), b'PT2H3M4S')
        self.assertEqual(vDuration(timedelta(0, 184)).to_ical(), b'PT3M4S')
        self.assertEqual(vDuration(timedelta(0, 22)).to_ical(), b'PT22S')
        self.assertEqual(vDuration(timedelta(0, 3622)).to_ical(), b'PT1H0M22S')
        self.assertEqual(vDuration(timedelta(days=1, hours=5)).to_ical(),
                         b'P1DT5H')
        self.assertEqual(vDuration(timedelta(hours=-5)).to_ical(), b'-PT5H')
        self.assertEqual(vDuration(timedelta(days=-1, hours=-5)).to_ical(),
                         b'-P1DT5H')

        # How does the parsing work?
        self.assertEqual(vDuration.from_ical('PT1H0M22S'), timedelta(0, 3622))

        self.assertRaises(ValueError, vDuration.from_ical, 'kox')

        self.assertEqual(vDuration.from_ical('-P14D'), timedelta(-14))

        self.assertRaises(ValueError, vDuration, 11)

    def test_prop_vPeriod(self):
        from ..prop import vPeriod

        # One day in exact datetimes
        per = (datetime(2000, 1, 1), datetime(2000, 1, 2))
        self.assertEqual(vPeriod(per).to_ical(),
                         b'20000101T000000/20000102T000000')

        per = (datetime(2000, 1, 1), timedelta(days=31))
        self.assertEqual(vPeriod(per).to_ical(), b'20000101T000000/P31D')

        # Roundtrip
        p = vPeriod.from_ical('20000101T000000/20000102T000000')
        self.assertEqual(
            p,
            (datetime(2000, 1, 1, 0, 0), datetime(2000, 1, 2, 0, 0))
        )
        self.assertEqual(vPeriod(p).to_ical(),
                         b'20000101T000000/20000102T000000')

        self.assertEqual(vPeriod.from_ical('20000101T000000/P31D'),
                         (datetime(2000, 1, 1, 0, 0), timedelta(31)))

        # Roundtrip with absolute time
        p = vPeriod.from_ical('20000101T000000Z/20000102T000000Z')
        self.assertEqual(vPeriod(p).to_ical(),
                         b'20000101T000000Z/20000102T000000Z')

        # And an error
        self.assertRaises(ValueError,
                          vPeriod.from_ical, '20000101T000000/Psd31D')

        # Timezoned
        dk = pytz.timezone('Europe/Copenhagen')
        start = dk.localize(datetime(2000, 1, 1))
        end = dk.localize(datetime(2000, 1, 2))
        per = (start, end)
        self.assertEqual(vPeriod(per).to_ical(),
                         b'20000101T000000/20000102T000000')
        self.assertEqual(vPeriod(per).params['TZID'],
                         'Europe/Copenhagen')

        p = vPeriod((dk.localize(datetime(2000, 1, 1)), timedelta(days=31)))
        self.assertEqual(p.to_ical(), b'20000101T000000/P31D')

    def test_prop_vWeekday(self):
        from ..prop import vWeekday

        self.assertEqual(vWeekday('mo').to_ical(), b'MO')
        self.assertRaises(ValueError, vWeekday, 'erwer')
        self.assertEqual(vWeekday.from_ical('mo'), 'MO')
        self.assertEqual(vWeekday.from_ical('+3mo'), '+3MO')
        self.assertRaises(ValueError, vWeekday.from_ical, 'Saturday')
        self.assertEqual(vWeekday('+mo').to_ical(), b'+MO')
        self.assertEqual(vWeekday('+3mo').to_ical(), b'+3MO')
        self.assertEqual(vWeekday('-tu').to_ical(), b'-TU')

    def test_prop_vFrequency(self):
        from ..prop import vFrequency

        self.assertRaises(ValueError, vFrequency, 'bad test')
        self.assertEqual(vFrequency('daily').to_ical(), b'DAILY')
        self.assertEqual(vFrequency('daily').from_ical('MONTHLY'), 'MONTHLY')

    def test_prop_vRecur(self):
        from ..prop import vRecur

        # Let's see how close we can get to one from the rfc:
        # FREQ=YEARLY;INTERVAL=2;BYMONTH=1;BYDAY=SU;BYHOUR=8,9;BYMINUTE=30

        r = dict({'freq': 'yearly', 'interval': 2})
        r.update({
            'bymonth': 1,
            'byday': 'su',
            'byhour': [8, 9],
            'byminute': 30
        })
        self.assertEqual(
            vRecur(r).to_ical(),
            b'FREQ=YEARLY;INTERVAL=2;BYMINUTE=30;BYHOUR=8,9;BYDAY=SU;BYMONTH=1'
        )

        r = vRecur(FREQ='yearly', INTERVAL=2)
        r.update({
            'BYMONTH': 1,
            'BYDAY': 'su',
            'BYHOUR': [8, 9],
            'BYMINUTE': 30,
        })
        self.assertEqual(
            r.to_ical(),
            b'FREQ=YEARLY;INTERVAL=2;BYMINUTE=30;BYHOUR=8,9;BYDAY=SU;BYMONTH=1'
        )

        r = vRecur(freq='DAILY', count=10)
        r['bysecond'] = [0, 15, 30, 45]
        self.assertEqual(r.to_ical(),
                         b'FREQ=DAILY;COUNT=10;BYSECOND=0,15,30,45')

        r = vRecur(freq='DAILY', until=datetime(2005, 1, 1, 12, 0, 0))
        self.assertEqual(r.to_ical(), b'FREQ=DAILY;UNTIL=20050101T120000')

        # How do we fare with regards to parsing?
        r = vRecur.from_ical('FREQ=DAILY;INTERVAL=2;COUNT=10')
        self.assertEqual(r,
                         {'COUNT': [10], 'FREQ': ['DAILY'], 'INTERVAL': [2]})
        self.assertEqual(
            vRecur(r).to_ical(),
            b'FREQ=DAILY;COUNT=10;INTERVAL=2'
        )

        r = vRecur.from_ical('FREQ=YEARLY;INTERVAL=2;BYMONTH=1;BYDAY=-SU;'
                             'BYHOUR=8,9;BYMINUTE=30')
        self.assertEqual(
            r,
            {'BYHOUR': [8, 9], 'BYDAY': ['-SU'], 'BYMINUTE': [30],
             'BYMONTH': [1], 'FREQ': ['YEARLY'], 'INTERVAL': [2]}
        )

        self.assertEqual(
            vRecur(r).to_ical(),
            b'FREQ=YEARLY;INTERVAL=2;BYMINUTE=30;BYHOUR=8,9;BYDAY=-SU;'
            b'BYMONTH=1'
        )

        # Some examples from the spec
        r = vRecur.from_ical('FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1')
        self.assertEqual(vRecur(r).to_ical(),
                         b'FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1')

        p = 'FREQ=YEARLY;INTERVAL=2;BYMONTH=1;BYDAY=SU;BYHOUR=8,9;BYMINUTE=30'
        r = vRecur.from_ical(p)
        self.assertEqual(
            vRecur(r).to_ical(),
            b'FREQ=YEARLY;INTERVAL=2;BYMINUTE=30;BYHOUR=8,9;BYDAY=SU;BYMONTH=1'
        )

        # and some errors
        self.assertRaises(ValueError, vRecur.from_ical, 'BYDAY=12')

    def test_prop_vText(self):
        from ..prop import vText

        self.assertEqual(vText(u'Simple text').to_ical(), b'Simple text')

        # Escaped text
        t = vText('Text ; with escaped, chars')
        self.assertEqual(t.to_ical(), b'Text \\; with escaped\\, chars')

        # Escaped newlines
        self.assertEqual(vText('Text with escaped\\N chars').to_ical(),
                         b'Text with escaped\\n chars')

        # If you pass a unicode object, it will be utf-8 encoded. As this is
        # the (only) standard that RFC 2445 support.
        t = vText(u'international chars \xe4\xf6\xfc')
        self.assertEqual(t.to_ical(),
                         b'international chars \xc3\xa4\xc3\xb6\xc3\xbc')

        # and parsing?
        self.assertEqual(vText.from_ical('Text \\; with escaped\\, chars'),
                         u'Text ; with escaped, chars')

        t = vText.from_ical('A string with\\; some\\\\ characters in\\it')
        self.assertEqual(t, "A string with; some\\ characters in\it")

        # We are forgiving to utf-8 encoding errors:
        # We intentionally use a string with unexpected encoding
        #
        self.assertEqual(vText.from_ical(b'Ol\xe9'), u'Ol\ufffd')

        # Notice how accented E character, encoded with latin-1, got replaced
        # with the official U+FFFD REPLACEMENT CHARACTER.

    def test_prop_vTime(self):
        from ..prop import vTime

        self.assertEqual(vTime(12, 30, 0).to_ical(), '123000')
        self.assertEqual(vTime.from_ical('123000'), time(12, 30))

        # We should also fail, right?
        self.assertRaises(ValueError, vTime.from_ical, '263000')

    def test_prop_vUri(self):
        from ..prop import vUri

        self.assertEqual(vUri('http://www.example.com/').to_ical(),
                         b'http://www.example.com/')
        self.assertEqual(vUri.from_ical('http://www.example.com/'),
                         'http://www.example.com/')

    def test_prop_vGeo(self):
        from ..prop import vGeo

        # Pass a list
        self.assertEqual(vGeo([1.2, 3.0]).to_ical(), '1.2;3.0')

        # Pass a tuple
        self.assertEqual(vGeo((1.2, 3.0)).to_ical(), '1.2;3.0')

        g = vGeo.from_ical('37.386013;-122.082932')
        self.assertEqual(g, (float('37.386013'), float('-122.082932')))

        self.assertEqual(vGeo(g).to_ical(), '37.386013;-122.082932')

        self.assertRaises(ValueError, vGeo, 'g')

    def test_prop_vUTCOffset(self):
        from ..prop import vUTCOffset

        self.assertEqual(vUTCOffset(timedelta(hours=2)).to_ical(), '+0200')

        self.assertEqual(vUTCOffset(timedelta(hours=-5)).to_ical(), '-0500')

        self.assertEqual(vUTCOffset(timedelta()).to_ical(), '+0000')

        self.assertEqual(vUTCOffset(timedelta(minutes=-30)).to_ical(),
                         '-0030')

        self.assertEqual(
            vUTCOffset(timedelta(hours=2, minutes=-30)).to_ical(),
            '+0130'
        )

        self.assertEqual(vUTCOffset(timedelta(hours=1, minutes=30)).to_ical(),
                         '+0130')

        # Support seconds
        self.assertEqual(vUTCOffset(timedelta(hours=1,
                                              minutes=30,
                                              seconds=7)).to_ical(), '+013007')

        # Parsing

        self.assertEqual(vUTCOffset.from_ical('0000'), timedelta(0))
        self.assertEqual(vUTCOffset.from_ical('-0030'), timedelta(-1, 84600))
        self.assertEqual(vUTCOffset.from_ical('+0200'), timedelta(0, 7200))
        self.assertEqual(vUTCOffset.from_ical('+023040'), timedelta(0, 9040))

        self.assertEqual(vUTCOffset(vUTCOffset.from_ical('+0230')).to_ical(),
                         '+0230')

        # And a few failures
        self.assertRaises(ValueError, vUTCOffset.from_ical, '+323k')

        self.assertRaises(ValueError, vUTCOffset.from_ical, '+2400')

    def test_prop_vInline(self):
        from ..prop import vInline

        self.assertEqual(vInline('Some text'), 'Some text')
        self.assertEqual(vInline.from_ical('Some text'), 'Some text')

        t2 = vInline('other text')
        t2.params['cn'] = 'Test Osterone'
        self.assertIsInstance(t2.params, Parameters)
        self.assertEqual(t2.params, {'CN': 'Test Osterone'})

    def test_prop_TypesFactory(self):
        from ..prop import TypesFactory

        # To get a type you can use it like this.
        factory = TypesFactory()
        datetime_parser = factory['date-time']
        self.assertEqual(datetime_parser(datetime(2001, 1, 1)).to_ical(),
                         b'20010101T000000')

        # A typical use is when the parser tries to find a content type and use
        # text as the default
        value = '20050101T123000'
        value_type = 'date-time'
        self.assertEqual(factory.get(value_type, 'text').from_ical(value),
                         datetime(2005, 1, 1, 12, 30))

        # It can also be used to directly encode property and parameter values
        self.assertEqual(
            factory.to_ical('comment', u'by Rasmussen, Max M\xfcller'),
            b'by Rasmussen\\, Max M\xc3\xbcller'
        )
        self.assertEqual(factory.to_ical('priority', 1), b'1')
        self.assertEqual(factory.to_ical('cn', u'Rasmussen, Max M\xfcller'),
                         b'Rasmussen\\, Max M\xc3\xbcller')
        self.assertEqual(
            factory.from_ical('cn', b'Rasmussen\\, Max M\xc3\xb8ller'),
            u'Rasmussen, Max M\xf8ller'
        )


class TestPropertyValues(unittest.TestCase):

    def test_vDDDLists_timezone(self):
        """Test vDDDLists with timezone information.
        """
        from .. import Event
        vevent = Event()
        at = pytz.timezone('Europe/Vienna')
        dt1 = at.localize(datetime(2013, 1, 1))
        dt2 = at.localize(datetime(2013, 1, 2))
        dt3 = at.localize(datetime(2013, 1, 3))
        vevent.add('rdate', [dt1, dt2])
        vevent.add('exdate', dt3)
        ical = vevent.to_ical()

        self.assertTrue(
            b'RDATE;TZID=Europe/Vienna:20130101T000000,20130102T000000' in ical
        )
        self.assertTrue(b'EXDATE;TZID=Europe/Vienna:20130103T000000' in ical)
