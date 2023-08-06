from IPStreet import client, query

apikey = '5AsaMTe6HUypUlAqv3Rw3E6Pvjo4dYL64Rr2z2va'
api_version = 2

ips_client = client.Client(apikey,api_version)



ips_query = query.PatentData()

names = ["rohinni", "avista utilites", "Next IT"]
for name in names:
    ips_query.add_owner(name)

ips_query.print_current_query()


results = ips_client.send(ips_query)

for asset in results:
    len(asset['forward_citation'])

