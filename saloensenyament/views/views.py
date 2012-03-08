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
from pyramid.httpexceptions import HTTPFound

logger = logging.getLogger('saloensenyament')

def my_view(request):
    return {'project':'saloensenyament'}

@view_config(context=MyModel, renderer='saloensenyament:templates/saloform.pt', permission='view')
def saloForm(context, request):
    page_title = "Formulari UPC Sal&oacute; Ensenyament 2012"
    api = TemplateAPI(context, request, page_title)
    
    titulacions, graus = getTitulacionsEnsenyament(request.registry.settings['titulacions_file_ensenyament'])

    sorted_titulacions = [dict(name=a[0],data=a[1]) for a in sorted(titulacions.iteritems(), key=itemgetter(0), reverse=False)]    
    
    if request.params.get('form.submitted', None) is not None:
        choices = []
        email = extractMail(request.POST.getall('email'))
        for key in request.POST.keys():
            if key!='email' and key!='form.submitted':
                choices.append(key)
        
        if enviaMail(request, email, choices, graus):
            logger.info(email + ' ' + str(choices))
        else:
            return HTTPFound(request.path_url)

        return dict(api=api, titulacions=sorted_titulacions)
    
    return dict(api=api, titulacions=sorted_titulacions)

@view_config(context=MyModel, name="salofutura", renderer='saloensenyament:templates/salofutura.pt', permission='view')
def saloFuturaForm(context, request):
    page_title = "Formulari UPC Sal&oacute; Futura 2012"
    api = TemplateAPI(context, request, page_title)

    titulacions, graus = getTitulacionsFutura(request.registry.settings['titulacions_file_futura'])
    sorted_titulacions = [dict(name=a[0],data=a[1]) for a in sorted(titulacions.iteritems(), key=itemgetter(0), reverse=False)]    
    
    if request.params.get('formFutura.submitted', None) is not None:
        choices = []
        email = extractMail(request.POST.getall('email'))
        for key in request.POST.keys():
            if key!='email' and key!='formFutura.submitted':
                choices.append(key)
    
        if enviaMailFutura(request, email, choices, graus):
            logger.info(email + ' ' + str(choices))
        else:
            return HTTPFound(request.path_url)

        return dict(api=api, titulacions=sorted_titulacions)
    
    return dict(api=api, titulacions=sorted_titulacions,)    

def extractMail(emailList):
    for email in emailList:
        if email!=u'':
            return email
     
def enviaMail(request, email, choices, graus):
    if not email :
        return False
    else:

        mailer = request.registry['mailer']
        
        subject = u"UPC. Saló de l’Ensenyament. Informació titulacions 2012/13"
        
        body1 = """Benvolgut/Benvolguda,<br/><br/>
    A continuació, adjuntem els documents relacionats amb les titulacions de la UPC sobre les quals has demanat informació al Saló de l'Ensenyament. Esperem que et siguin d’utilitat per ajudar-te a triar els teus estudis universitaris.<br/><br/>
    """.decode('utf-8')
        
        body2 = """<br/>Estem a la teva disposició per aclarir-te qualsevol dubte. Ho pots fer:<br/>
    * Visitant http://www.upc.edu/aprendre/estudis<br/>
    * Enviant un correu a info@upc.edu<br/>
    * Telefonant al 93 401 62 00<br/><br/>

    Salutacions cordials.<br/><br/>

    """.decode('utf-8')

        peu = """Barcelona, """.decode('utf-8') + unicode(datetime.datetime.now().day) + """ de març de 2012<br/>
    © UPC. Universitat Politècnica de Catalunya.  BarcelonaTech<br/><br/>

    En compliment del que estableixen les normatives de protecció de dades, t’informem que les dades que ens has donat en aquest formulari les inclourem al fitxer d’estudiants de la UPC, per tal de poder-te enviar la informació que ens has demanat. Usarem l’adreça de correu electrònic que ens has donat per enviar-te informació de la UPC, però si no vols rebre cap més informació, ens pots enviar un correu electrònic a saloensenyament@upc.edu, o ens ho pots dir quan responguis els correus electrònics que t’enviem.  Finalment, també t’informem que, si vols accedir a les dades teves, canviar- les, oposar-te a que les tinguem o que  deixem de tractar-les, et pots adreçar al Servei de Comunicació i Promoció, amb  domicili a la Plaça d’Eusebi Güell, 7 de  Barcelona, o a l’adreça electrònica: saloensenyament@upc.edu
        """.decode('utf-8')

        anexos = ''
        for choice in choices:
            for i in graus[choice]:
                link = '<a href="' + i['pdf'] + '">'+ i['place'] + ' ' + i['siglas'] + '</a>'
                anexos = anexos + '<b>' + choice.replace("  ","'") + '</b>' + ' impartit a '+ link + '<br/>'

        body = body1 + anexos + '\n' + body2 + peu 
        
        message = Message(subject=subject,
                          sender="saloensenyament@upc.edu", 
                          html=body,
                          recipients=email.split(','),
                          )
        # Versió 2011 adjuntava annexes en PDF
        #for choice in choices:
        #    attachment = Attachment(choice+".pdf", "application/pdf",
        #                             open(pdf_dir+ choice +".pdf", "rb"))
        #    print "Attachant "+ choice
        #    message.attach(attachment)

        mailer.send(message)
        return True


def enviaMailFutura(request, email, choices, graus):
    if not email :
        return False
    else:

        mailer = request.registry['mailer']
        # Versió 2011 adjuntava annexes en PDF        
        #pdf_dir = request.registry.settings['pdf_dir']
        
        subject = u"UPC. Saló de l'Ensenyament. Informació titulacions 2012/13"
        
        body1 = """Benvolgut/Benvolguda,<br/><br/>
        
    A continuació, adjuntem els documents relacionats amb les titulacions de la UPC sobre les quals has demanat informació al Saló de l'Ensenyament. Esperem que et siguin d’utilitat per ajudar-te a triar els teus estudis universitaris.<br/><br/>
    """.decode('utf-8')

        anexos = ''
        for choice in choices:
            for i in graus[choice]:
                link = '<a href="' + i['pdf'] + '">' + choice.replace("  ","'") + '</a>'
                anexos = anexos + link + '<br/>'            

        body2 = """<br/><br/>Estem a la teva disposició per aclarir-te qualsevol dubte. Ho pots fer:<br/>
    * Visitant http://www.upc.edu/aprendre/estudis<br/>
    * Enviant un correu a info@upc.edu<br/>
    * Telefonant al 93 401 62 00<br/><br/>

    Salutacions cordials.<br/><br/>

    """.decode('utf-8')

        peu = """Barcelona, """.decode('utf-8') + unicode(datetime.datetime.now().day) + """ de març de 2012<br/>
    © UPC. Universitat Politècnica de Catalunya.  BarcelonaTech<br/><br/>

    En compliment del que estableixen les normatives de protecció de dades, t’informem que les dades que ens has donat en aquest formulari les inclourem al fitxer d’estudiants de la UPC, per tal de poder-te enviar la informació que ens has demanat. Usarem l’adreça de correu electrònic que ens has donat per enviar-te informació de la UPC, però si no vols rebre cap més informació, ens pots enviar un correu electrònic a saloensenyament@upc.edu, o ens ho pots dir quan responguis els correus electrònics que t’enviem.  Finalment, també t’informem que, si vols accedir a les dades teves, canviar- les, oposar-te a que les tinguem o que  deixem de tractar-les, et pots adreçar al Servei de Comunicació i Promoció, amb  domicili a la Plaça d’Eusebi Güell, 7 de  Barcelona, o a l’adreça electrònica: saloensenyament@upc.edu
        """.decode('utf-8')

        body = body1 + anexos + '\n' + body2 + peu 
        
        message = Message(subject=subject,
                          sender="saloensenyament@upc.edu",
                          recipients=email.split(','),
                          html=body,)

        # Versió 2011 adjuntava annexes en PDF
        #for choice in choices:
        #    attachment = Attachment(choice+".pdf", "application/pdf",
        #                             open(pdf_dir+ choice +".pdf", "rb"))
        #    print "Attachant "+ choice
        #    message.attach(attachment)


        mailer.send(message)
        return True

def getTitulacionsEnsenyament(titulacions_file):
    
    # Estructura {'nomAmbit':{'nomCicle':{'nomTitulacio':[{'escuela':'C', 'url':'U'}],},},}
    #"Arquitectura, Urbanisme i Edificació"; "Grau" ; "Grau en Arquitectura"; "Sant Cugat del Vallès" ;"ETSAV";"http://www.upc.edu/estudispdf/pdfEstudi.php?id_estudi=229&lang=cat"
    titulacions = {}
    graus = {}
    res = csv.reader(open(titulacions_file, 'rb'), delimiter=';', quotechar='"')
    for row in res:
        ambit  = row[0].decode('utf-8')
        if ambit not in titulacions.keys():
            titulacions[ambit]={}
        cicle  = row[1].decode('utf-8').encode('utf-8')
        nom    = row[2].decode('utf-8')
        place  = row[3].decode('utf-8')
        siglas = row[4].decode('utf-8')
        pdf    = row[5].decode('utf-8')

        if cicle not in titulacions[ambit].keys():
            titulacions[ambit][cicle]={}
        titulacions[ambit][cicle].setdefault(nom, [])

        graus.setdefault(nom, [])
        graus[nom].append({'pdf':pdf, 'place':place, 'siglas':siglas,})
        
    return titulacions, graus


def getTitulacionsFutura(titulacions_file):
    
    # Estructura {'Ambit':[{'cicle':'A', 'pdf':'C'},},]
    # "Arquitectura, Urbanisme i Edificació";"Màster universitari en Arquitectura, Energia i Medi Ambient";"http://mastersuniversitaris.upc.edu/aem/"
    titulacions = {}
    graus = {}
    res = csv.reader(open(titulacions_file, 'rb'), delimiter=';', quotechar='"')
    for row in res:
        ambit  = row[0].decode('utf-8')
        if ambit not in titulacions.keys():
            titulacions[ambit]={}
        cicle  = row[1].decode('utf-8')
        pdf    = row[2].decode('utf-8')
        if cicle not in titulacions[ambit].keys():
            titulacions[ambit][cicle]={}
        
        titulacions[ambit][cicle].setdefault(cicle, [])

        graus.setdefault(cicle, [])
        graus[cicle].append({'pdf':pdf,})

    return titulacions, graus