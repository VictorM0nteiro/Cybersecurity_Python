approved_list = ["elarson", "bmoreno", "tshah", "sgilmore", "eraab"]

username = "bmoreno"

if username in approved_list:
    print("Access Granted")
else:
    print("Access Denied")

organization_hour = True
if organization_hour == True:
    print("Login attempt made during organization hours.")
else:
    print("Login attempt made outside of organization hours.")


# max_num = 10
# num = 1
# while num <= max_num:
#     print(num)
#     num+=1

# string = "Hello"
# for c in string:
#     print(c)

#to control incrementation
# for i in range(1, 12, 2):
#     print(i)

# computer_assets = ["laptop1", "desktop20", "smartphone03"]
# for asset in computer_assets:
#     if asset == "desktop20":
#         break
#         asset = "desktop20"
#     print(asset)

for i in [0, 5]:
    print(i)