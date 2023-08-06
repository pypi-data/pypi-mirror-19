from core import Route, Vehicle
from time import strptime


def route_from_dict(d):
    r = Route()
    r.id = d.get('id_ruta', None)
    r.name = d.get('nombre', None)
    r.duration = d.get('duracion', 0)
    r.route_length = d.get('longitud', 0.0)

    fromtime = d.get('inicio_servicio', '00:00:00')
    totime   = d.get('fin_servicio', '00:00:00')

    r.schedule = (
        strptime(fromtime, '%H:%M:%S'),
        strptime(totime, '%H:%M:%S'),
    )

    r.units = d.get('unidades_servicio', 0)

    return r

def vehicle_from_dict(d):
    r = Vehicle()
    r.id = d.get('vehiculo_id', None)
    r.imei = d.get('vehiculo_imei', None)

    lat = d.get('latitud', None)
    lng = d.get('longitud', None)

    if not isinstance(lat, float):
        raise ValueError('invalid lat')

    if not isinstance(lng, float):
        raise ValueError('invalid lng')

    r.location = (lat, lng,)

    return r