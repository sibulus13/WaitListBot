from Utils import create_same_weekday_arr, datetime


DISCORD_TOKEN = 'MTAyOTEzNzA5NTQzODExODk4Mg.GSI_It.lcoIScgmAp7h86vETlTQGJS5LuK8g32vnnNBUc'

FIREBASE_SDK_KEY = r"Z:\repo\Discord\WaitListBot\ssbc-waitlist-firebase-adminsdk-fx8xj-3b655fbfd4.json"

FIREBASE_DB_URL = "https://ssbc-waitlist-default-rtdb.firebaseio.com/"

PRIORITY_MAP = {
    "SFU": 0,
    "Non-SFUs & Alumnis": 2,
}

WAITLIST_PRIORITY = 1
MAX_SIGN_UP_COUNT = 3

monday_clear_priority_time = datetime.datetime(
    2022,
    10,
    11,
)
tuesday_reset_list_time = datetime.datetime(
    2022,
    10,
    11,
)


WEEKLY_MON_NIGHT_PRIORITY_CLEAR_SCHEDULE = create_same_weekday_arr(
    monday_clear_priority_time)
WEEKLY_TUES_NIGHT_LIST_CLEAR_SCHEDULE = create_same_weekday_arr(
    tuesday_reset_list_time)