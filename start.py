'''
Run main ETL application process
'''
from __future__ import absolute_import
import wmt_etl.run as job

def main():
    '''Main application entrypoint'''
    job.run()

if __name__ == '__main__':
    main()
