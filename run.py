'''
Run main ETL application process
'''

import wmt_etl.etl_config as config


print "Running load to {}".format(config.DB_SCHEMA)
