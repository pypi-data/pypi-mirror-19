from HackFoursquare import Hacking
import json
hack = Hacking("josiel.wirlino@gmail.com","j0sielengenheiro")
hack.open_browser()

venue = hack.get_venue_detail("5611c005498eacfce78eceee")
venue2 = json.loads(venue)
