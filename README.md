# pyirc stats

a thingy for displaying irc stats.
there are two components.

## the python bit

ircstats.py houses the IRCStats class, it outputs (and reads) json in the following format:

    {
      "current_nick": {
        "aliases": ["dave", "nigel", "partario"],
        "lines": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      }
    }

right now theres only an irssi logs parser, but you can write a parser for any type of irc log using the IRCStats object and the following methods:

### IRCStats(path, always_write)

path (string) :the file the stats will write to and initially read from to seed the array.

always_write (bool): whether to write after every change or not. if set to False the file will __only__ be written when you call write().


### IRCStats.new_line(nick, hour)

nick (string): the nick of the user, if the nick is new it will be added.

hour (int): the hour the message was sent, 0-23.


### IRCStats.nick_change(old, new)

old (string): the old nick being changed from.

new (string): the new nick being changed to.

### IRCStats.write()

writes whatever file was previously specified in the constructor

## the web bit

index.html under www reads that stats.json file. it requires date.js, raphael.js (both inlcuded) and jQuery.
