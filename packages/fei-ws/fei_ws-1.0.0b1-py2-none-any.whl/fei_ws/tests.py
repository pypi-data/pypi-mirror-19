import codecs
import unittest
from datetime import datetime
import sys

from clients import FEIWSClient10, FEIWSClient


class FEIWSClientTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = FEIWSClient()

    def test_findAthlete_by_id(self):
        result = self.client.findAthlete(FEIIDs=[10000412])
        self.assertEqual(result.AthleteOC[0]['Firstname'], 'Jeroen')

    def test_findAthlete_by_name(self):
        result = self.client.findAthlete(FirstName='Jeroen', FamilyName='Dubbeldam ')
        self.assertEqual(result.AthleteOC[0]['Firstname'], 'Jeroen')

    def test_commonws_without_argument(self):
        self.client._common_data.clear()
        result = self.client.get_common_data('getVersion')
        self.assertEqual(result, '2.77.6')

    def test_commonws_caching(self):
        self.client._common_data['getVersion'] = 'arie'
        result = self.client.get_common_data('getVersion')
        self.assertEqual(result, 'arie')

    def test_commonws_with_argument(self):
        result = self.client.get_common_data('getSeasonList', DisciplineCode='S')
        self.assertTrue(result.getSeasonListResult)

    def test_findHorse_by_id(self):
        result = self.client.findHorse(FEIIDs=['NED08021'])
        self.assertEqual(result.HorseOC[0]['BirthName'], 'TOTILAS')

    def test_findHorse_by_name(self):
        result = self.client.findHorse(Name='TOTILAS')
        self.assertEqual(result.HorseOC[0]['BirthName'], 'TOTILAS')

    def test_findEvent_by_id(self):
        result = self.client.findEvent(ID="2012_CI_0209")
        self.assertEqual(result.ShowOC[0].ShowID, "2012_CI_0209")

    def test_findEvent_by_venue_and_start(self):
        result = self.client.findEvent(VenueName="Aachen",
                                  ShowDateFrom=datetime(2013, 6, 25))
        self.assertEqual(result.ShowOC[0].ShowID, "2013_CI_0051")

    def test_findOfficial_by_ID(self):
        result = self.client.findOfficial(AnyID="10050465")
        self.assertEqual(result.PersonOfficialOC[0].FamilyName, 'VAN DIJK')
        self.assertEqual(result.PersonOfficialOC[0].FirstName, 'Joop')

    def test_findOfficial_by_Name(self):
        result = self.client.findOfficial(AnyName='VAN DIJK')
        joop = filter(lambda x: x.FirstName =='Joop', result.PersonOfficialOC)[0]
        self.assertEqual(joop.PersonFEIID, 10050465)

class FEIWSClient10TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = FEIWSClient10()

    def test_getVenueList(self):
        self.assertTrue(self.client.getVenueList().Venue)

    def test_getShowTypeList(self):
        self.assertTrue(self.client.getShowTypeList().ShowType)

    def test_getShowRegionList(self):
        self.assertTrue(self.client.getShowRegionList().ShowRegion)

    def test_searchForShow(self):
        #TODO: Test other search criteria
        result = self.client.searchForShow(Venue='Aachen',
                                           DateStart=datetime(2013,1,1),
                                           DateEnd=datetime(2013, 12, 12))
        self.assertEqual(len(result.Show), 2)
        self.assertEqual(result.Show[0].Venue, 'Aachen')

    def test_getEventsByShowCode(self):
        result = self.client.getEventsByShowCode('2013_CH-EU_0001')
        self.assertEqual(result.Event[0].ShowCode, '2013_CH-EU_0001')

    def test_getVersion(self):
        result = self.client.getVersion()
        self.assertEqual(result, '2.77.6')

    def test_getShow(self):
        result = self.client.getShow('2013_CH-EU_0001')
        self.assertEqual(result.Venue, 'Herning')

    def test_getShows(self):
        result = self.client.getShows(('2013_CH-EU_0001', '2012_CI_0209'))
        self.assertEqual(len(result.Show), 2)

    def test_getEventTypeCodeList(self):
        self.assertTrue(self.client.getEventTypeCodeList())

    def test_getEvent(self):
        result = self.client.getEvent('2013_CH-EU_0001_S_S_01')
        self.assertEqual(result.EventTypeCode, "CH-EU-S")

    def test_getEvents(self):
        result = self.client.getEvents(('2013_CH-EU_0001_S_S_01',
                                       '2013_CH-EU_0001_S_S_02'))
        self.assertEqual(len(result.Event), 2)

    def test_searchForEvent(self):
        #TODO: Test other search criteria
        result = self.client.searchForEvent(Venue='Aachen',
                                            DateStart=datetime(2013,1,1),
                                            DateEnd=datetime(2013, 12, 12))
        self.assertEqual(len(result.Event), 8)

    def test_getEventResults(self):
        self.assertTrue(self.client.getEventResults('2013_CH-EU_0001_S_S_01'))

    def test_getCompetitionsByEventCode(self):
        result = self.client.getCompetitionsByEventCode(
            '2013_CH-EU_0001_S_S_01')
        self.assertEqual(len(result.Competition), 5)

    def test_getCompetition(self):
        result = self.client.getCompetition(
            '2013_CH-EU_0001_S_S_01_01')
        self.assertTrue(result)

    def test_getCompetitions(self):
        result = self.client.getCompetitions(
                ('2013_CH-EU_0001_S_S_01_01',
                 '2013_CH-EU_0001_S_S_01_02')
            )
        self.assertEqual(len(result.Competition), 2)

    def test_getCompetitionResults(self):
        result = self.client.getCompetitionResults('2013_CH-EU_0001_S_S_01_01')
        self.assertTrue(result.NFResult)

    def test_getPerson(self):
        result = self.client.getPerson(10000412)
        self.assertEqual(result['FirstName'], 'Jeroen')

    def test_searchForPerson(self):
        #TODO: Test other search criteria
        result = self.client.searchForPerson(Name='Dubbeldam')
        self.assertEqual(result.Person[0].FirstName, 'Jeroen')
        result = self.client.searchForPerson(Name='Dubbeldam', ID=10000412,
                                             Gender='Male', CompetingFor='NED')
        self.assertEqual(result.Person[0].FirstName, 'Jeroen')

    def test_getPersons(self):
        result = self.client.getPersons((10002647, 10001784, 10011424))
        self.assertEqual(len(result.Person), 3)
        self.assertEqual(result.Person[0].FamilyName, 'WHITAKER')

    def test_getCompetitorHorses(self):
        result = self.client.getCompetitorHorses(10000412)
        self.assertTrue(result.Horse)

    def test_getCompetitorsHorses(self):
        result = self.client.getCompetitorsHorses((10002647, 10001784))
        self.assertEqual(len(result.CompetitorHorses), 2)

    def test_getHorseColorList(self):
        self.assertTrue(self.client.getHorseColorList().HorseColor)

    def test_getStudBookList(self):
        studbooks = self.client.getStudBookList().StudBook
        my_list = []
        f = codecs.open('my_test.py', 'w', 'utf-8')
        for sb in studbooks:
            f.write(u'(u"{0}", u"{1}"),\n'.format(sb.Code, sb.Name))
        # f.write(",\n".join(my_list))
        f.flush()
            #my_list.append((unicode(sb.Code), unicode(sb.Name)))
        #f.write(my_list.__repr__())
        self.assertTrue(self.client.getStudBookList().StudBook)

    def test_searchForHorse(self):
        #TODO test other search criteria
        result = self.client.searchForHorse(ID='NED08021')
        self.assertEqual(result.Horse[0].CurrentName, 'TOTILAS')

    def test_getHorse(self):
        result = self.client.getHorse('NED08021')
        self.assertEqual(result.CurrentName, 'TOTILAS')

    def test_getHorses(self):
        result = self.client.getHorses(('NED08021', '104CF32'))
        self.assertEqual(len(result.Horse), 2)

    def test_getHorseOwner(self):
        result = self.client.getHorseOwner('NED08021')
        self.assertTrue(result)

    def test_getHorseCompetitors(self):
        result = self.client.getHorseCompetitors('NED08021')
        self.assertTrue(result.Person)

    def test_getHorsesCompetitors(self):
        result = self.client.getHorsesCompetitors(('NED08021', '104CF32'))
        self.assertTrue(result.HorseCompetitors)

if __name__ == '__main__':
    unittest.main()
