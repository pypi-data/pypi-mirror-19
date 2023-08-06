# import json
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.dialects.postgresql import UUID
# import os
# import uuid
# from geoalchemy2.types import Geometry
# 
# from .test_base import Base, BaseTestCase
# 
# from .resource import CollectionResource, SingleResource
# 
# 
# if 'AUTOCRUD_DSN' in os.environ and os.environ['AUTOCRUD_DSN'].startswith('postgresql+pg8000:'):
#     class Place(Base):
#         __tablename__ = 'places'
#         id          = Column(UUID(), primary_key=True)
#         name        = Column(String(50), unique=True)
#         location    = Column(Geometry('POINT'))
# 
#     class PlaceCollectionResource(CollectionResource):
#         model = Place
# 
#     class PlaceResource(SingleResource):
#         model = Place
# 
#     class GeometryTest(BaseTestCase):
#         def create_test_resources(self):
#             self.app.add_route('/places', PlaceCollectionResource(self.db_engine))
#             self.app.add_route('/places/{id}', PlaceResource(self.db_engine))
# 
#         def test_point(self):
#             place = {
#                 'id':       1,
#                 'name':     'Brisbane',
#                 'location': {
#                     'longitude': 152.9614268,
#                     'latitude':  -27.4748781,
#                 },
#             }
#             response, = self.simulate_request('/places', method='POST', body=json.dumps(place), headers={'Accept': 'application/json', 'Content-Type': 'application/json'})
#             self.assertCreated(response, {
#                 'data': place
#             })
