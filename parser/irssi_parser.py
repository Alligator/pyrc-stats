import re
import sys

from ircstats import IRCStats

def parse(fi):
  print "reading file"
  lines = open(fi, 'r').readlines()
  reg = re.compile("""
    (?P<bla>---)?
    (?P<hour>\d\d):    # hour
    (?P<min>\d\d)\s     # minute
    (?P<prefix>[^\w]+)  # prefix. -!-,  <@ etc
    (?P<nick>[\w]+)     # nick
    (?P<rest>.*)
    """, re.VERBOSE)
  creg = re.compile('is now known as ([\w]+)')
  
  stats = IRCStats('stats.json', False)
  print len(lines)
  for i, line in enumerate(lines):
    sys.stdout.write('\r' + str((float(i) / len(lines)) * 100)[:4] + '% ' + str(i))
    try:
      match = reg.match(line).groupdict()
      if match:
        if match['prefix'] == '-!- ' and 'is now known as' in match['rest']:
          to = creg.search(match['rest']).groups(0)[0]
          stats.nick_change(match['nick'], to)
        elif not match['prefix'] == '-!- ':
          stats.new_line(match['nick'], int(match['hour']))
    except AttributeError, e:
      pass
  stats.write()

if __name__ == '__main__':
  parse(sys.argv[1]);
