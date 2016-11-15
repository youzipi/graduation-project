def _project(n, i):
    n['value'] = n['_id']
    del n['_id']
    n['id'] = i + 1
    return n


area_rank = [
    {
        '_id': 'cs',
        'count': '123'
    },
    {
        '_id': 'ee',
        'count': '27'
    },
]

length = len(area_rank)
result = map(_project, area_rank, range(length))
print result
