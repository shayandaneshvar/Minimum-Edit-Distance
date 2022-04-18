from MinimumEditDistance import MinimumEditDistance

if __name__ == '__main__':
    x = "shayan"
    y = 'daneshvar'
    med = MinimumEditDistance(x, y)
    # print(f"distance matrix:\n {med.distance_matrix}")
    # print(f"direction matrix:\n {med.direction_matrix} ")
    # print("------------------------------------------")
    print(f"Strings: {x} & {y}")
    print(f"Minimum Edit Distance is: {med.get_min_dist()}")
    print("Instructions Extracted from results:(from the end to the beginning)")
    # print(med.get_instructions_raw())
    for each in med.get_instructions():
        print(each)
    print("Editing Source to Target Step by Step:")
    for each in med.print_step_by_step():
        print(each)
else:
    print("Run this file as a project not a script!")

# print("By S.Shayan Daneshvar - 9726523")
