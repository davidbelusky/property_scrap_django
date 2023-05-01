# Real estate scrap API

## Requirements:
- Python3

## Startup:
- Install python packages `pip3 install requirements.txt`
- Run django API server `python3 manage.py runserver`


## Info:
App can scrap clean and store into DB properties data from `www.slnecnice.sk` and `www.yit.sk` 

Server is running on `http://localhost:8000/`

## Endpoints:

### `/update-properties/`
**POST** `/update-properties/` - Download properties data filter and clean them, then store cleaned data into DB

### `/properties/`
**GET** `/properties/` - Show all properties in DB, for this endpoint can be used filters below


**Filters:**
`"id": ["exact"], "available": ["exact"], "source": ["iexact"]`

for ex. 
`/properties?available=true` will show available properteis (availabilty means that property was in data during last `update-properties`)

**Ordering:** For this endpoint is also available to use `ordering` ex. `properties?available=false&ordering=-created_date`


### `/properties/<int:pk>`
**GET** - `/properties/<id>` Get specific property based on ID

**POST** - `/properties/` Add property into DB

**Input Body:** 
```
{
    "source": "custom",
    "source_id": "1223s",
    "available": false,
    "apartment_type": "byt",
    "rooms": "2",
    "floor": "3",
    "area_size": 75,
    "area_total_size": 150,
    "price": 180000,
    "update_date":"2023-04-28T11:30:23.372148"
}
```
**DELETE** - `/properties/<id>` Delete property from DB based on ID


