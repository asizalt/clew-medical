import json
import functools
import datetime
from aiohttp import web
def defaultconverter(o):
  if isinstance(o, datetime.datetime):
      return o.__str__()

pretty_json = functools.partial(json.dumps, indent=4,default=defaultconverter)

