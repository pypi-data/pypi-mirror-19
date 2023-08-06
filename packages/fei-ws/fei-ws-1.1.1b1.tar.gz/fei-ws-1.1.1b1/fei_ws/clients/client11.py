from base import FEIWSBaseClient

class FEIWSClient(FEIWSBaseClient):
    def __init__(self, username=None, password=None):
        super(FEIWSClient, self).__init__((1, 2), username, password)

    def findAthlete(self, FEIIDs=None,  FamilyName=None, FirstName=None,
                    GenderCode=None, CompetingFor=None):
        """Find athletes based on a certain search criteria.

        Params:
            FEIIDs: A tuple of Athlete FEI IDs you want to search for.
            FamilyName: The athlete's family name. Use % to create a `contain`
             query
            FirstNAme: The athlete's first name. User % to create a `contain`
             query
            GenderCode: The athlete gender(None=All, M=Male, F=Female)
            CompetingFor: The NOC code of the athlete's country he is competing
             for

        Return value: An array of Athlete objects.

        """
        fei_ids = None
        if FEIIDs:
            fei_ids = self._ows_client.factory.create('ArrayOfString')
            fei_ids.string = FEIIDs
        result = self._ows_client.service.findAthlete(
            FEIIDs=fei_ids, FamilyName=FamilyName, FirstName=FirstName,
            GenderCode=GenderCode, CompetingFor=CompetingFor)
        self._handle_messages(result)
        return result.findAthleteResult

    def findOfficial(self, AnyID=None, AnyName=None, PersonGender=None,
                     AdminNF=None, PersonStatus=None, OfficialFunction=None,
                     OfficialFunctionDiscipline=None):
        """Find officials based on a certain search criteria.

        Params:
            AnyID: Return officials having this ID, licence nr, or vet delegat nr.
            AnyName: Return officials having this family name, first name, nick name.
                use % to make a `contain` search.
            PersonGender: Return officials with this gender
            AdminNF: Return official that are member of the administrative NF
            PersonStatus: Return the official having this status:
                10: Search for all competitors
                1: Search only for active competitors
                0: Search only for inactive competitors
                2: Search only for pending competitors
                3: Search only for cancelled competitors
                9: Search only for suspended competitors.
            OfficialFunction: Search for officials with specified function
            OfficialFunctionDiscipline: Return officials having the specified official
                function for this discipline.

        Return value: An array of PersonOfficialOC objects

        """
        result = self._ows_client.service.findOfficial(
            AnyID=AnyID, AnyName=AnyName, PersonGender=PersonGender, AdminNF=AdminNF,
            PersonStatus=PersonStatus, OfficialFunction=OfficialFunction,
            OfficialFunctionDiscipline=OfficialFunctionDiscipline
        )
        self._handle_messages(result)
        return result.findOfficialResult

    def findHorse(self, FEIIDs=None, Name=None, SexCode=None, IsPony=None,
                  AthleteFEIID=None):
        """Find horses based on a certain search criteria.

        Params:
            FEIIDs: A tuple of Horse FEI IDs you want to search for.
            Name: The name of the horse. Use % to create a contain query
            SexCode: The sex code of the horse (None=All, F=Mare, G=Gelding,
                S=Stallion, M=Male Unknown, U=Unknown).
            IsPony: Boolean indicating to search for only ponies.
            AthleteFEIID: Search for horses associated with this Athlete.

        Return value: A list of Horse objects.

        """
        fei_ids = None
        if FEIIDs:
            fei_ids = self._ows_client.factory.create('ArrayOfString')
            fei_ids.string = FEIIDs
        result = self._ows_client.service.findHorse(
            FEIIDs=fei_ids, Name=Name, SexCode=SexCode, IsPony=IsPony,
            AthleteFEIID=AthleteFEIID)
        self._handle_messages(result)
        return result.findHorseResult

    def findEvent(self, ID='', ShowDateFrom=None, ShowDateTo=None,
                  VenueName='', NF='', DisciplineCode='', LevelCode='',
                  IsIndoor=None):
        """Find FEI events based on a certain search criteria.

        Params:
            ID: FEI show/event/competition ID.
            ShowDateFrom: Filter shows from this date up.
            ShowDateTo: Filter shows from this date down.
            VenueName: The name of the place where the show is held.
            NF: Country code of the national federation.
            DisciplineCode: Filter shows based on discipline.
            LevelCode: Filter shows based on level.
            IsIndoor: Filter indoor / outdoor shows.

        Return value: A list of FEI events

        """
        result = self._ows_client.service.findEvent(
            ID, ShowDateFrom, ShowDateTo, VenueName, NF, DisciplineCode,
            LevelCode, IsIndoor)
        self._handle_messages(result)
        return result.findEventResult

    def downloadResults(self, ID):
        """Download XML results from the FEI. (You need permission from the FEI
         to download results from an event.

        Params:
            ID: FEI event/competition ID.

        Return value: A string containing the information in FEI XML.

        """
        result = self._ows_client.service.downloadResults(ID)
        self._handle_messages(result)
        return result

    def uploadResults(self, ResultsXMLData):
        """Upload results to the FEI. (You need permission from the FEI to
        upload results to the FEI.

        Params:
            ResultsXMLData = Base64Encoded FEI result file.

        Return value:
            FileID = can be used to confirm uploaded results
            Results = String indicating if the uploaded succeeded.
                ERR = An error was found while processing the validation
                MAN = An error was found while processing the mandotory check
                OKW = It is ok for saving, but there are warnings
                OKD = the saving has been done

        """
        return self._ows_client.service.uploadResults(ResultsXMLData)

    def confirmUploadResults(self, FileID):
        """Confirm uploaded results. This is only needed when results returned
         OK with warnings.

        Params:
            FileID: The FileID return by the uploadResults routine.

        Return value: True if the saving has been done.

        """
        return self._ows_client.service.confirmUploadResults(FileID)

    def submitResults(self, ID):
        """Submit the results to the FEI validation for a given event or a
         given competition.

        Params:
            ID: FEI event/competition ID.

        Return value: True if the results have been successfully submitted.

        """
        return self._ows_client.service.submitResults(ID)
