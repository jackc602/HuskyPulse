import csv

import pandas as pd

application_csv = "application.csv"
backup_csv = "backup.csv"
club_csv = "club.csv"
comments_csv = "comment.csv"
compliance_csv = "compliance.csv"
event_csv = "event.csv"
feedback_csv = "feedback.csv"
location_csv = "location.csv"
logs_csv = "logs.csv"
post_csv = "post.csv"
post_comments_csv = "post_comment.csv"
roles_csv = "role.csv"
student_csv = "student.csv"
student_club_csv = "student_club.csv"
student_events_csv = "student_event.csv"
student_admin_csv = "system_admin.csv"


def convert_to_csv(csv_file):
    openFile = open('application.csv', 'r')
    csvFile = csv.reader(openFile)
    header = next(csvFile)
    headers = map((lambda x: '`'+x+'`'), header)
    insert = 'INSERT INTO Table (' + ", ".join(headers) + ") VALUES "
    for row in csvFile:
        values = map((lambda x: '"'+x+'"'), row)
        print (insert +"("+ ", ".join(values) +");" )
    openFile.close()



def main():


    application_df = convert_to_csv(application_csv)
    print (application_df)

    # club_df = convert_to_csv(club_csv)
    #
    # comments_df = convert_to_csv(comments_csv)
    #
    # compliance_df = convert_to_csv(compliance_csv)
    #
    # event_df = convert_to_csv(event_csv)
    #
    # feedback_df = convert_to_csv(feedback_csv)
    #
    # location_df = convert_to_csv(location_csv)
    #
    # logs_df = convert_to_csv(logs_csv)
    #
    # posts_df = convert_to_csv(post_csv)
    #
    # post_comments_df = convert_to_csv(post_comments_csv)
    #
    # roles_df = convert_to_csv(roles_csv)
    #
    # student_df = convert_to_csv(student_csv)
    #
    # student_club_df = convert_to_csv(student_club_csv)
    #
    # student_event_df = convert_to_csv(student_events_csv)
    #
    # student_admin_df = convert_to_csv(student_admin_csv)


if __name__ == '__main__':
    main()



