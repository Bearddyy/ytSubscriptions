import youtube_dl
import youtubeApiInterface
import json
import pickle
import os
import requests
import datetime
from fake_useragent import UserAgent


ua = UserAgent()

#Set up fake borwser for getting google data
headers = {
    'User-Agent': ua['google chrome'],
    'referer':'https://www.google.com/',}
session = requests.Session()


def main():
    # Authenticate
    youtubeApiInterface.init()

    #check if subs list is pickled
    if os.path.exists('subs.pickle'):
        with open('subs.pickle', 'rb') as f:
            subscriptions = pickle.load(f)
    else:
        # Get list of subscriptions
        subscriptions = youtubeApiInterface.get_list_of_subscriptions()
        # Get next page of subscriptions
        while True:
            subs = youtubeApiInterface.get_next_subs()
            if subs is None:
                break
            subscriptions.extend(subs)
        #pickle subs list
        with open('subs.pickle', 'wb') as handle:
            pickle.dump(subscriptions, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #if the list of vidoes exists, load it
    allVideos = None
    if os.path.exists('allVideos.pickle'):
        #if the list of vidoes exists, check if it is from today
        print('Loading allVideos.pickle')
        date = os.path.getmtime('allVideos.pickle')
        if date > datetime.datetime.now().timestamp() - 86400:
            print('allVideos.pickle is from today, so load')
            with open('allVideos.pickle', 'rb') as f:
                allVideos = pickle.load(f)
    if allVideos is None:
        print('allVideos.pickle does not exist, or is from a different day, so create')
        allVideos = []
        # Download videos
        for subscription in subscriptions[0:10]:
            # Get channel ID
            channelId = subscription['snippet']['resourceId']['channelId']
            videos = youtubeApiInterface.get_channel_videos(channelId)
            #print(f"{channelName} : {len(videos)} videos")
            allVideos.extend(videos)
    
        # sort all videos by date
        allVideos.sort(key=lambda x: x['snippet']['publishedAt'], reverse=True)
        
        #pickle all videos
        with open('allVideos.pickle', 'wb') as handle:
            pickle.dump(allVideos, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    #print latest 100 videos
    for i in range(100):
        video = allVideos[i]
        title = video['snippet']['title']
        date = video['snippet']['publishedAt']
        print(f'{i+1}. {title} - {date}')


if __name__ == '__main__':
    main()

