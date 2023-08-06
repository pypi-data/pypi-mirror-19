import json
import csv


def json2csv(type, fp_in, fp_out, output_mode='w'):
    with open(fp_in) as i, open(fp_out, output_mode) as o:
        csvwriter = csv.writer(o)
        for line in i:
            if type == 'user':
                csvwriter.writerow(json2csv_user(line))


def json2csv_user(line):
    jline = json.loads(line)

    uid = jline.get('id_str')
    scn = jline.get('screen_name')
    is_verified = jline.get('verified')
    created_at = jline.get('created_at')
    location = jline.get('location').encode('utf-8')
    language = jline.get('lang')


    n_tweets = jline.get('statuses_count')
    n_following = jline.get('friends_count')
    n_followers = jline.get('followers_count')
    n_likes = jline.get('favourites_count')

    return [uid, scn, is_verified, created_at,
            location, language,
            n_tweets, n_following, n_followers, n_likes]
