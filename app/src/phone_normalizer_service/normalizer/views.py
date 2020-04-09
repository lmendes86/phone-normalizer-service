import phonenumbers
from phonenumbers import geocoder, carrier, NumberParseException
from phonenumbers.phonenumber import PhoneNumber
from phonenumbers.phonenumberutil import PhoneNumberType, region_code_for_number

from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404

from .models import *
from .functions import format_ar_number, format_mx_number, cleaner


# Create your views here.


def test(request):
    return HttpResponse('OK')


def geo(request):
    res = {}
    status_code = 200
    if request.method == 'GET':
        if 'number' in request.GET:
            number = request.GET['number']
            country = ''
            if 'country' in request.GET:
                country = request.GET['country']

            tmpphone = cleaner(number, country.upper())

            try:
                parse_number = phonenumbers.parse(tmpphone, country.upper())
            except NumberParseException:
                try:
                    if not tmpphone.startswith('+'):
                        tmpphone = '+' + tmpphone
                    parse_number = phonenumbers.parse(tmpphone, None)
                except NumberParseException:
                    c = get_object_or_404(Country, iata=country.upper())
                    try:
                        parse_number = phonenumbers.parse('+' + c.code+tmpphone.replace('+', ''), country.upper())
                    except:
                        raise Http404('Country {0} does not match with number'.format(country.upper()))

            if not phonenumbers.is_valid_number(parse_number) and country:
                c = get_object_or_404(Country, iata=country.upper())
                try:
                    parse_number = phonenumbers.parse('+' + c.code + tmpphone.replace('+', ''), country.upper())
                except:
                    raise Http404('Country {0} does not match with number'.format(country.upper()))

            if country.upper() == 'AR' or tmpphone.startswith('+54'):
                parse_number = format_ar_number(tmpphone)

                if Country.objects.filter(code='54').exists():
                    country_object = Country.objects.get(code='54')
                    mobile_code = country_object.mobile_code
                    trunk_prefix = country_object.trunk_prefix
                else:
                    mobile_code = '15'
                    trunk_prefix = '0'

                national_number = parse_number['discable']
                region_code = parse_number['interurban']
                country_code = parse_number['country']
                number_type = parse_number['type']
                is_valid = True if number_type != PhoneNumberType.UNKNOWN else False
                location = parse_number['location']
                country = 'Argentina'
                country_iata = 'AR'
                tmpcarrier = parse_number['carrier']
                urbano = parse_number['urban']
                linea = parse_number['line']
                local_number = parse_number['urban'] + parse_number['line']
                is_posible = True if number_type != PhoneNumberType.UNKNOWN else False
                dial_number = phonenumbers.format_number(phonenumbers.parse('+' + country_code + national_number, None), phonenumbers.PhoneNumberFormat.E164)

            else:

                national_number = local_number = str(parse_number.national_number)
                region_code = ''
                country_code = str(parse_number.country_code)
                number_type = carrier.number_type(parse_number)
                is_valid = phonenumbers.is_valid_number(parse_number)
                location = geocoder.description_for_number(parse_number, 'EN')
                country = geocoder.country_name_for_number(parse_number, 'EN')
                country_iata = region_code_for_number(parse_number)
                tmpcarrier = carrier.name_for_valid_number(parse_number, 'EN')
                is_posible = phonenumbers.is_possible_number(parse_number)
                urbano = ''
                linea = ''
                mobile_code = ''
                trunk_prefix = ''
                dial_number = phonenumbers.format_number(parse_number, phonenumbers.PhoneNumberFormat.E164)
                if Country.objects.filter(code=country_code).exists():
                    country_object = Country.objects.filter(code=country_code)
                    if len(country_object) == 1:
                        country_object = country_object[0]
                        country = country_object.name
                        mobile_code = country_object.mobile_code
                        trunk_prefix = country_object.trunk_prefix
                        for i in range(1,5):
                            sub = local_number[:i]
                            if AreaCode.objects.filter(country=country_object, code=sub).exists():
                                ac = AreaCode.objects.get(country=country_object, code=sub)
                                location = ac.name
                                local_number = local_number[i:]
                                region_code = ac.code
                                break

                if country_code == '52' and is_valid:
                    parse_mx_number = format_mx_number(region_code, local_number)
                    urbano = parse_mx_number['urban']
                    linea = parse_mx_number['line']
                    number_type = parse_mx_number['type']

            if is_posible:
                res = {
                    'is_valid': is_valid,
                    'location': location,
                    'country': country,
                    'country_iata': country_iata,
                    'carrier': tmpcarrier,
                    'type': number_type,
                    'dial_number': dial_number,
                    'urban': urbano,
                    'line': linea,
                    'is_posible': is_posible,
                    'ori_number': number,
                    'number_data': {
                        'CC': country_code,
                        'NN': national_number,
                        'AC': region_code,
                        'LN': local_number,
                        'MC': mobile_code,
                        'IM': True if number_type == 1 else (True if location == 'Mobile' else False),
                        'TP': trunk_prefix,
                        'IN': dial_number.replace('+', '').strip()
                    }
                }
            else:
                status_code = 400
                res.update({'code': status_code, 'message': 'invalid number'})
        else:
            status_code = 400
            res.update({'code': status_code, 'message': 'some arguments missing'})
    else:
        status_code = 405
        res.update({'code': status_code, 'message': 'illegal request method ' + str(request.method)})

    response = JsonResponse(res)
    response.status_code = status_code

    return response
