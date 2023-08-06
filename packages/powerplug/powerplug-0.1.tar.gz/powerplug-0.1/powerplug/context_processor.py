from pkg_resources import working_set


def subnav(request):
    '''
    Loop through the entry points and build a sub navigation dictionary
    '''
    navigation = {}
    for entry in working_set.iter_entry_points('powerplug.subnav'):
        navigation.update(entry.load()(entry.name, request))
    return {'subnav': navigation}
