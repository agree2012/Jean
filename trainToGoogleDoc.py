import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


CREDENTIALS_FILE = '/var/lib/jenkins/workspace/DevopsTest/Jean_bot/TestGoogleDoSlack-b47c81f96c6e.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',                                                                                  'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

def create_table(date,row,column):
    CREDENTIALS_FILE = 'TestGoogleDoSlack-b47c81f96c6e.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',                                                                                  'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
    spreadsheet = service.spreadsheets().create( body = {
      'properties': {'title': 'Slackbot table', 'locale': 'ru_RU'},
       'sheets': [{'properties': {'sheetType': 'GRID',
                              'sheetId': 0,
                             'title': date,
                             'gridProperties': {'rowCount': row, 'columnCount': column }}}]
    }).execute()

    driveService = apiclient.discovery.build('drive', 'v3', http=httpAuth)
    shareRes = driveService.permissions().create(
        fileId=spreadsheet['spreadsheetId'],
        body={'type': 'anyone', 'role': 'reader'},
        fields='id'
    ).execute()

    results = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet['spreadsheetId'], body={
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": 0,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": 1

                    },
                    "properties": {
                        "pixelSize": 150
                    },
                    "fields": "pixelSize"
                }
            },

            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": 0,
                        "dimension": "COLUMNS",
                        "startIndex": 1,
                        "endIndex": 4
                    },
                    "properties": {
                        "pixelSize": 350
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }).execute()

    #results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet['spreadsheetId'], body={
    #    "valueInputOption": "USER_ENTERED",
    #    "data": [
    #        {"range": date + "!A1:D1",
    #         "majorDimension": "ROWS",
    #         "values": [
    #             [questions]]}
    #    ]
    #}).execute()

#spreadsheet = {u'spreadsheetId': u'1QzRrV1Y1GY3WAedIrDvDPAznxzz8ClLPfmYuoTNOXsk', u'properties': {u'locale': u'ru_RU', u'timeZone': u'Etc/GMT', u'autoRecalc': u'ON_CHANGE', u'defaultFormat': {u'padding': {u'top': 2, u'right': 3, u'left': 3, u'bottom': 2}, u'textFormat': {u'foregroundColor': {}, u'bold': False, u'strikethrough': False, u'fontFamily': u'arial,sans,sans-serif', u'fontSize': 10, u'italic': False, u'underline': False}, u'verticalAlignment': u'BOTTOM', u'backgroundColor': {u'blue': 1, u'green': 1, u'red': 1}, u'wrapStrategy': u'OVERFLOW_CELL'}, u'title': u'Evening ask'}, u'sheets': [{u'properties': {u'sheetType': u'GRID', u'index': 0, u'sheetId': 0, u'gridProperties': {u'columnCount': 4, u'rowCount': 20}, u'title': u'12.10.2017'}}], u'spreadsheetUrl': u'https://docs.google.com/spreadsheets/d/1QzRrV1Y1GY3WAedIrDvDPAznxzz8ClLPfmYuoTNOXsk/edit'}


#request = request.execute()

    driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
    shareRes = driveService.permissions().create(
        fileId = spreadsheet['spreadsheetId'],
        body = {'type': 'anyone', 'role': 'reader'},
        fields = 'id'
    ).execute()


    results = service.spreadsheets().batchUpdate(spreadsheetId = spreadsheet['spreadsheetId'], body = {
    "requests": [
        {
        "updateDimensionProperties": {
            "range": {
            "sheetId": 0,
            "dimension": "COLUMNS",
            "startIndex": 0,
            "endIndex": 1

            },
            "properties": {
            "pixelSize": 150
            },
            "fields": "pixelSize"
        }
        },

     {
          "updateDimensionProperties": {
            "range": {
            "sheetId": 0,
            "dimension": "COLUMNS",
            "startIndex": 1,
            "endIndex": 4
            },
            "properties": {
            "pixelSize": 350
            },
            "fields": "pixelSize"
        }
        }
    ]
    }).execute()
    return results
#spreadsheet = service.spreadsheets().create( body = {
 #  'properties': {'title': 'Evening ask', 'locale': 'ru_RU'},
 #   'sheets': [{'properties': {'sheetType': 'GRID',
 #                              'sheetId': 3,
 #                             'title': '19.10.2017',
 #                             'gridProperties': {'rowCount': 20, 'columnCount': 4}}}]


 #   results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheet['spreadsheetId'], body = {
 #           "valueInputOption": "USER_ENTERED",
 #        "data": [
 #            {"range": date+"!A1:D1",
 #               "majorDimension": "ROWS",
 #            "values": [["Name Person", "What Person do today?","What Person will be do tommorow?", "External information"]]}
 #           ]
 #       }).execute()
 #   return spreadsheet



def write_his_answer(spreadsheetId,date,range,values):
    service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": date + "!" + range,
            "values": [values]}
        ]
    }).execute()
    if(range != 'A1'):
        ranges = date + "!" + range
        include_grid_data = False
        result = service.spreadsheets().get(spreadsheetId=spreadsheetId, ranges=ranges, includeGridData=include_grid_data).execute()
        return result["sheets"][0]["properties"]["sheetId"]


def add_sheet(spreadsheetId,row,column,tittle):
    result = service.spreadsheets().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "requests": [
           {
                "addSheet": {
                    "properties": {
                        "title": tittle,
                      "gridProperties": {
                            "rowCount": row,
                            "columnCount": column
                    }
                  }
                }
            }
        ]
    }).execute()
    resultvalue = result["replies"][0]["addSheet"]["properties"]["sheetId"]
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": result['replies'][0]['addSheet']['properties']['sheetId'],
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": column
                    },
                    "properties": {
                        "pixelSize": 300
                    },
                    "fields": "pixelSize"
                }
            }
    ]
    }).execute()
    return resultvalue
