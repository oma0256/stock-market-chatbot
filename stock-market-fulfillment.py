import intrinio_sdk
from intrinio_sdk.rest import ApiException

# AWS lambda function
def lambda_handler(event, context):
    """
    Function that is triggered when making a request for a company's
    stock price
    args:
        event(dict): contains information about the request such as
                     action performed
    returns:
        dict: contains the text to return to user after the stock price
              has been fetched
    """
    queryResult = event['queryResult']
    action = queryResult['action']
    parameters = queryResult['parameters']
    response = get_fulfillment_response(action, parameters)
    return { 'fulfillmentText': response }

def map_company_and_price():
    """
    Maps company name and price type to match those of intrinio
    returns:
        tuple: containing the mapped price types and company name
    """
    price_map = {
        'opening': 'open_price',
        'closing': 'closing_price',
        'high': 'high_price',
        'maximun': 'high_price',
        'low': 'low_price',
        'minimum': 'low_price',
    }
    company_map = {
        'apple': 'AAPL',
        'microsoft': 'MSFT',
        'ibm': 'IBM',
    }
    return price_map, company_map

def get_fulfillment_response(action, parameters):
    """
    Returns a text response after fulfillment has been made
    args:
        action(str): representing the intent that the bot is refering to
        parameters(dict): contains the entities of the bot
    returns:
        str: text response depending on if the fulfillment for getting
             stock price has succeded or not
    """
    response = ''
    if action != 'input.getStockPrice':
        response = "I have no idea what you're asking for."
    else:
        response = get_stock_price(parameters)
    return response

def get_stock_price(parameters):
    """
    Makes an request for a company's stoke price
    args:
        parameters(dict): contains the entities of the bot
    returns:
        str: text response based on the api call
    """
    price_type = parameters['price_type']
    company_name = parameters['company_name']
    date = parameters['date']
    price_map, company_map = map_company_and_price()
    intrinio_sdk.ApiClient().configuration.api_key['api_key'] = \
    'OmI1NDcxMWU5ZTZhNTM3NjFmNGUxM2M0YzllMGU5NjA0'
    company_api = intrinio_sdk.CompanyApi()
    identifier = company_map[company_name.lower()]
    tag = price_map[price_type.lower()]

    opts = {
        'start_date': date,
        'end_date': '',
    }
    try:
        data = company_api.get_company_historical_data(identifier, tag, **opts)
        stock_price = data.historical_data[0].value
        response = \
        f'The {price_type} price for {company_name} on {date} was {stock_price}'
        return response
    except ApiException as e:
        print(e)
