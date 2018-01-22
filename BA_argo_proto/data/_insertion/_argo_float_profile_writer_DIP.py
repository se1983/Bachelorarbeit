from webapp import models


class ArgoFloatProfile:
    def __init__(self, argo_float, db):
        self.argo_float = argo_float

        self.db = db

    def write_data(self, entity_graph):
        """
        :param entity_graph:
        {models.ArgoFloat:
            [{
                'location': models.Location,
                'measurement': models.Measurement,
                'profile': models.Profile,
                'pressure': models.Record,
                'temperature': models.Record,
                'salinity': models.Record,
                'conductivity': models.Record
            }]
        }
        """

        for profiles, argo_float in entity_graph.items():
            self.db.session.add(argo_float)

            for dataset in profiles:
                self.db.session.add(dataset)
        self.db.session.commit()


