import numpy as np
import pandas as pd
import sys
startwd = '/Users/hendrik/Documents/astrohack/'
TEST_PATH = startwd + 'validationdata.csv'


def calculate_chi2(x):
    error = (10**float(x['logMstar_y'])) * np.log(10) * x['err_logMstar']
    return (10**x['logMstar_x']-10**x['logMstar_y'])**2 / error**2


def calculate_full_score(submission_path, test_path=TEST_PATH):
    submission = pd.read_csv(submission_path, delimiter=',', names=['SDSS_ID', 'logMstar'], header=0)
    test = pd.read_csv(test_path, delimiter=',', names=['SDSS_ID', 'logMstar', 'err_logMstar', 'distance'], header=0)
    comparison = pd.merge(submission, test, on='SDSS_ID', how='right')
    comparison.fillna(0, inplace=True)

    # filter -99 values (not in submissions, else it's easy to get chi2=0 as a score)
    comparison = comparison[(comparison.logMstar_y != -99) & (comparison.err_logMstar != 0)]

    comparison['chi2'] = comparison.apply(calculate_chi2, axis=1)
    total_chi2 = np.sum(comparison.chi2)
    return total_chi2


if __name__ == "__main__":
    calculate_full_score(sys.argv[0])
