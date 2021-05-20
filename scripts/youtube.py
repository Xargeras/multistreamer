from datetime import datetime
import os
import json

import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


scopes = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"]


def get_user_credentials(user):
    credentials = None
    api_service_name = "youtube"
    api_version = "v3"

    USER_TOKEN_FILE = './scripts/client_tokens/' + 'client_token_' + str(user) + '.json'
    if os.path.exists(USER_TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(USER_TOKEN_FILE, scopes)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('./scripts/client_secrets.json', scopes)
            credentials = flow.run_local_server(port=4000)
        with open(USER_TOKEN_FILE, 'w') as token:
            token.write(credentials.to_json())
    #youtube = build(api_service_name, api_version, credentials=credentials)
    return credentials.to_json()


def start_broadcast(youtube, settings):
    time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    #print(time)
    broadcast = youtube.liveBroadcasts().insert(
        part="snippet, status, contentDetails",
        body={
            "snippet": {
                "title": settings["title"],
                "scheduledStartTime": time,
                "description": settings["description"]
            },
            "status": {
                "privacyStatus": settings['privacy']
            },
            "contentDetails": {
                "enableAutoStart": "true",
                "enableAutoStop": "true"
            }
        }
    )

    response = broadcast.execute()
    return response


def start_stream(youtube, settings):
    stream = youtube.liveStreams().insert(
        part="snippet,cdn",
        body=dict(
            snippet=dict(
                title="start_stream"
            ),
            cdn=dict(
                resolution=settings["resolution"],
                frameRate="60fps",
                ingestionType='rtmp'
            )
        )
    )

    response = stream.execute()
    return response


def restart_stream(youtube):
    pass


def bind_broadcast(youtube, broadcast, stream):
    bind = youtube.liveBroadcasts().bind(
        part="id, contentDetails",
        id=broadcast["id"],
        streamId=stream["id"]
    )
    response = bind.execute()
    return response


def authorization(user):
    token = get_user_credentials(user)
    return token


def main(settings, user):
    if settings == None:
        settings = {
            "title": "Stream",
            "description": "Restream via Multistream https://multistream.io",
            "resolution": "1080p",
            "privacy": "public"
        }
    print(settings)
    youtube = get_user_credentials(user)
    broadcast = start_broadcast(youtube, settings)
    stream = start_stream(youtube, settings)
    bind_broadcast(youtube, broadcast, stream)
    key = stream["cdn"]["ingestionInfo"]["streamName"]
    return key
