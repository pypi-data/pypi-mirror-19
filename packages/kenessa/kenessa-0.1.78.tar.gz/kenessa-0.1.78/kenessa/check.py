def checker(identifier):
    if identifier == 'all':
        params = 'all'
        return identifier, params
    elif identifier[0] == '0':
        params = 'code'
        return identifier, params
    else:
        try:
            identifier = int(identifier)
            params = 'id'
            return identifier, params
        except ValueError:
            params = 'name'
            return [identifier, params]



