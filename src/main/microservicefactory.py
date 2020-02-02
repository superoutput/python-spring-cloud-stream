from microserviceenum import MicroserviceEnum
from microservices.api.api import API
from microservices.aas.aas import AAS
from gqs import GQS
from valet import Valet
#from microservices_base.terminology import Terminology

class MicroserviceFactory:
    def __init__(self):
        pass

    def create(self, microservice):
        if not isinstance(microservice, MicroserviceEnum):
            raise TypeError

        if microservice is MicroserviceEnum.API :
            return API()
        elif microservice is MicroserviceEnum.AAS :
            return AAS()
        elif microservice is MicroserviceEnum.GQS :
            return GQS()
        elif microservice is MicroserviceEnum.VALET :
            return Valet()
        else :
            print("Not Implemented yet")
            return None