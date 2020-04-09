phone-normalizer-service
========================

Phone Normalizer Service is a Django based service which receive phone numbers in many formats
and convert them in standardize international format.
It also gives extra information such as:
* Number validation
* country name and IATA code
* Carrier data
* Number type:
```
    FIXED_LINE = 0
    MOBILE = 1
    In some regions (e.g. the USA), it is impossible to distinguish between
    fixed-line and mobile numbers by looking at the phone number itself.
    FIXED_LINE_OR_MOBILE = 2
    Freephone lines
    TOLL_FREE = 3
    PREMIUM_RATE = 4
    The cost of this call is shared between the caller and the recipient,
    and is hence typically less than PREMIUM_RATE calls. See
    http://en.wikipedia.org/wiki/Shared_Cost_Service for more information.
    SHARED_COST = 5
    Voice over IP numbers. This includes TSoIP (Telephony Service over IP).
    VOIP = 6
    A personal number is associated with a particular person, and may be
    routed to either a MOBILE or FIXED_LINE number. Some more information
    can be found here: http://en.wikipedia.org/wiki/Personal_Numbers
    PERSONAL_NUMBER = 7
    PAGER = 8
    Used for "Universal Access Numbers" or "Company Numbers". They may be
    further routed to specific offices, but allow one number to be used for
    a company.
    UAN = 9
    Used for "Voice Mail Access Numbers".
    VOICEMAIL = 10
    A phone number is of type UNKNOWN when it does not fit any of the known
    patterns for a specific region.
    UNKNOWN = 99
```
* Extra data:
    * CC: Country Code
    * NN: National Number Format
    * AC: Area Code
    * LN: Local Number Format
    * MC: Mobile Code Prefix
    * IM: Is Mobile Flag
    * TP: Trunk Prefix
    * IN: International Number Format

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
  "urban": "",
  "line": "",
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
  "urban": "4891",
  "line": "0000",
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
3. In the browser `http://127.0.0.1/normalization/geo/?number=+12345678910`
