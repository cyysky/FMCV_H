import time
from datetime import datetime, timezone
#https://stackoverflow.com/questions/4563272/how-to-convert-a-utc-datetime-to-a-local-datetime-using-only-standard-library
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    #filename = self.utc_to_local(datetime.utcnow()).strftime('%Y-%m-%d_%H%M%S_%f')[:-3]

def without_keys(d, keys):    
    '''
    Usage
    without_keys({"1":1,"2":2},{"1"})
    '''
    return {x: d[x] for x in d if x not in keys}
              