# def calculate_rectangle_area(length, width):
#     area = length * width
#     return area


# lenght = int(input())
# width = int(input())
# area = calculate_rectangle_area(lenght, width)
# print("The area of the rectangle is:", area)

def calculate_fails(total_attempts, failed_attempts):
    success_rate = (total_attempts - failed_attempts) / total_attempts * 100
    return success_rate

total_attempts = float(input())
failed_attempts = float(input())
success_rate = calculate_fails(total_attempts, failed_attempts)
print(f"The success rate is: {success_rate:.2f}%")
if(success_rate < 50.00):
    print("you are locked")