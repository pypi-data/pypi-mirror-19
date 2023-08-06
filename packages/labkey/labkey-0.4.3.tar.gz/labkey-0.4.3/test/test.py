# This script targets the client api version 0.4.0 and later
import labkey

server_context = labkey.utils.create_server_context('www.labkey.org', 'home/Demos/Study/demo', use_ssl=True)

my_results = labkey.query.select_rows(server_context, 'study', 'Demographics', max_rows=1)

print('number of rows: ' + str(len(my_results['rows'])))
