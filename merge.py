import pandas as pd
mgwr_data = pd.read_excel('MGTWR_Data.xlsx')
final_data_no_duplicates = pd.read_excel('Final_Data_No_Duplicates.xlsx')
# It appears that the new data file contains latitude ('oy') and longitude ('ox') data corresponding to the province.
# We will extract the province, latitude, and longitude, then merge this information into the final dataset.

# Select relevant columns from the new dataset (Province, Latitude, Longitude)
location_data = mgwr_data[['起点省份', 'oy', 'ox']].drop_duplicates()

# Rename columns for consistency with the existing dataset
location_data = location_data.rename(columns={'起点省份': '省份', 'oy': '纬度', 'ox': '经度'})

# Merge the location data into the final dataset
final_data_with_location = pd.merge(final_data_no_duplicates, location_data, on='省份', how='left')

# Save the final data with latitude and longitude to an Excel file
output_file_path_with_location = 'MGTWR_Data_With_Location.xlsx'
final_data_with_location.to_excel(output_file_path_with_location, index=False)

