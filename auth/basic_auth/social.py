def create_user(strategy, details, user=None, *args, **kwargs):

    print(details)
    print("\n")
    print("\n")
    print(kwargs)
    print("\n")
    print("\n")
    print(user)
    print("\n")
    print("\n")
    
    if user:
        return {'is_new': False}
 
    fields = {'email': details.get('email'), 'nickname': details.get('username')}
 
    if not fields:
        return
 
    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }