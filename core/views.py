from django.shortcuts import render
import requests
from django.conf import settings
from isodate import parse_duration
from django.core.paginator import Paginator,  EmptyPage, PageNotAnInteger

def index(request):
	videos =[]

	if request.method == 'POST':
		search_url = 'https://www.googleapis.com/youtube/v3/search'
		video_url = 'https://www.googleapis.com/youtube/v3/videos'
		s_params ={
		'part' : 'snippet',
		'q': request.POST['search'],
		'type' : 'video',
		'key' : settings.YOUTUBE_DATA_API_KEY,
		'maxResults' : 12
		}

		

		r = requests.get(search_url, params=s_params)

		results = r.json()['items']

		video_ids = []
		channel_ids = []

		for result in results:
			video_ids.append(result['id']['videoId'])
			channel_ids.append(result['snippet']['channelId'])

		v_params ={
			'part' : 'snippet, contentDetails,statistics',
			'id' : ','.join(video_ids),
			'key' : settings.YOUTUBE_DATA_API_KEY,
			'maxResults' : 12
		}

		r= requests.get(video_url, params=v_params)
		results = r.json()['items']

		

		for result in results:
			video_data ={
				'title' : result['snippet']['title'],
				'id': (result['id']),
				'duration' : round(parse_duration(result['contentDetails']['duration']).total_seconds()/60, 2),
				'thumbnail' :result['snippet']['thumbnails']['high']['url'],
				'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
				'ch_url' : f"https://www.youtube.com/channel/{ result['snippet']['channelId'] }",
				'viewCount': result['statistics']['viewCount'],
				'ch_name' : result['snippet']['channelTitle'],
			}
			
			

			videos.append(video_data)

	context = {'videos': videos}

	return render(request, 'core/index.html', context)

		



