from stream_chat import StreamChat

gstream = StreamChat('','')
offset = 0
limit = 30
sort = None
filter = {'banned': False}

while True:
    users = gstream.query_users(filter, sort, ** {'limit':limit, 'offset':offset})
    offset = offset + 30
    if not len(users['users']):
        break
    for user in users['users']:
        if 'name' in user and not isinstance(user['name'], str):
            print(user)
            gstream.update_user({
                'id': str(user['id']),
                'name': str('{} {}'.format(user['first_name'], user['last_name'])),
            })
