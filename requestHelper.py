
import queryRunner
import userHelper


def addSelections(userData, haveCourse, wantCourse):
    print("IN addSelections")
    params = {
        'have': haveCourse,
        'want': wantCourse,
        'telegram_id': userData.id,
        'first_name': userData.first_name
    }
    query = """
    INSERT INTO requests (user_id, have, want)
    SELECT users.user_id, %(have)s, %(want)s
    FROM users
    WHERE users.telegram_id = %(telegram_id)s and users.first_name = %(first_name)s;"""
    request_id = queryRunner.execute_query(query, params)
    userHelper.mapRequestIdToUser(userData, request_id)
    print("OUT addSelections")
    return request_id


def getRequestFromId(requestId):
    print("IN getRequestFromId")
    params = {
        'request_id': requestId
    }
    query = "SELECT have, want, created_date, status, matched_request_id FROM requests WHERE request_id = %(request_id)s;"
    requestDetails = queryRunner.only_execute_query(query, params)
    print(requestDetails)
    if (requestDetails):
        dt = requestDetails[2]
        d = dt.date()
        details = {'have': requestDetails[0],
                   'want': requestDetails[1],
                   'date_created': d,
                   'status': requestDetails[3],
                   'matched_request_id': requestDetails[4]}
        print("OUT getRequestFromId")
        return details
    print("OUT getRequestFromId")
    return False


def setStatus(requestId, status):
    print("IN setStatus")
    params = {
        'request_id': requestId,
        'statusString': status}
    query = "UPDATE requests SET status = %(statusString)s WHERE request_id = %(request_id)s"
    queryRunner.execute_query(query, params)
    print("out setStatus")
    return
