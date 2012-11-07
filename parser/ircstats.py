import json
from pprint import pprint

class IRCStats(object):
  def __init__(self, path, always_write):
    self.path = path
    self.reverse = {}
    self.always_write = always_write
    try:
      self.users = json.loads(open(self.path, 'r').read())
    except Exception, e:
      self.users = {}

  # JSON makes defaultdict weird, roll yer own
  def add(self, nick):
    return self.users.setdefault(nick, {
      'aliases': [],
      'lines': [0]*24
    })

  def new_line(self, nick, hour):
    self.add(nick)
    self.users[nick]['lines'][hour] += 1
    if self.always_write:
      self.write()

  def nick_change(self, old, new):
    # if the new nick is already there just use it
    if new in self.users:
      return

    # switch to new key
    try:
      self.users[new] = self.users[old]
      del self.users[old]
    except KeyError, e:
      # something is real weird, just add a new user
      self.add(new)
      return

    # add old key to aliases
    if old not in self.users[new]['aliases']:
      self.users[new]['aliases'].append(old)
      self.reverse[old] = new
      try:
        del self.reverse[new]
      except KeyError, e:
        pass

    # remove new nick from anyone else who might have it
    if new in self.reverse:
      print
      print self.reverse[new]
      pprint(self.reverse)
      print old, new
      self.users[self.reverse[new]]['aliases'].remove(new)
      del self.reverse[new]
    else:
      for user, data in self.users.iteritems():
        if new in data['aliases']:
          data['aliases'].remove(new)

    if self.always_write:
      self.write()

  def write(self):
    open(self.path, 'w').write(json.dumps(self.users))

  def __str__(self):
    return str(dict(self.users))
