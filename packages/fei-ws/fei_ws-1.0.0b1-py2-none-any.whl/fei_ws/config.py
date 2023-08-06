FEI_WS_USERNAME = ''
FEI_WS_PASSWORD = ''
FEI_WS_BASE_URL = 'https://data.fei.org/'

# FEI_WS_USERNAME = 'OC_WS_scg_test'
# FEI_WS_PASSWORD = '753scg987'
# FEI_WS_BASE_URL = 'https://validation.family.fei.org'

try:
    from django.conf import settings
    if hasattr(settings, 'FEI_BASE_URL'):
        FEI_WS_BASE_URL = settings.FEI_WS_BASE_URL
    if hasattr(settings, 'FEI_WS_USERNAME'):
        FEI_WS_USERNAME = settings.FEI_WS_USERNAME
    if hasattr(settings, 'FEI_WS_PASSWORD'):
        FEI_WS_PASSWORD = settings.FEI_WS_PASSWORD
except ImportError as e:
    print "Import error ", e.message

