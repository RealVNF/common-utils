# rounds off the sum of all probabilities in the list to be equal to 1.0
def round_off_list_to_1(prob_list):
    if len(prob_list) != 0:
        prob_list[0] = round(prob_list[0] + (1 - sum(prob_list)), 2)
    assert abs(1.0 - sum(prob_list)) < 1 / 2 ** 16, "Sum of list not equal to 1.0"
    return prob_list
