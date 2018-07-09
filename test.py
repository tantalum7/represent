
from twfy_python import TheyWorkForYou

API_KEY = open("twfy_key").read().strip()

twfy = TheyWorkForYou(API_KEY)

#get one user from id
t_may = twfy.api.getPerson(id="10426")
for p in t_may:
    print (p["full_name"] + p["left_house"])

