
def parse_subugid_file(file):
    for line in file:
        line = line.strip()
        if not line: continue
        username, base, length = line.split(':')
        yield (username, int(base), int(length))

def get_subugid_ranges_for_user(username):
    us, gs = (set((b,l) for u,b,l in
                  parse_subugid_file(open('/etc/sub{}id'.format(c)))
                  if u==username)
              for c in 'ug')
    return tuple(list(sorted(xs)) for xs in (us, gs))

def invert_ranges(base_length_iter, min_id, max_id):
    i = 0
    for r_b, r_l in sorted((base, length) for base, length in base_length_iter):
        if i < r_b:
            yield (i, r_b-i)
        i = r_b + r_l
    if i < max_id:
        yield (i, max_id-i)

def find_free_contiguous_range(base_length_iter, length, align=1):
    b, l = 0, length
    for r_b, r_l in sorted((base, length) for base, length in base_length_iter):
        if not (b + l <= r_b or b >= r_b + r_l):
            b = r_b + r_l
            b += (-b) % align
    return (b, l)

#print(get_subugid_ranges_for_user('root'))

