import cProfile
import pstats
import flickrapi, os, json, time, sys
from flickrapi.exceptions import FlickrError
import pandas as pd
from dotenv import load_dotenv
from typing import Union, Dict, List
from threading import Thread

attributes=[]

def g_info_t(pic,flickr,album_title, a_id):
    photo_id = pic['id']
    try:
        photo_info = flickr.photos.getInfo(photo_id=photo_id)
        photo_info = photo_info ['photo']
    except FlickrError as e:
        if 'Status code 500' in str(e):
            print(f"Encountered an error for photo_id {photo_id}: {e}. waiting 2 seconds and then trying again")
            time.sleep(2)
            try:
                photo_info = flickr.photos.getInfo(photo_id=photo_id)
                photo_info = photo_info ['photo']
            except Exception as e:
                print(f"Mulitple Errors lets stop")
                print(f"ending program")
                sys.exit(1)
        else:
            print(f"Encountered an error for photo_id {photo_id}: {e}. Skipping this photo. waiting 2 seconds and then trying again")
            time.sleep(2)
            try:
                photo_info = flickr.photos.getInfo(photo_id=photo_id)
                photo_info = photo_info ['photo']
            except Exception as e:
                print(f"Mulitple Errors lets stop")
                print(f"ending program")
                sys.exit(1)
    except Exception as e:
        print(f"Worker caught an unknown exception: {e}")
        print(f"ending program")
        sys.exit(1)

    title = photo_info['title']['_content']
    description = photo_info['description']['_content']
    url = f"https://www.flickr.com/photos/fractracker/{photo_id}/in/album-{a_id}"
    dt=photo_info['dates']['taken']
    latitude = None
    longitude = None
    if 'location' in photo_info:
        location_info = photo_info['location']
        if 'latitude' in location_info and 'longitude' in location_info:
            latitude = location_info['latitude']
            longitude = location_info['longitude']
            attributes.append({'PhotoID': photo_id,'Title': title, 'Date_taken': dt,'Description': description,'URL': url,
                'Latitude': latitude,'Longitude': longitude,'AlbumID': a_id,'AlbumTitle': album_title})

def get_pic_info(photos, flickr, album_title, a_id):
    teds=[]
    for pic in photos['photoset']['photo']:
        t =Thread(target=g_info_t, args=(pic,flickr,album_title, a_id))
        t.start()
        teds.append(t)
    for i in teds: i.join()

def album_pull(flickr, album_ids):
    for a_id in album_ids:
        pg_start, pg_end, per_page = 1, 1, 500
        photos : JSONObject = flickr.photosets.getPhotos(photoset_id=a_id, page=pg_start, per_page=per_page)
        for pg in range(1, photos['photoset']['pages']+1):
            print(f"ON page {pg=} of album id {photos['photoset']['id']}")
            if pg!=1: photos : JSONObject = flickr.photosets.getPhotos(photoset_id=a_id, page=pg, per_page=per_page)
            print(f"\t On this page of the album there are {len(photos['photoset']['photo'])}")
            album_title = photos['photoset']['title']
            start = time.time()
            get_pic_info(photos, flickr, album_title, a_id)
    end = time.time()
    elapsed = end - start
    elapsed_since_st = end - start_entire
    elapsed_since_st_MIN = elapsed_since_st/60
    print(f'\tTime taken for this page: {elapsed:.6f} seconds')
    print(f'\tTime taken since code start: {elapsed_since_st:.6f} seconds')
    print(f'\tTime taken since code start: {elapsed_since_st_MIN:.6f} min')

def main():
    print(f"Local folder defined env variables found?.... {load_dotenv()=}")
    JSONVal = Union[str, int, 'JSONArray', 'JSONObject']
    JSONArray = List[JSONVal]
    JSONObject = Dict[str, JSONVal]
    secret : str = os.getenv('SECRET')
    key : str = os.getenv('KEY')
    USER_NAME : str = os.getenv('ORG_USER_NAME')
    flickr : flickr.FlickrAPI = flickrapi.FlickrAPI(key, secret, format='parsed-json')
    user_info : JSONObject = flickr.people.findByUsername(username=USER_NAME)
    user_id : str = user_info['user']['id']
    photosets : JSONObject = flickr.photosets.getList(user_id=user_id)
    album_ids : List[str] = [albumMetaData['id'] for albumMetaData in photosets['photosets']['photoset']]
#    album_ids = album_ids[-4:-2]

    with cProfile.Profile() as pr:
        album_pull(flickr, album_ids) 

    with open('thread_data_pull.p.json', 'w') as file: json.dump(attributes, file, indent=4)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename='needs_profiling.prof')

if __name__ == "__main__": 
    start_entire = time.time()
    main()
    end_entire = time.time()
    elapsed_entire = end_entire - start_entire
    print(f'Time taken for this entire script: {elapsed_entire:.6f} seconds')
