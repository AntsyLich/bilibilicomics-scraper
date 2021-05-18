import requests
import json

def pathtourl(imgPath, headers):
    #A small helper which turns a Image path into a image link
    url = "https://www.bilibilicomics.com/twirp/comic.v1.Comic/ImageToken"
    res = requests.post(
            url, json.dumps({"urls": json.dumps([imgPath])}), headers = headers #ImagePath needs to be in a list.
        )
    data = json.loads(res.text)['data'][0]
    url = data['url'] + '?token=' + data['token']
    return url


class BilibiliComics():

    def __init__(self):
        #Necessary Headers
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.5",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://www.bilibilicomics.com",
            "referer": "https://www.bilibilicomics.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; rv:88.0) Gecko/20100101 Firefox/88.0",
            "cookie": ""
        }


    def comicdetails(self, comicID: int):
        #https://www.bilibilicomics.com/detail/mc{comicID}
        #Gets necessary details of the comic (title, description, author, etc.)
        #
        url = "https://www.bilibilicomics.com/twirp/comic.v2.Comic/ComicDetail"
        res = requests.post(
                url, json.dumps({"comic_id": comicID}), headers = self.headers 
            )
        data = json.loads(res.text)["data"]
        return data

    def getepisode(self, episodeID: int):
        #https://www.bilibilicomics.com/mc{comicID}/{episodeID}
        #Gets Episode Name and number (stored as str by short_title)
        
        url = "https://www.bilibilicomics.com/twirp/comic.v1.Comic/GetEpisode"
        res = requests.post(
                url, json.dumps({"id": episodeID}), headers = self.headers 
            )
        data = json.loads(res.text)["data"]
        return data

    def getepisodeimages(self, episodeID: int):
        #https://www.bilibilicomics.com/mc{comicID}/{episodeID}
        #Gets image path, height, width for every image in the episode
        url = "https://www.bilibilicomics.com/twirp/comic.v1.Comic/GetImageIndex"
        res = requests.post(
                url, json.dumps({"ep_id":episodeID}), headers = self.headers 
            )

        imagesData = json.loads(res.text)["data"]["images"]
        
        imagelinks = {}

        for i, dict in enumerate(imagesData):
            # "{path}@{width aka x}w.jpg"
            imagePath = "\"" + imagesData[i]["path"] + "@" + str(dict["x"]) + "w.jpg" + "\""


            imagelinks[str(int(i) + 1)] = pathtourl(imagePath, self.headers)

        return imagelinks
