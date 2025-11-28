import queryRunner
import datetime
import requestHelper


def addUser(userData):
    print("IN adduser")
    params = {
        'telegram_id': userData.id,
        'first_name': userData.first_name
    }
    query = "INSERT IGNORE INTO users (telegram_id, first_name) VALUES (%(telegram_id)s, %(first_name)s)"
    queryRunner.execute_query(query, params)
    print("OUT adduser")
    return


def fetchAllUserTelegramId():
    query = "SELECT telegram_id FROM users"
    allTelegramIds = queryRunner.find_match(query, True)
    return allTelegramIds


def checkIfUserRequestExist(userData):
    params = {
        'telegram_id': userData.id,
        'first_name': userData.first_name
    }
    query = "SELECT request_id FROM users WHERE telegram_id = %(telegram_id)s AND first_name = %(first_name)s"
    requestId = queryRunner.only_execute_query(query, params)
    print("1")
    print(requestId)
    if (requestId):
        return requestHelper.getRequestFromId(requestId[0])
    return False


def mapRequestIdToUser(userData, request_id):
    print("IN mapRequestIdToUser")
    query = """    
    UPDATE users
    SET request_id = %(request_id)s
    WHERE telegram_id = %(telegram_id)s AND first_name = %(first_name)s;"""
    params = {
        'request_id': request_id,
        'telegram_id': userData.id,
        'first_name': userData.first_name}
    queryRunner.execute_query(query, params)
    print("OUT mapRequestIdToUser")
    return


def addContactNumber(userData, contactNumber):
    print("IN addContactNumber")
    query = """    
    UPDATE users
    SET contact_number = %(contactNumber)s
    WHERE telegram_id = %(telegram_id)s AND first_name = %(first_name)s;"""
    params = {
        'contactNumber': contactNumber,
        'telegram_id': userData.id,
        'first_name': userData.first_name}
    queryRunner.execute_query(query, params)
    print("OUT addContactNumber")
    return


def getrequestId(userData):
    print("IN GETREQUESTID")
    params = {
        'telegram_id': userData.id,
        'first_name': userData.first_name}
    query = """
    SELECT request_id FROM users WHERE first_name = %(first_name)s AND telegram_id =  %(telegram_id)s;"""
    print("OUT GET REQUESTID")
    return queryRunner.only_execute_query(query, params)


def dropRequestForUser(userData):
    print("IN dropRequestForUser")
    requestId = getrequestId(userData)
    print('ok', requestId)
    requestHelper.setStatus(requestId[0], 'DROPPED')
    query = """
        UPDATE USERS SET request_id = NULL where first_name = %(first_name)s AND telegram_id =  %(telegram_id)s;
    """
    params = {
        'telegram_id': userData.id,
        'first_name': userData.first_name}
    queryRunner.execute_query(query, params)
    print("OUT dropRequestForUser")
# def main():


if __name__ == '__main__':
    main()
