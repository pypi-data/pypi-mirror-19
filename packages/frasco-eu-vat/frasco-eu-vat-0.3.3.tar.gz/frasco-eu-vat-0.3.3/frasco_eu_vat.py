from frasco import (Feature, Service, action, signal, command, cached_property, expose,\
                    request_param, current_app, ServiceError, jsonify, lazy_translate)
from frasco_models import transaction, save_model
from suds.client import Client as SudsClient
from suds import WebFault
import requests
import xml.etree.ElementTree as ET
import datetime
import urllib2


EU_COUNTRIES = {
    "AT": "EUR", # Austria
    "BE": "EUR", # Belgium
    "BG": "BGN", # Bulgaria
    "DE": "EUR", # Germany
    "CY": "EUR", # Cyprus
    "CZ": "CZK", # Czech Republic
    "DK": "DKK", # Denmark
    "EE": "EUR", # Estonia
    "ES": "EUR", # Spain
    "FI": "EUR", # Finland
    "FR": "EUR", # France,
    "GB": "GBP", # Great Britain
    "GR": "EUR", # Greece
    "HR": "HRK", # Croatia
    "HU": "HUF", # Hungary
    "IE": "EUR", # Ireland
    "IT": "EUR", # Italy
    "LT": "EUR", # Lithuania
    "LV": "EUR", # Latvia
    "LU": "EUR", # Luxembourg
    "MT": "EUR", # Malta
    "NL": "EUR", # Netherlands
    "PL": "PLN", # Poland
    "PT": "EUR", # Portugal
    "RO": "RON", # Romania
    "SE": "SEK", # Sweden
    "SI": "EUR", # Slovenia
    "SK": "EUR"  # Slovakia
}

KNOW_VAT_RATES = {
    "AT": 20.0, # Austria
    "BE": 21.0, # Belgium
    "BG": 20.0, # Bulgaria
    "DE": 19.0, # Germany
    "CY": 19.0, # Cyprus
    "CZ": 21.0, # Czech Republic
    "DK": 25.0, # Denmark
    "EE": 20.0, # Estonia
    "ES": 21.0, # Spain
    "FI": 24.0, # Finland
    "FR": 20.0, # France,
    "GB": 20.0, # Great Britain
    "GR": 23.0, # Greece
    "HR": 25.0, # Croatia
    "HU": 27.0, # Hungary
    "IE": 23.0, # Ireland
    "IT": 22.0, # Italy
    "LT": 21.0, # Lithuania
    "LV": 21.0, # Latvia
    "LU": 15.0, # Luxembourg
    "MT": 18.0, # Malta
    "NL": 21.0, # Netherlands
    "PL": 23.0, # Poland
    "PT": 23.0, # Portugal
    "RO": 24.0, # Romania
    "SE": 25.0, # Sweden
    "SI": 22.0, # Slovenia
    "SK": 20.0  # Slovakia
}

ECB_EUROFXREF_URL = 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
ECB_EUROFXREF_XML_NS = 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'
VIES_SOAP_WSDL_URL = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
TIC_SOAP_WSDL_URL = 'http://ec.europa.eu/taxation_customs/tic/VatRateWebService.wsdl'


_exchange_rates_cache = {}
_vat_rates_cache = {}


def is_eu_country(country_code):
    return country_code and country_code.upper() in EU_COUNTRIES


def fetch_exchange_rates():
    today = datetime.date.today()
    if today in _exchange_rates_cache:
        return _exchange_rates_cache[today]
    rates = {'EUR': 1.0}
    try:
        r = requests.get(ECB_EUROFXREF_URL)
        root = ET.fromstring(r.text)
        for cube in root.findall('eu:Cube/eu:Cube/eu:Cube', {'eu': ECB_EUROFXREF_XML_NS}):
            rates[cube.attrib['currency']] = float(cube.attrib['rate'])
        _exchange_rates_cache[today] = rates
    except Exception as e:
        current_app.log_exception(e)
    return rates


VIESClient = None
def get_vies_soap_client():
    global VIESClient
    if not VIESClient:
        VIESClient = SudsClient(VIES_SOAP_WSDL_URL)
    return VIESClient


TICClient = None
def get_ticc_soap_client():
    global TICClient
    if not TICClient:
        TICClient = SudsClient(TIC_SOAP_WSDL_URL)
    return TICClient


class EUVATService(Service):
    name = 'eu_vat'
    url_prefix = '/eu-vat'

    @expose('/rates/<country_code>')
    @request_param('country_code', type=str)
    def get_vat_rate(self, country_code, rate_type=None):
        country_code = country_code.upper()
        if not is_eu_country(country_code):
            raise ServiceError('Not an EU country', 404)
        if not rate_type:
            rate_type = current_app.features.eu_vat.options['vat_rate']
        if country_code not in _vat_rates_cache:
            _vat_rates_cache[country_code] = {}
            try:
                r = get_ticc_soap_client().service.getRates(dict(memberState=country_code,
                    requestDate=datetime.date.today().isoformat()))
                for rate in r.ratesResponse.rate:
                    _vat_rates_cache[country_code][rate.type.lower()] = float(rate.value)
            except Exception as e:
                current_app.log_exception(e)
                _vat_rates_cache.pop(country_code)
                return current_app.features.eu_vat.options['backup_vat_rates'].get(country_code)
        return _vat_rates_cache[country_code].get(rate_type.lower())

    @expose('/validate-vat-number', methods=['POST'])
    @request_param('vat_number', type=str)
    def validate_vat_number(self, vat_number, raise_on_error=True):
        if len(vat_number) < 3:
            if raise_on_error:
                raise ServiceError('VAT number too short', 400)
            return False
        try:
            r = get_vies_soap_client().service.checkVat(vat_number[0:2].upper(), vat_number[2:])
            return r.valid
        except WebFault:
            pass
        return False

    @expose('/exchange-rates/<country_code>', methods=['POST'])
    @expose('/exchange-rates/<country_code>/<src_currency>', methods=['POST'])
    @request_param('country_code', type=str)
    @request_param('src_currency', type=str)
    def get_exchange_rate(self, country_code, src_currency='EUR'):
        if not is_eu_country(country_code):
            raise ServiceError('Not an EU country', 404)
        dest_currency = EU_COUNTRIES[country_code]
        rates = fetch_exchange_rates()
        if src_currency == dest_currency:
            return 1.0
        if src_currency == 'EUR':
            return rates.get(dest_currency, 1.0)
        if src_currency not in rates:
            raise ServiceError('Can only use a currency listed in the ECB rates', 400)
        return round(1.0 / rates[src_currency] * rates.get(dest_currency, 1.0), 5)

    @expose('/check', methods=['POST'])
    @request_param('country_code', type=str)
    @request_param('vat_number', type=str)
    @request_param('amount', type=float)
    @request_param('src_currency', type=str)
    def check(self, country_code, vat_number=None, amount=None, src_currency='EUR'):
        if not is_eu_country(country_code):
            raise ServiceError('Not an EU country', 404)
        is_vat_number_valid = self.validate_vat_number(vat_number, False) if vat_number else False
        o = {
            "country": country_code,
            "currency": EU_COUNTRIES[country_code],
            "vat_rate": self.get_vat_rate(country_code),
            "vat_number": vat_number,
            "is_vat_number_valid": is_vat_number_valid,
            "should_charge_vat": current_app.features.eu_vat.should_charge_vat(country_code, vat_number and is_vat_number_valid),
            "exchange_rate": self.get_exchange_rate(country_code, src_currency),
            "src_currency": src_currency
        }
        if amount:
            rate = 0
            if o['should_charge_vat']:
                rate = o['vat_rate'] / 100
            o.update({"amount": amount,
                      "vat_amount": round(amount * rate, 2),
                      "amount_with_vat": amount + amount * rate,
                      "exchanged_amount_with_vat": round((amount + amount * rate) * o["exchange_rate"], 2)})
        return o


class EUVATFeature(Feature):
    name = "eu_vat"
    defaults = {"own_country": None,
                "vat_rate": "standard",
                "model": None,
                "backup_vat_rates": KNOW_VAT_RATES,
                "invoice_customer_mention_message": lazy_translate("VAT Number: {number}")}

    model_rate_updated_signal = signal('vat_model_rate_updated')
    rates_updated_signal = signal('vat_rates_updated')

    def init_app(self, app):
        app.register_service(EUVATService())
        self.service = app.services.eu_vat

        if self.options['model']:
            self.model = app.features.models.ensure_model(self.options['model'],
                eu_vat_country=str,
                eu_vat_number=str,
                eu_vat_rate=float)
            self.model.should_charge_eu_vat = property(lambda s: self.should_charge_vat(s.eu_vat_country, s.eu_vat_number))

        if app.features.exists('invoicing'):
            app.features.models.ensure_model(app.features.invoicing.model,
                is_eu_country=bool,
                eu_vat_number=str,
                eu_exchange_rate=float,
                eu_vat_amount=float)
            app.features.invoicing.invoice_issueing_signal.connect(self.on_invoice)

    def is_eu_country(self, country_code):
        return is_eu_country(country_code)

    def should_charge_vat(self, country_code, eu_vat_number=None):
        return is_eu_country(country_code) and (self.options['own_country'] == country_code\
            or not eu_vat_number)

    def set_model_country(self, obj, country_code):
        if is_eu_country(country_code):
            obj.eu_vat_country = country_code.upper()
            obj.eu_vat_rate = self.service.get_vat_rate(obj.eu_vat_country)
        else:
            obj.eu_vat_country = None
            obj.eu_vat_rate = None

    @command()
    def update_model_vat_rates(self):
        with transaction():
            query = current_app.features.models.query(self.model)
            for country_code in EU_COUNTRIES:
                rate = self.service.get_vat_rate(country_code)
                for obj in query.filter(eu_vat_country=country_code, eu_vat_rate__ne=rate).all():
                    obj.eu_vat_rate = rate
                    self.model_rate_updated_signal.send(obj)
                    save_model(obj)
            self.rates_updated_signal.send(self)

    def on_invoice(self, sender):
        if is_eu_country(sender.country):
            sender.is_eu_country = True
            if sender.customer:
                sender.eu_vat_number = sender.customer.eu_vat_number
            try:
                sender.eu_exchange_rate = self.service.get_exchange_rate(sender.country, sender.currency)
                if sender.tax_amount:
                    sender.eu_vat_amount = sender.tax_amount * sender.eu_exchange_rate
            except Exception as e:
                current_app.log_exception(e)
                sender.eu_exchange_rate = None
            if sender.eu_vat_number and self.options['invoice_customer_mention_message']:
                sender.customer_special_mention = self.options['invoice_customer_mention_message'].format(
                    number=sender.eu_vat_number)
        else:
            sender.is_eu_country = False