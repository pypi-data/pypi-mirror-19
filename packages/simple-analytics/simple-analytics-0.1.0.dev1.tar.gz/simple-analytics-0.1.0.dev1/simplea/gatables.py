import urllib.parse

from googleapiclient.errors import HttpError  
from googleapiclient import sample_tools  
from oauth2client.service_account import ServiceAccountCredentials as SAC
from httplib2 import Http  
from apiclient.discovery import build

from simplea.utils import add_suffix

class GATable(object):
    
    def __init__(self, table_id, start_date, end_date, 
            metrics, sampling_level="FASTER"):
        self.table_id = table_id
        # start and end dates in the format YYYY-MM-DD
        self.start_date = start_date
        self.end_date = end_date
        # comma separated list of analytics metrics (no ga: suffix required)
        self.metrics = metrics
        
        self.dims = None # dimensions
        self.filters = None
        self.sampling_level = sampling_level
        self.sort = None
        self.service = None

        return

    def initialize(self, keyfile):
        # Authenticate and create the service for the Core Reporting API
        credentials = SAC.from_json_keyfile_name(keyfile,
                  ['https://www.googleapis.com/auth/analytics.readonly'])
        http_auth = credentials.authorize(Http())  
        self.service = build('analytics', 'v3', http=http_auth)  
        return

    def adjust_dates(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        return self

    def filter(self, filters):
        # if existing filters exists, append
        if self.filters is not None and self.filters != filters:
            self.filters += "," + filters
        else:
            self.filters = filters
        return self

    def set_dims(self, dims):
        """set dimensions (dims short for dimensions)."""
        if self.dims is not None and self.dims != dims:
            self.dims += "," + dims
        else:
            self.dims = dims
        return self

    def order_by(self, sort):
        if self.sort is not None and self.sort != sort:
            self.sort += "," + sort
        else:
            self.sort = sort
        return self

    def get_query(self, max_results):
        return self.service.data().ga().get(
                ids=add_suffix(self.table_id, "ga:"), start_date=self.start_date,
                end_date=self.end_date, metrics=add_suffix(self.metrics, "ga:"),
                dimensions=add_suffix(self.dims, "ga:"),
                sort=add_suffix(self.sort, "ga:"),
                filters=add_suffix(self.filters, "ga:"), max_results=max_results,)

    def get_response(self, max_results):
        return self.get_query(max_results).execute()

    def get(self, max_results):
        return self.get_response(max_results)["rows"]
