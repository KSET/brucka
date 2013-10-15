import os

# this should be one of prod, qa, staging, dev. Default to dev for safety.
env = os.environ.get('APP_ENV', 'dev')

if env == 'dev':
    from dev import *
elif env == 'prod':
    from prod import *

# print locals() # for debugging
