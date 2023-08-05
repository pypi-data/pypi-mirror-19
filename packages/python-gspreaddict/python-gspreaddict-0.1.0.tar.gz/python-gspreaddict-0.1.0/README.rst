~~~~~~~~~~~
gspreaddict
~~~~~~~~~~~

Google spreadsheet as dictionary list. read-only.

Preparation
===========

Google API Console
------------------

Make credentials on Google spreadsheet.

https://console.developers.google.com/apis/dashboard

Credentials -> Create credentials -> Service account key

Download credential as JSON.



Google spreadsheet
------------------

Open google spreadsheet.

Share -> Input email in credential file

xxxxxxxxxxxx@appspot.gserviceaccount.com


Usage
=====

::

    from gspreaddict import GSpreadDict

    class TestRecord(GSpreadDict):
        spreadsheet_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        credentials_json_path = os.path.join(
            os.path.dirname(__file__), "My Project-xxxxxxxx.json")

spreadsheet_key is in Google spreadsheet URL.

credentials_json_path is downloaded Json credentials path.

Get instances,

::

    record = TestRecord.objects.get(key=value))

::

    record = TestRecord.objects.get(lambda x: x['key'] == value)

Caching
=======

::

    from django.core.cache import caches

    class TestRecord(GSpreadDict):
        spreadsheet_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        credentials_json_path = os.path.join(
            os.path.dirname(__file__), "My Project-xxxxxxxx.json")

    @classmethod
    def cache_set(cls, key, value):
        caches['gspreaddict'].set(key, value)

    @classmethod
    def cache_get(cls, key):
        return caches['gspreaddict'].get(key)

Override cache_set and cache_get classmethods.
