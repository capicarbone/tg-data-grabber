# -*- coding: utf-8 -*-

'''
Created on 22/01/2014

@author: Capi
'''
import endpoints
from models import Doctor
from protorpc import message_types, messages, remote
from protorpc.message_types import VoidMessage

from google.appengine.api import mail

package = "Hello"

email_body = u"""

    Buenas Dr(a). %s,

    Mi nombre es Carlos Pinelly. Soy estudiante de la Universidad Nacional Experimental de Guayana (UNEG). Actualmente me encuentro realizando mi trabajo de grado para optar a mi título de Ingeniero en Informática. Mi investigación está orientada al desarrollo de una aplicación móvil dirigida a la área médica y quizás usted podría ayudarme. En el siguiente enlace encontrará una encuesta electrónica que me permitirá recolectar cierta información necesaria para mi investigación la cual espero pueda tomarse unos minutos para responder.

    https://docs.google.com/forms/d/1LrQhbwlv-6Xj4GFPG_5G3iecAveEV8fH9g92l4V4DgQ/viewform

    Si desea conocer más sobre mi investigación puede consultar el siguiente enlace:

    http://tusaludapp.appspot.com/

    Sin mas que decir, me despido agradeciendo su apoyo en mi investigación.

    Saludos.
"""

class DoctorMessage(messages.Message):
    full_name = messages.StringField(1)
    specialities = messages.StringField(2)
    email = messages.StringField(3)
    sent = messages.BooleanField(4)
    poll_open = messages.BooleanField(5)
    invited_by = messages.StringField(6)

class DoctorsCollection(messages.Message):
    doctors = messages.MessageField(DoctorMessage, 1, repeated=True)


@endpoints.api(name="doctors", version='v1',
               description='Api para la gestión de doctores y sus encuestas.')
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
                                                 poll_open = d.poll_open,
                                                 invited_by = d.invited_by
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
        d = Doctor(full_name=request.full_name, specialities=request.specialities, email=request.email, invited_by=request.invited_by)
        d.user = d.email.split('@')[0]

        capitalized_name =  ''

        for name in d.full_name.split(' '):
            capitalized_name = capitalized_name + name.capitalize() + ' '

        d.full_name = capitalized_name

        d.put()

        return DoctorMessage(full_name=d.full_name, specialities=d.specialities, email=d.email)


    EMAIL_RESOURCE = endpoints.ResourceContainer(message_types.VoidMessage,
                                                email=messages.StringField(1))

    @endpoints.method(EMAIL_RESOURCE, message_types.VoidMessage,
                      path="doctorsend",
                      name="send_email")
    def send_email(self, request):

        to_email = request.email

        doctor = Doctor.all().filter("email =",to_email)[0]

        if (mail.is_email_valid(to_email) and doctor):

            from_email = "Carlos Pinelly <cpinelly@gmail.com>"
            subject = u"Apoyo para trabajo de investigación"
            body = email_body % (doctor.full_name)

            mail.send_mail(from_email, to_email, subject, body)

            doctor.sent = True
            doctor.put()

        return message_types.VoidMessage()

    @endpoints.method(EMAIL_RESOURCE, message_types.VoidMessage,
                      path="poll_opened", name="poll_opened")
    def poll_opened(self, request):

        doctor = Doctor.all().filter("user =", request.email)[0]
        doctor.poll_open = True
        doctor.put()

        return message_types.VoidMessage()

APPLICATION = endpoints.api_server([DoctorsApi])




