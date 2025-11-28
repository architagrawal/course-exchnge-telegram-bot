import queryRunner


def findMatchAndShow():
    print('in findMatchAndShow')
    query = """SELECT r1.request_id, r1.user_id, r1.have, r1.want, 
       MIN(r2.request_id) AS matched_request_id, 
       MIN(r2.user_id) AS matched_user_id, 
       MIN(r2.have) AS matched_have, 
       MIN(r2.want) AS matched_want
FROM requests r1
LEFT JOIN requests r2 
    ON r1.have = r2.want 
    AND r1.want = r2.have 
    AND r1.request_id < r2.request_id 
    AND r1.status = 'open' 
    AND r2.status = 'open'
WHERE r2.request_id IS NOT NULL
GROUP BY r1.request_id, r1.user_id, r1.have, r1.want;"""
    matches = queryRunner.find_match(query, True)
    print('out findMatchAndShow')
    for match in matches:
        print(match)
        isOk = input("Want to continue with this data? Enter y/n")
        if isOk.lower() == 'y':
            insertMatchesIntoMatchedtable()


# """ SELECT distinct r1.request_id AS request_id_1, r2.request_id AS request_id_2, r1.user_id AS user_id_1, r2.user_id AS user_id_2
#                 FROM requests r1
#                 INNER JOIN requests r2 ON r1.have = r2.want AND r1.want = r2.have AND r1.request_id <> r2.request_id
#                 where r1.status is null and r2.status is null;"""

# """SELECT r2.request_id, r2.user_id, r2.have, r2.want, r1.request_id AS matched_request_id, r1.user_id AS matched_user, r1.have AS want, r1.want AS have
# FROM requests r1
# INNER JOIN (
#   SELECT r2.have, r2.want, MIN(r2.request_id) AS min_request_id
#   FROM requests r2
#   LEFT JOIN requests r3 ON r3.have = r2.want AND r3.want = r2.have AND r3.request_id > r2.request_id
#   WHERE r3.request_id IS NULL
#   GROUP BY r2.have, r2.want
# ) r4 ON r1.request_id = r4.min_request_id AND r1.have = r4.have AND r1.want = r4.want
# INNER JOIN requests r2 ON r2.have = r1.want AND r2.want = r1.have
# ORDER BY r2.request_id;
# """


def insertMatchesIntoMatchedtable():
    print('in insertMatchesIntoMatchedtable')
    query = """ INSERT IGNORE INTO matchedrequests (requestID1,requestID2)
SELECT r1.request_id,MIN(r2.request_id) 
FROM requests r1
LEFT JOIN requests r2 
    ON r1.have = r2.want 
    AND r1.want = r2.have 
    AND r1.request_id < r2.request_id 
    AND r1.status = 'open' 
    AND r2.status = 'open'
WHERE r2.request_id IS NOT NULL
GROUP BY r1.request_id, r1.user_id, r1.have, r1.want;"""

    matches = queryRunner.find_match(query)
    print('out insertMatchesIntoMatchedtable')
    for match in matches:
        print(match)
    updateMatchedRequestId()


def updateMatchedRequestId():
    query = """UPDATE requests r
JOIN matchedrequests m ON r.request_id = m.requestID1 or r.request_id = m.requestID2
SET r.status = 'FOUND', r.matched_request_id = m.matchID
WHERE r.status = 'OPEN'
limit 1000;"""
    queryRunner.find_match(query)


def main():
    findMatchAndShow()


if __name__ == '__main__':
    main()
