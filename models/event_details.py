from google.appengine.ext import ndb


class EventDetails(ndb.Model):
    """
    EventsDetails contains aggregate details about an event that tends to
    update often throughout an event. This includes rankings, event stats, etc.
    key_name is the event key, like '2010ct'
    """
    alliance_selections = ndb.JsonProperty()  # Formatted as: [{'picks': [captain, pick1, pick2, 'frc123', ...], 'declines':[decline1, decline2, ...] }, {'picks': [], 'declines': []}, ... ]
    district_points = ndb.JsonProperty()
    matchstats = ndb.JsonProperty()  # for OPR, DPR, CCWM, etc.
    rankings = ndb.JsonProperty()

    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    def __init__(self, *args, **kw):
        # store set of affected references referenced keys for cache clearing
        # keys must be model properties
        self._affected_references = {
            'key': set(),
        }
        super(EventDetails, self).__init__(*args, **kw)

    @property
    def alliance_teams(self):
        """
        Load a list of team keys playing in elims
        """
        alliances = self.alliance_selections
        if alliances is None:
            return []
        teams = []
        for alliance in alliances:
            for pick in alliance['picks']:
                teams.append(pick)
        return teams

    @property
    def key_name(self):
        return self.key.id()