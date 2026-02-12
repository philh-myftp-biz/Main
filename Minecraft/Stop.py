from __init__ import Worlds, Tasks

for w in Worlds():

    Tasks[w.name()].stop()
