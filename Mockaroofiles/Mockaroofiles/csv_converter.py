import csv
import os

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
system_admin_csv = "system_admin.csv"


def convert_to_sql(csv_file, table_name):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        headers = [f'`{col}`' for col in headers]
        for row in reader:
            values = [f'"{v}"' for v in row]
            print(f"INSERT INTO `{table_name}` ({', '.join(headers)}) VALUES ({', '.join(values)});")


def main():

    # student = convert_to_sql('student.csv', 'student')
    # print(student)

    # club_df = convert_to_sql('club.csv', 'club')
    # print(club_df)

    # student_club_df = convert_to_sql(student_club_csv, "student_club")
    # print(student_club_df)

    # location_df = convert_to_sql(location_csv, "location")
    # print(location_df)

    # event_df = convert_to_sql(event_csv, "event")
    # print(event_df)

    # student_event_df = convert_to_sql(student_events_csv, "student_event")
    # print(student_event_df)

    # posts_df = convert_to_sql(post_csv, "posts")
    # print(posts_df)

    # comments_df = convert_to_sql(comments_csv, "comments")
    # print(comments_df)

    # post_comments_df = convert_to_sql(post_comments_csv, "post_comments")
    # print(post_comments_df)

    # system_admin_df = convert_to_sql(system_admin_csv, "system_admin")
    # print(system_admin_df)

    # feedback_df = convert_to_sql(feedback_csv, "feedback")
    # print(feedback_df)

    # application_df = convert_to_sql(application_csv, "application")
    # print (application_df)

    # backup_df = convert_to_sql(backup_csv, "backup")
    # print("backup_df")

    # logs_df = convert_to_sql(logs_csv, "logs")
    # print(logs_df)

    # roles_df = convert_to_sql(roles_csv, "role")
    # print(roles_df)

    compliance_df = convert_to_sql(compliance_csv, "compliance")
    print(compliance_df)


if __name__ == '__main__':
    main()