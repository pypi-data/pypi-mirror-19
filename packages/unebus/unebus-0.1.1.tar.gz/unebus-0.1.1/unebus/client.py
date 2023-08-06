from core import Route
from factory import route_from_dict,\
                    vehicle_from_dict
import requests


class Client(object):
    
    def __init__(self,
        city=1, 
        base_url='http://bussonora.in/api/v1'):
        super(Client, self).__init__()
        self.city = city
        self.base_url = base_url

    def routes(self):
        lines = []
        url = "{}/rutas/ciudades/{}/?json".format(
            self.base_url,
            self.city,
        )
        response = requests.get(url)
        if response.status_code == 200:
            items = response.json()
            for item in items:
                line = route_from_dict(item)
                lines.append(line)

            return lines

        return None

    def vehicles(self, route_id):
        cars = []
        url = "{}/ubicaciones/{}/?json".format(
            self.base_url,
            route_id,
        )
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            items = data['ubicaciones']
            for item in items:
                car = vehicle_from_dict(item)
                cars.append(car)
            return cars

        else:
            return None

if __name__ == '__main__':
    client = Client()
    routes = client.routes()
    if routes:
        route = routes[0]
        print(route.id)
        vehicles = client.vehicles(route.id)
        print(vehicles)