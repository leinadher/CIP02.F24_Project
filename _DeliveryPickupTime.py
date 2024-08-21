import re
import pandas as pd

# Simplification of string information to integers
def convert_delivery_time(delivery_time):
    if pd.isna(delivery_time):
        return None
    elif delivery_time == "morgen geliefert":
        return 1
    elif delivery_time == f"in 3 Tagen geliefert":
        return 3
    elif delivery_time == f"innerhalb 4 Tagen geliefert":
        return 4
    elif re.search(r"(Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag)", str(delivery_time)):
        return 7
    elif delivery_time == "innerhalb 1 - 2 Wochen geliefert" or delivery_time == "innerhalb 2 Wochen geliefert":
        return 14
    elif delivery_time == "innerhalb 2 - 3 Wochen geliefert" or delivery_time == "in 2 - 3 Wochen geliefert":
        return 21
    elif delivery_time == "in 3 - 4 Wochen geliefert":
        return 30
    elif delivery_time == "in 4 - 5 Wochen geliefert":
        return 35
    elif delivery_time == "in 7 Wochen geliefert":
        return 49
    elif delivery_time == "Liefertermin unbekannt":
        return None
    else:
        return None

def convert_pickup_time(pickup_time):
    if pd.isna(pickup_time):
        return None
    elif pickup_time == "morgen abholbereit":
        return 1
    elif re.search(r"(Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag)", str(pickup_time)):
        return 7
    elif pickup_time == "innerhalb 1 - 2 Wochen abholbereit" or pickup_time == "innerhalb 2 Wochen abholbereit":
        return 14
    elif pickup_time == "in 3 - 4 Wochen abholbereit":
        return 30
    elif pickup_time == "in 4 - 5 Wochen abholbereit":
        return 35
    elif pickup_time == "in 7 Wochen abholbereit":
        return 49
    elif pickup_time == "Lieftermin unbekannt":
        return None
    else:
        return None
