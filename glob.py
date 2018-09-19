# All globals stored in here
msgDuration = 5000
fieldRowHeight = 25

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False