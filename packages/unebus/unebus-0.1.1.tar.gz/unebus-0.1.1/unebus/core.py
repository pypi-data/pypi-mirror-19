from time import strptime


class Route(object):
    __slots__ = ['id', 'duration',
                 'route_length', 
                 'schedule',
                 'units', 'name'
                 ]

    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def __repr__(self):
        return 'Client({}={})'.format(
            'name', repr(getattr(self, 'name', None))
        )


class Vehicle(object):
    __slots__ = ['id', 'imei',
                 'location']

    def __repr__(self):
        return 'Vehicle({}={})'.format(
            'location', repr(getattr(self, 'location', None))
        )
