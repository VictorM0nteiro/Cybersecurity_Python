adress = "192.223.xx.xx"

#extract the firt 3 characters of the adress
first_3_characters = adress[0:3]
print(first_3_characters)

#.append() adds a imput to the end of a list

IP = ["199.233.xx.xx","111.234.xx.xx","128.235.xx.xx","178.236.xx.xx"]

#extract the first 3 characters of each adress in the list
networks = []
for adress in IP:
    networks.append(adress[0:3])
print(networks)