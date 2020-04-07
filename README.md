phone-normalizer-service
========================

Phone Normalizer Service is a Django based service which receive phone numbers in many formats
and convert them in standardize international format.
It also gives extra information such as:
* Number validation
* country name and IATA code
* Carrier data
* Type of number (fixed line, mobile, free number, etc.)
* Extra data:
    * CC: Country number code
    * NN: National number format
    * AC: Area code
    * LN: Local number
    * MC: Mobile code prefix
    * IM: Is Mobile flag
    * TP: Trunk prefix
    * IN: International Number

Example requests:
```
International number from China
// http://127.0.0.1/normalization/geo/?number=+86%2021%203323%206666

{
  "is_valid": true,
  "location": "Shanghai",
  "country": "",
  "country_iata": "CN",
  "carrier": "",
  "type": 0,
  "dial_number": "+862133236666",
  "urbano": "",
  "linea": "",
  "is_posible": true,
  "ori_number": " 86 21 3323 6666",
  "number_data": {
    "CC": "86",
    "NN": "2133236666",
    "AC": "",
    "LN": "2133236666",
    "MC": "",
    "IM": false,
    "TP": "",
    "IN": "862133236666"
  }
}
```
For Latin America the Service is more accurate allowing (for most of the countries) to  infer the area code if it's not
sent as part of the parameters.

This three examples are valid for Argentina:
```
Local number from Argentina
// http://127.0.0.1/normalization/geo/?number=+541148910000
// http://127.0.0.1/normalization/geo/?number=1148910000&country=ar
// http://127.0.0.1/normalization/geo/?number=48910000&country=ar

{
  "is_valid": true,
  "location": "AMBA",
  "country": "Argentina",
  "country_iata": "AR",
  "carrier": "TELECOM ARGENTINA STET FRANCE TELECOM SOCIEDAD ANONIMA",
  "type": 0,
  "dial_number": "+541148910000",
  "urbano": "4891",
  "linea": "0000",
  "is_posible": true,
  "ori_number": "48910000",
  "number_data": {
    "CC": "54",
    "NN": "1148910000",
    "AC": "11",
    "LN": "48910000",
    "MC": "15",
    "IM": false,
    "TP": "0",
    "IN": "541148910000"
  }
}
```

Quick start
-----------

1. Run `docker pull lmendes86/phone-normalizer-service:1.0.0`
2. Run `docker run -p 80:80/tcp lmendes86/phone-normalizer-service:1.0.0`
