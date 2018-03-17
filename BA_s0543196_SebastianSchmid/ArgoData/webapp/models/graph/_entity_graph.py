from BA_argo_proto.webapp.models import  ArgoFloat, Record, Profile, Measurement, Location

class EntityGraph(object):
    
    def __init__(self, argo_float_identifier):
        
        self.__argo_float = ArgoFloat(identifier=argo_float_identifier)
        self.graph = self._generate_entity_graph()

    def _generate_entity_graph(self):

        graph = {self.__argo_float : []}

        for ds in self.__argo_float.data:
            location_model = Location(latitude=ds.position['latitude'], longitude=ds.position['longitude'])
            measurement_model = Measurement(argo_float=self.__argo_float, location=location_model)
            profile_model = Profile(cycle=int(ds.cycle_number), timestamp=ds.date_creation,measurement=measurement_model)
            pressure_record_model = Record(data_type='pressure', value=ds.pressure, profile=profile_model)
            temperature_record_model = Record(data_type='temperature', value=ds.temperature, profile=profile_model)
            salinity_record_model = Record(data_type='salinity', value=ds.salinity, profile=profile_model)
            conductivity_record_model = Record(data_type='conductivity', value=ds.conductivity,profile=profile_model)

            graph[self.__argo_float].append({
                {
                    'location': location_model,
                    'measurement': measurement_model,
                    'profile': profile_model,
                    'pressure': pressure_record_model,
                    'temperature': temperature_record_model,
                    'salinity': salinity_record_model,
                    'conductivity': conductivity_record_model
                }
            })
        return graph

    def __str__(self):
        return str(self.graph)
        