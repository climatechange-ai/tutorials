import numpy as np

from . import utilities

# Make a dictionary to hold ice core data 
# from the two different expiditions. 
#
# Returns a dictionary icecore_data
def load_data():
    icecore_data = {}
    
    year = 2003
    skiprows = 20
    keys = ['depth', 'age_ice', 'age_air', 'co2']
    
    # Use the file name from the earlier wget command for the 2003 data
    icecore_fname = '/content/drive/My Drive/ccai/course/icecore/vostok.icecore.co2'
    icecore_data[year] = utilities.read_text_file(icecore_fname, skiprows=skiprows, keys=keys)
    
    year = 1999
    skiprows = 60
    keys = ['depth', 'age_ice', 'deuterium', 'temp_variation']
    
    # Use the file name from the earlier wget command for the 1999 data
    icecore_fname = '/content/drive/My Drive/ccai/course/icecore/vostok.1999.temp.dat'
    icecore_data[year] = utilities.read_text_file(icecore_fname, skiprows=skiprows, keys=keys)
    
    return icecore_data

# Data Clean-up:
# Find year alignment of the icecore datasets.
# The two ice core datasets recorded measurements 
# at slightly different depths and took different 
# numbers of samples. We'll have to find which samples
# from the two experiments are closest to each other,
# so that we can compare CO2 and Temperature measurements
# for approximately the same years. 

def align_dates(icecore_data):
    for year in [2003,1999]:
      print(f"{len(icecore_data[year]['age_ice'])} samples in the {year} icecore data")
    
    # Let's find the samples in the 1999 data (the longer set, Global Temperature)
    # that correspond with the samples from 2003 (the shorter set, CO_2)
    # Because the two lists are both in sorted order, 
    # we only have to traverse them once to get the correspondence indexes.
    
    search_idx = 0
    # We start by searching for the 1999 sample for the year that is 
    # closest to the first year in the 2003 data (the current search_year). 
    search_year = icecore_data[2003]['age_ice'][search_idx]
    closest_match_idx = -1
    closest_match_year_diff = 1e6
    match_idxs = []
    for idx, age_ice in enumerate(icecore_data[1999]['age_ice']):
      # Check the different between the search_year 
      # and the current sample from the 1999 data.
      year_diff = np.abs(search_year - age_ice)
    
      # If the sample we are looking at is closer to the 
      # search year than the last sample we looked at,
      # let's update our hypothesis of the closest match
      # to our search_year.
      if year_diff < closest_match_year_diff:
        closest_match_idx = idx
        closest_match_year_diff = year_diff
    
      # If this is not a closer year, 
      # we either need to keep looking,
      # or we may have just passed the closest year.
      # Let's take a deeper look.
      else:
        # If the last year we checked was the closest match...
        if closest_match_idx == idx - 1:
          # Record which 1999 sample matched with our 2003 sample search_year.
          match_idxs.append(idx-1)
          search_idx += 1
    
          # Let's make sure we haven't matched all of the 2003 samples already
          if search_idx > len(icecore_data[2003]['age_ice']) - 1:
            break
    
          # If not, update our search year to the next 2003 sample
          search_year = icecore_data[2003]['age_ice'][search_idx]
          # and reset our closest match from the 1999 data.
          closest_match_idx = idx
          closest_match_year_diff = np.abs(search_year - age_ice)
    
    # Save the corresponding indexes for the 2003 samples to the 1999 samples. 
    icecore_data[1999]['idxs_match_2003'] = match_idxs
    
    matching_years = [icecore_data[1999]['age_ice'][year_idx] for year_idx in icecore_data[1999]['idxs_match_2003']]
    # changing a 'list' to a numpy array lets us use some convenient math functions later
    matching_years = np.array(matching_years)
    matching_temps = [icecore_data[1999]['temp_variation'][year_idx] for year_idx in icecore_data[1999]['idxs_match_2003']]
    matching_temps = np.array(matching_temps)
    
    return matching_years, matching_temps