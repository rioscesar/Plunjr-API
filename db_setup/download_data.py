# {
#     "id": 21772,
#     "name": "Biggby Coffee Shop",
#     "street": "Michigan Avenue",
#     "city": "Dearborn",
#     "state": "Michigan",
#     "accessible": false,
#     "unisex": true,
#     "directions": "At the back of the coffee shop there is one restroom, one stall, non-gender-specific.  ",
#     "comment": "",
#     "latitude": null,
#     "longitude": null,
#     "created_at": "2016-05-01T21:48:30.765Z",
#     "updated_at": "2016-05-01T21:48:30.765Z",
#     "downvote": 0,
#     "upvote": 0,
#     "country": "US"
#   }
import json

import requests


def get_all_refugerestrooms():
    page = 1
    while True:
        responses = requests.get('http://www.refugerestrooms.org:80/api/v1/restrooms.json?page={}&per_page=99'.format(page)).json()
        if not responses:
            break
        for response in responses:
            if response['longitude'] and response['latitude']\
                    and response['street'] and response['city'] and response['state']:
                rating = ((response['upvote'] * 5) + response['downvote']) / \
                         ((response['upvote'] + response['downvote']) + (1
                          if (response['upvote'] + response['downvote']) == 0 else 0))
                payload = {
                    'lat': response['latitude'],
                    'lng': response['longitude'],
                    'name': response['name'],
                    'address': response['street'] + ', ' + response['city'] + ', ' + response['state'],
                    'rating': rating if rating > 0 else 3,
                    'description': response['comment'],
                    'title': response['directions'],
                    'user': 'Anonymous'
                }
                requests.post('http://104.130.132.153//api/reviews/', json=payload)
        page += 1

if __name__ == '__main__':
    # get_all_refugerestrooms()
    headers = {'content-type': 'application/json'}
    payload = {
        'imagesUrl': ['http://vignette2.wikia.nocookie.net/runescape2/images/1/14/Old_School_HUD.png']
    }
    # requests.patch('http://104.130.132.153/api/restrooms/1', data=json.dumps(payload), headers=headers)
    response = requests.patch('http://127.0.0.1:8000/api/restrooms/3', data=json.dumps(payload), headers=headers)
    a = response.status_code
