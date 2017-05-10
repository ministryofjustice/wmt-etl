'''
Run main ETL application process
'''

import wmt_etl.etl_config as config

def main():
    '''Main application entry point'''
    print "Running load to {}".format(config.DB_SCHEMA)

if __name__ == '__main__':
    main()
