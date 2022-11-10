import pandas as pd
import numpy as np
import scipy
from scipy import stats


def column_calc(datafile,ID):

    #name of the statistical distributions to check.
    dist_names = ['weibull_min','norm','weibull_max','beta',
                'invgauss','uniform','gamma','expon',   
                'lognorm','pearson3','triang']

    #Read your data and set y_std to the column to fit.
    y_main=pd.read_excel(datafile,sheet_name=0)
    y_std=y_main[ID]
    y_std = y_std.dropna()

    #-------------------------------------------------
    chi_square_statistics = []
    size=len(y_std)

    # 20 equi-distant bins of observed Data 
    percentile_bins = np.linspace(0,100,20)
    percentile_cutoffs = np.percentile(y_std, percentile_bins)
    observed_frequency, bins = (np.histogram(y_std, bins=percentile_cutoffs))
    cum_observed_frequency = np.cumsum(observed_frequency)

    # Loop through candidate distributions
    for distribution in dist_names:
        # Set up distribution and get fitted distribution parameters
        dist = getattr(scipy.stats, distribution)
        param = dist.fit(y_std)
        print("{}\n{}\n".format(dist, param))

        # Get expected counts in percentile bins
        # cdf of fitted sistrinution across bins
        cdf_fitted = dist.cdf(percentile_cutoffs, *param)
        expected_frequency = []
        for bin in range(len(percentile_bins)-1):
            expected_cdf_area = cdf_fitted[bin+1] - cdf_fitted[bin]
            expected_frequency.append(expected_cdf_area)

        # Chi-square Statistics
        expected_frequency = np.array(expected_frequency) * size
        cum_expected_frequency = np.cumsum(expected_frequency)
        ss = sum (((cum_expected_frequency - cum_observed_frequency) ** 2) / cum_observed_frequency)
        chi_square_statistics.append(ss)


    #Sort by minimum ch-square statistics
    results = pd.DataFrame()
    results['Distribution'] = dist_names
    results['chi_square'] = chi_square_statistics
    results.sort_values(['chi_square'], inplace=True)

    return (results)

