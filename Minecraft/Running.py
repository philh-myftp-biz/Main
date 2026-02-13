from __init__ import Worlds, Tasks


for w in Worlds():

    # If the world is running
    if Tasks[w.name()].exists():

        # Output True
        print('true')
        break

# If no worlds are running
else:
    # Output False
    print('false')