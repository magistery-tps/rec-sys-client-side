#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------
import sys
sys.path.append('./src')
from domain_context import DomainContext
#------------------------------------------------------------------------------
#
#
#
#
#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
if __name__ == '__main__':
    DomainContext(
        host      = 'http://localhost:8000',
        temp_path = './temp'
    ).svd_distance_matrix_job.execute()
