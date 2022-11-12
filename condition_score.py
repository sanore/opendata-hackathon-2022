
import pandas as pd
import numpy as np


def get_condition_score(constr_year, renov_year):
    # Convert to int
    if pd.notna(constr_year):
        constr_year = int(constr_year)
    if pd.notna(renov_year):
        renov_year = int(renov_year)
    
    # Read and extract construction year data of the city
    city_data = pd.read_csv("data/baujahr.csv", sep=';', usecols=['INDIKATOR_NAME', 'INDIKATOR_JAHR', 'INDIKATOR_VALUE'], encoding='ansi')
    city_data.columns = ['built_after', 'jahr', 'value']
    city_data['built_after'] = city_data['built_after'].str[-8:-4]
    city_data = city_data[city_data['jahr']==city_data['jahr'].max()]
    city_after_2000 = city_data[city_data['built_after']=='2000'].loc[:,'value'].iloc[0]
    city_after_2010 = city_data[city_data['built_after']=='2010'].loc[:,'value'].iloc[0]
    
    # Read and extract data of canton
    canton_columns = ["Vor 1919 2021", "1919-1945 2021", "1946-1960 2021", "1961-1970 2021", "1971-1980 2021", "1981-1990 2021", "1991-2000 2021", "2001-2005 2021", "2006-2021 2021"]
    canton_data = pd.read_csv("data/baudaten_kanton.csv", sep=';', usecols=canton_columns, encoding='ansi')
    column_sums = canton_data.sum().to_numpy()
    # Adjust for mismatched years (linear interpolation)
    column_sums[-1], column_sums[-2] = int(column_sums[-1]*10/15), column_sums[-2] + int(column_sums[-1]*5/15)
    year_after = [1850, 1919, 1945, 1960, 1970, 1980, 1990, 2000, 2010]
    canton_after = column_sums * 100.0 / column_sums.sum()
    # Adept to city numbers (only 2010 & 2000 values are actually available! -> rest has to be estimated)
    city_after = np.zeros_like(canton_after, dtype=float)
    city_after[-2:] = np.array([city_after_2000, city_after_2010])
    city_after[:-2] = canton_after[:-2] * (100-city_after[-2:].sum())/canton_after[:-2].sum()

    years = np.arange(1850, 2021)
    yearly_percentage = np.zeros_like(years, dtype=float)
    canton_idx = 0
    for idx, year in enumerate(years):
        for b_idx, boundary_year in enumerate(year_after):
            if year < boundary_year:
                length = year_after[b_idx] - year_after[b_idx-1]
                canton_idx = b_idx - 1
                break
        yearly_percentage[idx] = city_after[canton_idx] / length
    yearly_percentage = yearly_percentage*100/yearly_percentage.sum()
    
    cum_percentage = np.cumsum(yearly_percentage)
    
    # Calculate score
    if pd.isna(constr_year):
        if renov_year:
            return round(cum_percentage[int(renov_year)-1850-5] * 0.09 + 1.0, 1)
        else:
            return None
    elif constr_year <= 1850:
        constr_score = 1.0
    else:
        constr_score = round(cum_percentage[int(constr_year)-1850] * 0.09 + 1.0, 1)
    
    if pd.isna(renov_year):
        return constr_score
    elif renov_year <= 1850:
        renov_score = 1.0
    else:
        renov_score = round(cum_percentage[int(renov_year)-1850] * 0.09 + 1.0, 1)
    return round(0.8*renov_score + 0.2*constr_score, 1)


if __name__ == "__main__":
    print(get_condition_score(2000, 2020))
    print(get_condition_score(1800, None))
    print(get_condition_score(1999, 2020))
    print(get_condition_score(None, 1960))
    print(get_condition_score(2000, 2001))
    print(get_condition_score(1970, 2020))
    print(get_condition_score(2000, -3))
    print(get_condition_score(1990, 2020))
    print(get_condition_score(2005, 2006))

