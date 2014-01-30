# -*- coding: utf-8 -*-

'''
Created on 22/01/2014

@author: Capi
'''
import endpoints
from models import Doctor
from protorpc import message_types, messages, remote
from protorpc.message_types import VoidMessage


package = "Hello"



class DoctorMessage(messages.Message):
    full_name = messages.StringField(1)
    specialities = messages.StringField(2)
    email = messages.StringField(3)
    sent = messages.BooleanField(4)
    want_test = messages.BooleanField(5)
    poll_open = messages.BooleanField(6)

class DoctorsCollection(messages.Message):
    doctors = messages.MessageField(DoctorMessage, 1, repeated=True)


@endpoints.api(name="doctors", version='v1')
class DoctorsApi(remote.Service):

    @endpoints.method(message_types.VoidMessage, DoctorsCollection,
                      path='doctors', http_method='GET',
                      name="all")
    def doctors_list(self, request):
        doctors = Doctor.all()

        doctors_message = []

        for d in doctors:
            doctors_message.append(DoctorMessage(full_name=d.full_name,
                                                 sent = d.sent,
                                                 email = d.email,
                                                 specialities = d.specialities,
                                                 want_test = d.want_test,
                                                 poll_open = d.poll_open
                                                 ))


        return DoctorsCollection(doctors=doctors_message)


    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))


    FIELDS_RESOURCE = endpoints.ResourceContainer(DoctorMessage)


    @endpoints.method(FIELDS_RESOURCE, DoctorMessage,
                      path='doctorsave', http_method='POST',
                      name="save"
                      )
    def doctors_save(self, request):
        d = Doctor(full_name=request.full_name, specialities=request.specialities, email=request.email)
        d.put()

        return DoctorMessage(full_name=d.full_name, specialities=d.specialities, email=d.email)


    # Especificar método
    def send_email(self, request):
        pass


APPLICATION = endpoints.api_server([DoctorsApi])




