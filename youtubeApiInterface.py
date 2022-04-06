# -*- coding: utf-8 -*-

# Sample Python code for youtube.subscriptions.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import imp
import os
import pickle
import re
from tkinter import N

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from numpy import polyval

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


NEXT_PAGE_TOKEN = None
YOUTUBE = None

def init():
    global NEXT_PAGE_TOKEN
    global YOUTUBE
    api_service_name = "youtube"
    api_version = "v3"
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    YOUTUBE = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

def get_list_of_subscriptions():
    global NEXT_PAGE_TOKEN
    global YOUTUBE
   
    request = YOUTUBE.subscriptions().list(part='snippet', mine=True, maxResults=50, order='unread')
    response = request.execute()
    NEXT_PAGE_TOKEN = response['nextPageToken']
    return response['items']

def get_next_subs():
    global NEXT_PAGE_TOKEN
    global YOUTUBE
    if NEXT_PAGE_TOKEN is None:
        return None
    request = YOUTUBE.subscriptions().list(part='snippet', mine=True, maxResults=50, order='unread', pageToken=NEXT_PAGE_TOKEN)
    response = request.execute()
    if 'nextPageToken' in response:
        NEXT_PAGE_TOKEN = response['nextPageToken']
    else:
        NEXT_PAGE_TOKEN = None
    return response['items']
    

def get_channel_videos(channelId):
    global YOUTUBE
    # from the channelId get the uploads playlistId
    request = YOUTUBE.channels().list(part='contentDetails', id=channelId)
    response = request.execute()
    playlistId = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    # from the playlistId get the videos
    request = YOUTUBE.playlistItems().list(part='snippet', playlistId=playlistId, maxResults=50)
    response = request.execute()
    
    return response['items']