# Travel Scrapper
Travel scrapper is an algorithm made for automatically checking for new flight prices. 

**Main pipeline**
- HTTP request for the Tequilla API is sent (kiwi.com)
- New flights are added to a PostgresSQL database
- Whenever a new cheaper flight appears on the radar, it sends a telegram message to the user

## Setup guide
Look at .env_example for the default pattern. Create a .env file on the tokens folder with the following:
- KIWI_TOKEN → your tequilla API token
- TELEGRAM_TOKEN →  token of the BOT that will send you telegram messages
- TELEGRAM_USER_ID → your telegram user number. Send a message to @get_my_telegram_chat_id_bot to check it by yourself
- POSTGRES_HOST, POSTGRES_DATABASE, POSTGRES_USER, POSTGRES_PASSWORD → self explanatory, these are your postgresSQL database credentials

After configuring everything on the .env file, you should run
```
apis/travel_api/travel_api_launcher.py
```

## Main endpoints

| Prefix | Endpoint | Tag | Type |
| ------ | ------ |  ------ |  ------ |
| http://localhost:8080/ | create_query | <query_tag> | POST
| http://localhost:8080/ | list_all_queries | _ | GET
| http://localhost:8080/| list_all_flights | _ | GET
| http://localhost:8080/ | refresh_db | _ | DELETE
| http://localhost:8080/ | run_all_queries | _ | POST

#### Create query
Creates a query that will be run by the run_all_queries function. Example below
```
{
	"fly_from": "FOR",
	"fly_to": "RIO",
	"date_from": "01/10/2022",
	"date_to": "12/12/2022",
	"query_limit": 5
}
```

#### Run all Queries
This function runs the whole pipeline described above on the current queries (tequilla HTTP request → postgresSQL database operations → telegram notifications) 

#### Refresh DB
This function recreates the columns and erases all data in the database

# HEROKU
After testing the endpoints locally, you should
- Upload the code on Heroku
- Setup the environment variables on Heroku
- Install the Heroku Scheduler addon and run the job below every day
```
$ python apis/api_execution/self_execution.py
```


