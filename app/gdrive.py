import os
import httplib2
from apiclient.discovery import build
from apiclient.http import MediaIoBaseDownload, MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from google.oauth2 import service_account
import googleapiclient.discovery


def get_credentials():
    SCOPES = "https://www.googleapis.com/auth/classroom.coursework.students https://www.googleapis.com/auth/classroom.courses https://www.googleapis.com/auth/classroom.push-notifications https://www.googleapis.com/auth/drive https://spreadsheets.google.com/feeds https://www.googleapis.com/auth/classroom.profile.emails"
    store = Storage('app/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('app/client_id.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return creds


def create_file(service, name, mimetype, parents='root'):
    file_metadata = {
        'name': name,
        'mimeType': mimetype,
        'parents': [parents]
    }
    search = fetch(" '{}' in parents and mimeType='{}' and name='{}'".format(parents, mimetype, name), sort='modifiedTime desc')
    print(search)
    if len(search) == 0:
        file = service.files().create(body=file_metadata, fields='id').execute()
        return '{}'.format(file.get('id'))
    else:
        return '{}'.format(search[0].get('id'))


def fetch(service, query, sort='modifiedTime desc'):
    results = service.files().list(
        q=query, orderBy=sort, pageSize=120, fields="nextPageToken, files(id, name, webViewLink)").execute()
    items = results.get('files', [])
    return items


def fetch_acl(service, file_id):
    results = service.permissions().list(fileId=file_id).execute()
    items = results.get('permissions', [])
    for perm in items:
        perm.get('id')
    return items


def share(service, file_id, email):
    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print(response.get('id'))
    batch = service.new_batch_http_request(callback=callback)
    user_permission = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': email
    }
    batch.add(service.permissions().create(
        fileId=file_id,
        sendNotificationEmail=False,
        body=user_permission,
        fields='id',
    ))
    batch.execute()
