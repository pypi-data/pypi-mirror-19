# AnalogBridge Python bindings
# API docs at https://analogbridge.io/docs
# Authors:
# Eugene Gekhter <eg@analogbridge.io>

# Configuration variables

api_key = None
api_base = 'https://api.analogbridge.io'
default_api_version = 'v1'
api_version = None

from analogbridge.api_request import APIRequest

from analogbridge.resource import (
    Customer,
    Order,
    Product
)