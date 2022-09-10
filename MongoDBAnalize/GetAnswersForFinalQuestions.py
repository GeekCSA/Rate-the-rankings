import pymongo
from datetime import datetime


def print_ans(list_ans_1):
    for (num, ans) in enumerate(list_ans_1):
        print(num, ") ", ans)


if __name__ == "__main__":

    CONNECTION_STRING = "mongodb+srv://star:Qwerty123456@starrankcluster.eotzt.mongodb.net/starrankdb?retryWrites=true&w=majority"
    myclient = pymongo.MongoClient(CONNECTION_STRING)

    mydb = myclient["Prod"]
    print(myclient.list_database_names())

    mycoll = mydb["results"]
    print(mydb.list_collection_names())

    # myquery = mycoll.find({}, {"pages.consent_page.times.start_time_client": 1, "pages.feedback_page.times.end_time_client": 1})
    myquery = mycoll.find({'apk_version': '1.0.2', 'experiment_completed': True, "pages.evaluation_page.passed_validation": True})

    listUser = []

    for item in myquery:

        start_time_str = None
        end_time_str = None
        start_time = None
        end_time = None
        questions = None

        id = item["_id"]

        if("pages" in item):
            if ("consent_page" in item["pages"]):
                if ("times" in item["pages"]["consent_page"]):
                    if ("start_time_client" in item["pages"]["consent_page"]["times"]):
                        start_time_str = item["pages"]["consent_page"]["times"]["start_time_client"]
                        # print(item["pages"]["consent_page"]["times"]["start_time_client"])
                    else:
                        pass
                        # print("Has no start_time_client")
                else:
                    pass
                    # print("Has no times")
            else:
                pass
                # print("Has no consent_page")
        else:
            # print("Has no pages")
            pass

        if "pages" in item:
            if ("feedback_page" in item["pages"]):
                if ("times" in item["pages"]["feedback_page"]):

                    q1 = item["pages"]["feedback_page"]["Q-reasoning"]
                    q2 = item["pages"]["feedback_page"]["Q-affect"]
                    q3 = item["pages"]["feedback_page"]["Q-importance"]
                    q4 = item["pages"]["feedback_page"]["Q-otherInfo"]
                    q5 = item["pages"]["feedback_page"]["Q-issues"]

                    questions = (q1,q2,q3,q4,q5)

                    if ("end_time_client" in item["pages"]["feedback_page"]["times"]):
                        end_time_str = item["pages"]["feedback_page"]["times"]["end_time_client"]
                        # print("###", item["pages"]["feedback_page"]["times"]["end_time_client"])
                    else:
                        pass
                        # print("Has no end_time_client")
                else:
                    pass
                    # print("Has no times")
            else:
                pass
                # print("Has no feedback_page")
        else:
            pass
            # print("Has no pages")

        if start_time_str != None:
            start_time = start_time_str[:-4]
            start_time = start_time.replace(".", "/")
            start_time = datetime.strptime(start_time, '%d/%m/%Y %H:%M:%S')

        if end_time_str != None:
            end_time = end_time_str[:-4]
            end_time = end_time.replace(".", "/")
            end_time = datetime.strptime(end_time, '%d/%m/%Y %H:%M:%S')

        diff_time = None
        if end_time_str != None and start_time_str != None:
            diff_time = end_time - start_time


        tuple_user = (id, start_time_str, end_time_str, diff_time, questions)

        listUser.append(tuple_user)


    all_times = None
    num = 1
    list_ans_1 = []
    list_ans_2 = []
    list_ans_3 = []
    list_ans_4 = []
    list_ans_5 = []
    list_ans_6 = []
    list_ans_7 = []

    for user in listUser:

        if user[3] != None:
            # print(num, ") ", "id: ", user[0], ", start: ", user[1], ", end: ", user[2], ", diff: ", user[3])
            num += 1
            if all_times == None:
                all_times = user[3]
            else:
                all_times = all_times + user[3]

        if user[4] != None:
            list_ans_1.append(user[4][0])
            list_ans_2.append(user[4][1])
            list_ans_3.append(user[4][2])
            list_ans_4.append(user[4][3])
            list_ans_5.append(user[4][4])
            # for q in user[4]:
            #     print("*\t", q)

    print("Answer for 1:\n")
    print_ans(list_ans_1)
    print("Answer for 2:\n")
    print_ans(list_ans_2)
    print("Answer for 3:\n")
    print_ans(list_ans_3)
    print("Answer for 4:\n")
    print_ans(list_ans_4)
    print("Answer for 5:\n")
    print_ans(list_ans_5)

    # print(all_times)



