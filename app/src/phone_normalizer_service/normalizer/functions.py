import phonenumbers
import re

from phonenumbers import geocoder, carrier, NumberParseException
from phonenumbers.phonenumber import PhoneNumber
from phonenumbers.phonenumberutil import PhoneNumberType

from .models import *


def cleaner(tmpphone, country):

    tmpphone = tmpphone.strip()

    started_with_plus = False

    if tmpphone.startswith('+'):
        tmpphone = tmpphone.replace('+', '', 1)
        started_with_plus = True

    if tmpphone.startswith('00'):
        tmpphone = tmpphone[2:]

    #Checkout CO bug controller
    if len(tmpphone) == 13 and tmpphone.startswith('5713'):
        tmpphone = tmpphone.replace('5713', '573', 1)
    if len(tmpphone) == 11 and tmpphone.startswith('13') and country == 'CO':
        tmpphone = tmpphone.replace('13', '3', 1)

    if started_with_plus:
        tmpphone = '+' + tmpphone

    return tmpphone


def format_ar_number(tmpphone, useDDI=False):

    normphone = {}
    normphone['type'] = PhoneNumberType.UNKNOWN

    leSaqueElCero = False
    teniaQuince = False
    empezabaCon00 = False
    leSaqueElNueve = False

    if tmpphone.startswith('00'):
        empezabaCon00 = True
        if useDDI:
            normphone['type'] = PhoneNumberType.FIXED_LINE_OR_MOBILE
            normphone['country'] = '00'
            normphone['urban'] = ''
            normphone['line'] = ''
            normphone['interurban'] = ''
            normphone['location'] = ''
            normphone['province'] = ''
            normphone['discable'] = tmpphone
            normphone['carrier'] = ''
        else:
            while tmpphone.startswith('00'):
                tmpphone = tmpphone[1:]

    if not empezabaCon00 or (empezabaCon00 and not tmpphone.startswith('00')):

        if tmpphone.startswith('0810') or tmpphone.startswith('0800'):
            normphone['type'] = PhoneNumberType.TOLL_FREE
            normphone['country'] = '54'
            normphone['urban'] = ''
            normphone['line'] = ''
            normphone['interurban'] = ''
            normphone['location'] = ''
            normphone['province'] = ''
            normphone['discable'] = tmpphone
            normphone['carrier'] = ''

        else:
            if tmpphone.startswith('+'):
                tmpphone = tmpphone[1:]
            if tmpphone.startswith('54'):
                tmpphone = tmpphone[2:]
                if tmpphone.startswith('9'):
                    tmpphone = tmpphone[1:]
                    leSaqueElNueve = True
            if tmpphone.startswith('0'):
                tmpphone = tmpphone[1:]
                leSaqueElCero = True
            if tmpphone.startswith('15'):
                tmpphone = tmpphone[2:]
                teniaQuince = True


            #if (provTel.ToUpper().Equals('AMBA') | | provTel.ToUpper().Equals('CABA') | | provTel.ToUpper().Equals(
            #        'GRAN BUENOS AIRES') | | provTel.ToUpper().Equals('CIUDAD AUT. DE BUENOS AIRES'))
            #    areaTel = 'AMBA';

            cod_ares = None
            area = None
            prov = None
            linea = ''
            #List < cncCod > lcncncods;
            #List < CncNumGeo > listaCods = new List < CncNumGeo > ();

            if len(tmpphone) >= 6:
                if len(tmpphone) < 10:
                    listaCods = None
                    if not leSaqueElCero and len(tmpphone) == 8:
                        subCod = tmpphone[:4]
                        listaCods = NumGeoAr.objects.filter(indicativo='11', bloque=subCod)
                        if listaCods.count() > 0:
                            cod_ares = '11'
                            area = 'AMBA'
                            prov = 'AMBA'

                    if listaCods and listaCods.count() == 0:
                        #Sacarlo de una tabla de provincia por indicativo
                        lcncncods = NumGeoAr.objects.values_list('indicativo').distinct().order_by('indicativo')
                        for p in lcncncods:

                            if tmpphone.startswith(p[0]):
                                cod_ares = p[0]
                                #area = cnccod.Localidad
                                #prov = cnccod.Provincia
                                tmpphone = tmpphone[len(cod_ares):]
                                break

                        if not cod_ares and lcncncods.count() > 0:
                            cod_ares = lcncncods[0].indicativo
                            area = lcncncods[0].localidad
                            #prov = lcncncods[0].Provincia

                        listaCods = NumGeoAr.objects.filter(indicativo=cod_ares)
                else:
                    if tmpphone.startswith('+54'):
                        tmpphone = tmpphone[3:]
                    if tmpphone.startswith('54'):
                        tmpphone = tmpphone[2:]
                    if tmpphone.startswith('0'):
                        tmpphone = tmpphone[1:]
                    if tmpphone.startswith('15'):
                        tmpphone = tmpphone[2:]

                    i = 2
                    j = 1
                    tmpphone_len = len(tmpphone)-j

                    ind = tmpphone[0: i]
                    blok = tmpphone[i:]

                    listaCods = NumGeoAr.objects.filter(indicativo=ind, bloque=blok)

                    while listaCods.count() != 1 and i <= 4:
                        tmpphone_len = len(tmpphone) - j
                        while listaCods.count() != 1 and tmpphone_len > (4 if blok.startswith('15') else 2) and tmpphone_len > i:
                            j+=1
                            tmpphone_len = len(tmpphone) - j
                            ind = tmpphone[0:i]
                            blok = tmpphone[i:j + i]
                            if blok.startswith('15'):
                                blok = blok[2:]
                            listaCods = NumGeoAr.objects.filter(indicativo=ind, bloque=blok)

                        j = 1
                        i += 1

                    if listaCods.count() == 1:
                        cod_ares = listaCods[0].indicativo
                        area = listaCods[0].localidad
                        #prov = this.GetProvFromCodArea(cod_ares);
                        tmpphone = tmpphone[len(cod_ares):]

            if cod_ares:
                if tmpphone.startswith('15'):
                    tmpphone = tmpphone[2:]

                for cod in listaCods:
                    if tmpphone.startswith(cod.bloque):
                        linea = tmpphone[len(cod.bloque):]
                        if cod.servicio.strip() in ('SMT/PCS', 'PCS', 'SRMC', 'SRMC/PCS', 'SRCE') or 'STM' in cod.servicio.strip():
                            tmpphone = '15' + tmpphone
                            normphone['type'] = PhoneNumberType.MOBILE
                        else:
                            normphone['type'] = PhoneNumberType.FIXED_LINE
                        tmpphone = cod_ares + tmpphone
                        if normphone['type'] == PhoneNumberType.FIXED_LINE and len(tmpphone) == 10:
                            normphone['country'] = '54'
                            normphone['urban'] = cod.bloque
                            normphone['line'] = linea
                            normphone['interurban'] = cod_ares
                            normphone['location'] = area
                            normphone['province'] = prov
                            normphone['discable'] = tmpphone
                            normphone['carrier'] = cod.operador
                        else:
                            if  normphone['type'] == PhoneNumberType.MOBILE  and len(tmpphone) == 12:
                                normphone['country'] = '54'
                                normphone['urban'] = cod.bloque
                                normphone['line'] = linea
                                normphone['interurban'] = cod_ares
                                normphone['location'] = area
                                normphone['province'] = prov
                                normphone['discable'] = tmpphone
                                normphone['carrier'] = cod.operador
                            else:
                                normphone['type'] = PhoneNumberType.UNKNOWN
                                normphone['country'] = '54'
                                normphone['urban'] = ''
                                normphone['line'] = ''
                                normphone['interurban'] = ''
                                normphone['location'] = ''
                                normphone['province'] = ''
                                normphone['discable'] = tmpphone
                                normphone['carrier'] = ''

            if normphone['type'] == PhoneNumberType.UNKNOWN:
                longValid = False
                if tmpphone.startswith('11'):
                    tmpphone = tmpphone[2:]
                if teniaQuince or leSaqueElNueve:
                    tmpphone = '15' + tmpphone

                match = re.match('^15[2-7]\d{7}$', tmpphone)

                if not leSaqueElCero and match:
                    normphone['type'] = PhoneNumberType.MOBILE
                    tmpphone = '11' + tmpphone
                    cod_ares = '11'
                    area = 'AMBA'
                    prov = 'AMBA'
                    longValid = True
                if not longValid:
                    match = re.match('^[2-7]\d{7}$', tmpphone)
                    if not leSaqueElCero and match:
                        normphone['type'] = PhoneNumberType.FIXED_LINE
                        tmpphone = '11' + tmpphone
                        longValid = True
                if not longValid:
                    match = re.match('^[2-3]\d{2}15\d{7}$', tmpphone)
                    if match:
                        normphone['type'] = PhoneNumberType.MOBILE
                        longValid = True
                if not longValid:
                    match = re.match('^[2-3]\d{3}15\d{6}$', tmpphone)
                    if match:
                        normphone['type'] = PhoneNumberType.MOBILE
                        longValid = True
                if not longValid:
                    match = re.match('^[2-3]\d{9}$', tmpphone)
                    if match:
                        normphone['type'] = PhoneNumberType.FIXED_LINE
                        longValid = True

                normphone['country'] = '54'
                normphone['urban'] = ''
                normphone['line'] = ''
                normphone['interurban'] = cod_ares if cod_ares else ''
                normphone['location'] = area if area else ''
                normphone['province'] = prov if prov else ''
                normphone['discable'] = tmpphone
                normphone['carrier'] = ''

    return normphone

def format_mx_number(nir, local_number):

    normphone = {}
    serie = local_number[:-4]
    line = local_number[-4:]
    normphone['urban'] = serie
    normphone['line'] =  line
    normphone['type'] = '0'

    listCodes = NumGeoMx.objects.filter(nir=nir,serie=serie,numeracion_inicial__lte=line, numeracion_final__gte=line)
    if listCodes.exists():
        normphone['type'] = 1 if listCodes[0].tipo_red.upper() == 'MOVIL' else 0



    return normphone