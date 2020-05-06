# Using write transactions allow the driver to handle retries and transient errors for you
# write_results = session.write_transaction(create_relationship_between_people, "Alice", "David")
# for result in write_results:
#     print("Create successful: ", result.get("p1"), result.get("p2"))







# with graph._driver.session() as session:
#     # Using write transactions allow the driver to handle retries and transient errors for you
#     write_results = session.write_transaction(query, csv)
#     print(write_results)
#     # for result in write_results:
#     #     print("Create successful: ", result.get("p1"), result.get("p2"))






# Aura requires you to use the "bolt+routing" protocol
# and process your queries using an encrypted connection
# driver = GraphDatabase.driver(uri=uri, auth=basic_auth(user=user, password=password), encrypted=True)

# # SET VARIABLES -----------------------------------------------------
# subject_limit = 40

# def main():
#     with driver.session() as session:

#         topic_result = session.read_transaction(find_main_subjects, subject_limit)
#         records = topic_result.records()
#         for r in records:
#             print(r['t']['subject_eng'])

#         # for result in topic_result:
#         #     print(result.get("topics"))

#     # Don't forget to close the driver connection when you are finished with it
#     driver.close()

# if __name__ == "__main__":
#     main()


# g.read_data(find_main_subjects, 10)
# with graph._driver.session() as session:
#     topic_result = session.read_transaction(find_main_subjects, subject_limit)
#     records = topic_result.records()
#     for r in records:
#         print(r['t']['subject_eng'])