# -*- coding: utf-8 -*-
import os
import csv
from pyramid.view import view_config
from saloensenyament.models import MyModel

from saloensenyament.views.api import TemplateAPI

from pyramid_mailer.message import Message, Attachment
import datetime
import logging
from operator import itemgetter

logger = logging.getLogger('saloensenyament')

#@view_config(context=MyModel, renderer='saloensenyament:templates/mytemplate.pt')
def my_view(request):
    return {'project':'saloensenyament'}

@view_config(context=MyModel, renderer='saloensenyament:templates/saloform.pt', permission='view')
def saloForm(context, request):
    page_title = "Formulari UPC Sal&oacute; Ensenyament 2011"
    api = TemplateAPI(context, request, page_title)
    titulacions = getTitulacions(request.registry.settings['titulacions_file'])
    sorted_titulacions = [dict(name=a[0],data=a[1]) for a in sorted(titulacions.iteritems(), key=itemgetter(0), reverse=False)]    
    if request.params.get('form.submitted', None) is not None:
        choices = []
        email = extractMail(request.POST.getall('email'))
        for key in request.POST.keys():
            if key!='email' and key!='form.submitted':
                choices.append(key)
        
        enviaMail(request, email, choices)
        logger.info(email + ' ' + str(choices))

        return dict(api=api, titulacions=sorted_titulacions)
    
    return dict(api=api, titulacions=sorted_titulacions)

def extractMail(emailList):
    for email in emailList:
        if email!=u'':
            return email
     
def enviaMail(request, email, choices):
    mailer = request.registry['mailer']
    pdf_dir = request.registry.settings['pdf_dir']
    
    subject = u"UPC. Saló de l’Ensenyament. Informació titulacions 2011/12"
    
    body = """Benvolgut/Benvolguda,
    
A continuació, adjuntem els documents informatius relacionats amb les titulacions de la UPC sobre les quals has demanat informació al Saló de l'Ensenyament. Esperem que et siguin d’utilitat per ajudar-te a triar els teus estudis universitaris. 

Estem a la teva disposició per aclarir-te qualsevol dubte. Ho pots fer:
* Visitant http://www.upc.edu/aprendre/estudis
* Enviant un correu a info@upc.edu
* Telefonant al 93 401 62 00

Salutacions cordials.

""".decode('utf-8')
    
    peu = """Barcelona, """.decode('utf-8') + unicode(datetime.datetime.now().day) + """ de març de 2011
© UPC. Universitat Politècnica de Catalunya.  BarcelonaTech

En compliment del que estableixen les normatives de protecció de dades, t’informem que les dades que ens has donat en aquest formulari les inclourem al fitxer d’estudiants de la UPC, per tal de poder-te enviar la informació que ens has demanat. Usarem l’adreça de correu electrònic que ens has donat per enviar-te informació de la UPC, però si no vols rebre cap més informació, ens pots enviar un correu electrònic a saloensenyament@upc.edu, o ens ho pots dir quan responguis els correus electrònics que t’enviem.  Finalment, també t’informem que, si vols accedir a les dades teves, canviar- les, oposar-te a que les tinguem o que  deixem de tractar-les, et pots adreçar al Servei de Comunicació i Promoció, amb  domicili a la Plaça d’Eusebi Güell, 7 de  Barcelona, o a l’adreça electrònica: saloensenyament@upc.edu
           """.decode('utf-8')

    body = body + peu
    
    message = Message(subject=subject,
                  sender="saloensenyament@upc.edu",
                  recipients=email.split(','),
                  body=body)

    for choice in choices:
        attachment = Attachment(choice+".pdf", "application/pdf",
                                 open(pdf_dir+ choice +".pdf", "rb"))
        print "Attachant "+ choice
        message.attach(attachment)


    mailer.send(message)


def getTitulacions(titulacions_file):
    
    # Estructura {'Ambit':[{'cicle':'A', 'nom':'B', 'pdf':'C'},},]
    titulacions = {}
    res = csv.reader(open(titulacions_file, 'rb'), delimiter=';', quotechar='"')
    for row in res:
        ambit=row[0].decode('utf-8')
        if ambit not in titulacions.keys():
            titulacions[ambit]={}
        cicle=row[1].decode('utf-8')
        nom=row[2].decode('utf-8')
        pdf=row[3].decode('utf-8')
        if cicle not in titulacions[ambit].keys():
            titulacions[ambit][cicle]=[]
        titulacions[ambit][cicle].append({'nom':nom, 'pdf':pdf})
    return titulacions
