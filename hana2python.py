import sys
import os.path
def get_col_name(s):
    """Takes splitted create sql fragment and returns columnname"""
    start_idx = s.index('"')
    end_idx = s.index('"',start_idx+1)
    return s[start_idx+1:end_idx].strip()


def parse_hana_header(folder):
	""" Load a HANA Exported Table from folder, Returns Header"""
	create_sql_query = open('%s/create.sql' %folder ).read()
	create_sql_query = create_sql_query[create_sql_query.index("("):]
	column_names = [get_col_name(x) for x in create_sql_query.split(", ")[:]]
	return column_names




def read_hanaexport(folder):
	"""Read HANA Export from Folder and return Pandas Dataframe"""
	try:
		import pandas as pd
	except:
		raise Exception("Could not load pandas")

	column_names = parse_hana_header(folder)
	inputfile = None
	options = [("%s/data.csv"%folder, None) , ("%s/data.bz2"%folder, "bz2") , ("%s/data.gz"%folder,"gz") ]
	for filepath, compression_opt in options:
		if os.path.isfile(filepath): 
			inputfile = filepath
			compression = compression_opt
	if not inputfile:
		raise Exception("Could not find 'data' file. Valid inputfilenames are %s" % options)				

	data = pd.read_csv(inputfile,delimiter=",",header=None, names= column_names, compression=compression)
	return data


if __name__ == "__main__":
	sys.exit()