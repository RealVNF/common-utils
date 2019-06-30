# rounds off the sum of all probabilities in the list to be equal to 1.0
def round_off_list_to_1(prob_list):
    offset = 1 - sum(prob_list)
    # Because of floating point precision (.59 + .33 + .08) can be equal to .99999999
    # So we correct the sum only if the absolute difference is more than a tolerance(0.0000152587890625)
    if len(prob_list) != 0 and abs(offset) > 1 / 2 ** 16:
        # 1 - sum(prob_list) = the difference by which the elements of the list are away from 1.0, could be +'ive /-i've
        # the difference is added/subtracted from the 1st element of the list, which is also rounded to 2 decimal points
        prob_list[0] = round(prob_list[0] + offset, 2)
    assert abs(1 - sum(prob_list)) < 1 / 2 ** 16, "Sum of list not equal to 1.0"
    return prob_list
