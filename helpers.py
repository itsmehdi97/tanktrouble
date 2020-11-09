def read_pos(s):
    s = s.split(",")
    return int(s[0]), int(s[1])

def write_pos(tup):
    return f"{tup[0]},{tup[1]}"