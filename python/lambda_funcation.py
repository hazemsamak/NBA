from bs4 import BeautifulSoup
import requests
import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

site = "https://www.sport-video.org.ua"
URL = "https://www.sport-video.org.ua/basketball.html"

def lambda_handler(event, context):
    operation = event.get('operation')
    if operation == 'parse':
        print('Parse Movies List')
        return parseBasketballSite()
    else:
        return getJSONInDynamoDB()


def getExtraDetails(movie_url):
    r = requests.get(movie_url).text
    soup = BeautifulSoup(r, "html.parser")

    # Get poster image url
    poster = soup.find("div", {"id": "movie-poster"})
    img = poster.find('img')

    # Get IMDB reting details
    rating = {}
    ratings = soup.find_all("div", class_="rating-row")
    for r in ratings:
        if r.has_attr('itemprop'):
            link = r.find('a')['href']
            rate = r.find('span').text
            rating = {
                "link": link,
                "rate": rate
            }

    # Get torrents and mangnets URLs
    data = soup.find_all("div", class_="modal-torrent")
    torrents = []
    for t in data:
        quality = t.find('div').text
        # if quality != '1080p':
        #    continue
        qualitySize = t.find('p', class_="quality-size").text
        torrentURL = t.find('a', class_="download-torrent button-green-download2-big")['href']
        magentURL = t.find('a', class_="magnet-download download-torrent magnet")['href']
        torrent = {
            "quality": quality,
            "qualitySize": qualitySize,
            "torrent": torrentURL,
            "magnet": magentURL
        }
        torrents.append(torrent)

    extraDetails = {
        "image": img['src'],
        "torrents": torrents,
        "rating": rating
    }
    return extraDetails

def saveJSONInDynamoDB(movieList):
    string = json.dumps(movieList)
    # encoded_string = movieList.encode("utf-8")

    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('YTSMovies')
    response = dynamoTable.update_item(
        Key={
            'ID': 1
        },
        UpdateExpression="set MoviesJSON = :r , InsertDateTime=:p",
        ExpressionAttributeValues={
            ':r': string,
            ':p': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        ReturnValues="UPDATED_NEW"
    )

def getJSONInDynamoDB():
    print('Retrieve Movies list from DynamoDB')
    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('YTSMovies')
    try:
        response = dynamoTable.get_item(
            Key={
                'ID': 1
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print("GetItem succeeded, Movies list:")
        print(json.loads(item['MoviesJSON']))
        return json.loads(item['MoviesJSON'])

def parseBasketballSite():


    r = requests.get(URL).text
    soup = BeautifulSoup(r, "html.parser")
    count = 1

    match_list = []
    for link in soup.find_all('a'):
        match_url = link['href']
        if check_teams(match_url):
            match_details = get_match_details(match_url)
            match_list.append(match_details)

    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "list": match_list
    }
    matches = {
        "list": match_list
    }
    # saveJSONInDynamoDB(YTSMovies)
    print('Parse https://www.sport-video.org.ua site, and here is Matches List:')
    print(matches)
    return matches

def check_teams(link):
    teams = [
        "LA Clippers",
        "Los Angeles Lakers",
        "Golden State Warriors",
        "Toronto Raptors",
        "Philadelphia 76ers",
        "Milwaukee Bucks"
    ]

    for team in teams:
        if team in link:
            return True

    return False

def get_match_details(link):
    match = link[:link.index(".mkv")].split('/')[1]
    date = match[len(match) - 8 :]
    teams = match[:len(match) - 9].split('-')
    return {
        "team1": teams[0].strip(),
        "team2": teams[1].strip(),
        "date": date,
        "torrent": URL + '/.' + link
    }

def main():
    # TODO implement
    event = {
        'operation': 'parse'
    }
    operation = event.get('operation')
    if operation == 'parse':
        print('Parse Movies List')
        return parseBasketballSite()
    else:
        return getJSONInDynamoDB()



if __name__ == "__main__":
    main()



