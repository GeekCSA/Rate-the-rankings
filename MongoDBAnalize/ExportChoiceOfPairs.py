import sys
import math
import pymongo
import collections
from bson import ObjectId


def concat_dist(dist_a, dist_b):
    str_a = str(dist_a["star5"]) + "," + str(dist_a["star4"]) + "," + str(dist_a["star3"]) + "," + str(
        dist_a["star2"]) + "," + str(dist_a["star1"])
    str_b = str(dist_b["star5"]) + "," + str(dist_b["star4"]) + "," + str(dist_b["star3"]) + "," + str(
        dist_b["star2"]) + "," + str(dist_b["star1"])

    str_a_b = str_a + "," + str_b

    votes_a = dist_a["total_votes"]
    votes_b = dist_b["total_votes"]

    return str_a_b, votes_a, votes_b


def get_db(table_name):
    # CONNECTION_STRING = "mongodb+srv://star:Qwerty123456@starrankcluster.eotzt.mongodb.net/starrankdb?retryWrites" \
    #                     "=true&w=majority "

    CONNECTION_STRING = "mongodb+srv://star:Qwerty123456@starrankcluster.eotzt.mongodb.net"
    my_client = pymongo.MongoClient(CONNECTION_STRING)
    mydb = my_client["Prod"]

    return mydb[table_name]


def get_dist_from_db(pairs_call, choose):
    # print(choose['id'])
    pairs = None
    if '625b1b0e6b3cc4c792cef183' == str(choose['id']):
        pairs = pairs_call.find({'_id': ObjectId("625b1b0d6b3cc4c792cef176")})
    else:
        pairs = pairs_call.find({'_id': ObjectId(choose['id'])})

    for pair in pairs:
        dist_a = pair['first']
        dist_b = pair['second']

        return dist_a, dist_b


def export_dist(dist_as_dictionary):
    dist = [dist_as_dictionary['star5'],
            dist_as_dictionary['star4'],
            dist_as_dictionary['star3'],
            dist_as_dictionary['star2'],
            dist_as_dictionary['star1']]

    return dist


def calcHPP(dist):
    if dist[0] == 0 and dist[1] == 0 and dist[3] == 0 and dist[4] == 0:
        return sys.maxsize

    a = (dist[0] + dist[1] * 1.) - (dist[3] + dist[4])
    return math.floor(a*10000)/10000


def special_HPP_calc(dist, i, j, k, q):
    if dist[3] == 0 and dist[4] == 0:
        return sys.maxsize
    # dist[0] = 5 stars etc.
    return (i * dist[0] + j * dist[1] * 1.) - (k * dist[3] + q * dist[4])


def check_criticism_question(dist_index, chosen):
    if dist_index == 7 and chosen != 'a':
        return False
    if dist_index == 14 and chosen != 'b':
        return False

    return True


def regular_hpp(dists_info):

    hpp_a = []
    hpp_b = []
    correct_HPP_amount = 0

    for dist in dists_info:
        HPP_a = calcHPP(dist[3])
        HPP_b = calcHPP(dist[4])

        hpp_a.append(HPP_a)
        hpp_b.append(HPP_b)

        if dist[1] > dist[2] and HPP_a > HPP_b:
            correct_HPP_amount += 1
        elif dist[1] < dist[2] and HPP_a < HPP_b:
            correct_HPP_amount += 1
        elif dist[1] == dist[2] and HPP_a == HPP_b:
            correct_HPP_amount += 1

    print("Check HPP, there are ", correct_HPP_amount, "from total ", str(len(dists_info)))

    return correct_HPP_amount, hpp_a, hpp_b


def calcSpecialMean(dist):
    a = (5 * dist[0] + 4 * dist[1] + 2 * dist[3] + dist[4])/100.
    return math.floor(a * 10000) / 10000


def calcMean(dist):
    a = (5 * dist[0] + 4 * dist[1] + 3 * dist[2] + 2 * dist[3] + dist[4])/100.
    return math.floor(a * 10000) / 10000


def special_mean(dists_info):
    mean_a = []
    mean_b = []

    correct_mean_amount = 0
    for dist in dists_info:
        MEAN_a = calcSpecialMean(dist[3])
        MEAN_b = calcSpecialMean(dist[4])

        mean_a.append(MEAN_a)
        mean_b.append(MEAN_b)

        if dist[1] > dist[2] and MEAN_a > MEAN_b:
            correct_mean_amount += 1
        elif dist[1] < dist[2] and MEAN_a < MEAN_b:
            correct_mean_amount += 1
        elif dist[1] == dist[2] and MEAN_a == MEAN_b:
            correct_mean_amount += 1

    print("Check special Mean, there are ", correct_mean_amount, "from total ", str(len(dists_info)))

    return correct_mean_amount, mean_a, mean_b


def regular_mean(dists_info):
    mean_a = []
    mean_b = []

    correct_mean_amount = 0
    for dist in dists_info:
        MEAN_a = calcMean(dist[3])
        MEAN_b = calcMean(dist[4])

        mean_a.append(MEAN_a)
        mean_b.append(MEAN_b)

        if dist[1] > dist[2] and MEAN_a > MEAN_b:
            correct_mean_amount += 1
        elif dist[1] < dist[2] and MEAN_a < MEAN_b:
            correct_mean_amount += 1
        elif dist[1] == dist[2] and MEAN_a == MEAN_b:
            correct_mean_amount += 1

    print("Check Mean, there are ", correct_mean_amount, "from total ", str(len(dists_info)))

    return correct_mean_amount, mean_a, mean_b


def special_hpp(dists_info, correct_HPP_amount):
    # each item {(alpha_for_5, beta_for_1), #correct_ans_from_50}
    correct_special_HPP_dist = set()

    correct_special_HPP_dist.add(((1, 1), correct_HPP_amount))
    count1bigfer5 = 0
    for i in range(0, 20):
        for j in range(0, 20):
            for k in range(0, 20):
                for q in range(0, 20):
                    correct_special_HPP_amount = 0
                    for dist in dists_info:
                        if k == 0 and q == 0:
                            continue

                        HPP_a = special_HPP_calc(dist[3], i/2., j/2., k/2., q/2.)
                        HPP_b = special_HPP_calc(dist[4], i/2., j/2., k/2., q/2.)

                        if dist[1] > dist[2] and HPP_a > HPP_b:
                            correct_special_HPP_amount += 1
                        elif dist[1] < dist[2] and HPP_a < HPP_b:
                            correct_special_HPP_amount += 1
                        elif dist[1] == dist[2] and HPP_a == HPP_b:
                            correct_special_HPP_amount += 1

                    if correct_special_HPP_amount >= correct_HPP_amount and correct_special_HPP_amount >= 49:
                    # if correct_special_HPP_amount >= correct_HPP_amount and correct_special_HPP_amount >= 36:
                        correct_special_HPP_dist.add(((i/2., j/2., k/2., q/2.), correct_special_HPP_amount))
                        if(i > q):
                            count1bigfer5 += 1
    print("1 bigger than 5", count1bigfer5)
    print("special hpp: ", correct_special_HPP_dist)


def biggest(a, b):
    if a > b:
        return "a"
    elif a < b:
        return "b"
    else:
        return "EQUAL"


def to_str(arr):
    return [str(x) for x in arr]


def correct_choose(calc, user):
    if user == "EQUAL" or calc == user:
        return 1
    else:
        return 0


def export_into_learning_file(file_name, dists_info):
    #(index, #choose_a, #choose_b, list_of_dist_a, list_of_dist_b, votes_a, votes_b)
    # dists_info = [(dist, dist_to_choose[dist][0].count('a'), dist_to_choose[dist][0].count('b'),
    #                export_dist(dist_to_choose[dist][1]), export_dist(dist_to_choose[dist][2])) for dist in
    #               dist_to_choose.keys()]

    with open(file_name, "a") as file_object:

        file_object.write(','.join(['a5','a4','a3','a2','a1','b5','b4','b3','b2','b1','mean a','mean b','hpp a','hpp b','votes a','votes b','win']))

        for dist in dists_info:
            dist_a = dist[3]
            dist_b = dist[4]

            mean_a = calcMean(dist_a)
            mean_b = calcMean(dist_b)

            HPP_a = calcHPP(dist_a)
            HPP_b = calcHPP(dist_b)

            votes_a = dist[5]
            votes_b = dist[6]

            choose_a = dist[1]
            choose_b = dist[2]
            win = biggest(choose_a, choose_b)

            line = ','.join(to_str(dist_a) + to_str(dist_b) + [str(mean_a), str(mean_b), str(HPP_a), str(HPP_b), str(votes_a), str(votes_b), win])

            file_object.write("\n" + line)


def export_summary_fil(summary_file_name, dists_info, count_users):
    choose_a = [dist[1] for dist in dists_info]
    choose_b = [dist[2] for dist in dists_info]

    # regular HPP
    correct_HPP_amount, hpps_a, hpps_b = regular_hpp(dists_info)
    correct_mean_amount, means_a, means_b = regular_mean(dists_info)
    correct_special_mean_amount, special_means_a, special_means_b = special_mean(dists_info)
    special_hpp(dists_info, correct_HPP_amount)

    users_win_dist = [biggest(a, b) for a, b in zip(choose_a, choose_b)]
    mean_win_dist = [biggest(a, b) for a, b in zip(means_a, means_b)]
    special_mean_win_dist = [biggest(a, b) for a, b in zip(special_means_a, special_means_b)]
    hpp_win_dist = [biggest(a, b) for a, b in zip(hpps_a, hpps_b)]

    correct_mean_per_users = [correct_choose(mean, user) for mean, user in zip(mean_win_dist, users_win_dist)]
    correct_special_mean_per_users = [correct_choose(mean, user) for mean, user in zip(special_mean_win_dist, users_win_dist)]
    correct_hpp_per_users = [correct_choose(hpp, user) for hpp, user in zip(hpp_win_dist, users_win_dist)]

    with open(summary_file_name, "a") as file_object:
        file_object.write(','.join(["ID"] + to_str(range(1, 1 + len(choose_a)))))
        file_object.write(','.join(["\nusers choose a"] + to_str(choose_a)))
        file_object.write(','.join(["\nusers choose b"] + to_str(choose_b)))
        file_object.write(','.join(["\nbiggest user"] + to_str(users_win_dist)))
        file_object.write("\n")
        file_object.write(','.join(["\nmean a"] + to_str(means_a)))
        file_object.write(','.join(["\nmean b"] + to_str(means_b)))
        file_object.write(','.join(["\nbiggest mean"] + to_str(mean_win_dist)))
        file_object.write("\n")
        file_object.write(','.join(["\nspecial mean a"] + to_str(means_a)))
        file_object.write(','.join(["\nspecial mean b"] + to_str(means_b)))
        file_object.write(','.join(["\nbiggest special mean"] + to_str(mean_win_dist)))
        file_object.write("\n")
        file_object.write(','.join(["\nIS a"] + to_str(hpps_a)))
        file_object.write(','.join(["\nIS b"] + to_str(hpps_b)))
        file_object.write(','.join(["\nbiggest IS"] + to_str(hpp_win_dist)))
        file_object.write("\n")
        file_object.write(','.join(["\ncorrect mean per users"] + to_str(correct_mean_per_users) + ["total success is:",
                                                                                                    str(sum(
                                                                                                        correct_mean_per_users))]))
        file_object.write(','.join(["\ncorrect special mean per users"] + to_str(correct_special_mean_per_users) + ["total success is:",
                                                                                                    str(sum(
                                                                                                        correct_special_mean_per_users))]))
        file_object.write(','.join(["\ncorrect IS per users"] + to_str(correct_hpp_per_users) + ["total success is:",
                                                                                                  str(sum(
                                                                                                      correct_hpp_per_users))]))
        file_object.write("\n")
        file_object.write(','.join(["\nInfo"] + ["amount of users:", str(count_users)]))


def main():

    users_answers = get_db("results")

    # ignore all answers of people that answered not correctly for criticism question
    summary_file_name = "experiment_2_with_validation_subHPP.csv"
    data_for_learning_file_name = "data_for_learning_file_name.csv"
    # myquery = users_answers.find({"experiment_completed": True, "apk_version": "1.0.2", "pages.evaluation_page.passed_validation": True})
    myquery = users_answers.find({"experiment_completed": True, "apk_version": "1.0.1", "pages.evaluation_page.passed_validation": True})

    pairs_call = get_db("distribution-pairs")

    dist_line = set()
    with open('output_file_describe_figures.csv') as f:
        lines = [line.rstrip() for line in f]

    dist_to_choose = {}
    hash_to_choose = {}
    count_users = 0

    for item in myquery:
        count_users += 1

        for choose in item["pages"]["evaluation_page"]["decisions_arr"]:
            dist_a, dist_b = get_dist_from_db(pairs_call, choose)

            concat_dist_str, votes_a, votes_b = concat_dist(dist_a, dist_b)
            dist_index = lines.index(concat_dist_str)

            if dist_index in dist_to_choose:
                dist_to_choose[dist_index][0].append(choose['option'])
            else:
                dist_to_choose[dist_index] = ([choose['option']], dist_a, dist_b, votes_a, votes_b)

    dist_to_choose = collections.OrderedDict(sorted(dist_to_choose.items()))
    # hash_to_choose = collections.OrderedDict(sorted(hash_to_choose.items()))

    for item in hash_to_choose.keys():
        print(item, " ", hash_to_choose[item])

    #(index, #choose_a, #choose_b, list_of_dist_a, list_of_dist_b, votes_a, votes_b)
    dists_info = [(dist, dist_to_choose[dist][0].count('a'), dist_to_choose[dist][0].count('b'), export_dist(dist_to_choose[dist][1]),export_dist(dist_to_choose[dist][2]), dist_to_choose[dist][3], dist_to_choose[dist][4]) for dist in dist_to_choose.keys()]

    print("All the data: \n", dists_info)

    # export_into_learning_file(data_for_learning_file_name, dists_info)
    export_summary_fil(summary_file_name, dists_info, count_users)


def main2():
    ans = [(0, 7, 7), (1, 6, 13), (2, 2, 6), (3, 5, 13), (4, 2, 15), (5, 1, 17), (6, 9, 9), (7, 2, 13), (8, 9, 2), (9, 7, 3), (10, 18, 3), (11, 2, 12), (12, 1, 12), (13, 3, 11), (14, 1, 10), (15, 1, 13), (16, 9, 4), (17, 12, 4), (18, 11, 3), (19, 12, 6), (20, 10, 1), (21, 19, 4), (22, 11, 6), (23, 4, 10), (24, 2, 9), (25, 11, 1), (26, 10, 4), (27, 8, 7), (28, 6, 6), (29, 8, 9), (30, 2, 13), (31, 7, 9), (32, 16, 1), (33, 5, 3), (35, 6, 9), (36, 2, 14), (37, 6, 4), (38, 7, 12), (39, 7, 9), (40, 6, 10), (41, 6, 7), (42, 7, 7), (43, 16, 0), (44, 16, 1), (45, 1, 12), (46, 4, 8), (47, 13, 2), (48, 2, 16), (49, 3, 17), (50, 4, 9), (51, 9, 0)]

    str_a = ""
    str_b = ""
    ratio = []
    index = 0
    for i in range(55):
        if index == len(ans) or i != ans[index][0]:
            print(i)
            str_a += ","
            str_b += ","
        else:
            str_a += str(ans[index][1]) + ","
            str_b += str(ans[index][2]) + ","

            if ans[index][1] == 0:
                ratio.append(ans[index][2])
            elif ans[index][2] == 0:
                ratio.append(ans[index][1])
            elif ans[index][1] > ans[index][2]:
                ratio.append(round((ans[index][1] * 1.) / ans[index][2], 2))
            else:
                ratio.append(round((ans[index][2] * 1.) / ans[index][1], 2))

            index += 1

    print(str_a)
    print(str_b)
    print(','.join([str(r) for r in ratio]))
    print("finish")


if __name__ == '__main__':
    main()
    # main2()
