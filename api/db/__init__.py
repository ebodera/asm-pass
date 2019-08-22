import string
import random
import pymysql
import datetime

#** Variables **#
_id_chars = string.digits + string.ascii_uppercase + string.ascii_lowercase

# enum event-permissions
EVENT_PERMISSIONS_ATTENDEE  = 0
EVENT_PERMISSIONS_VOLUNTEER = 1
_event_permissions_enum = [
    EVENT_PERMISSIONS_ATTENDEE,
    EVENT_PERMISSIONS_VOLUNTEER,
]

#** Classes **#

class Database:
    """database connector to modify values and retrieve data easily"""

    def __init__(self, auth, host='127.0.0.1', db='apass'):
        assert isinstance(auth, tuple) and len(auth) == 2
        self._conn = pymysql.connect(
            host=host,
            user=auth[0],
            password=auth[1],
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    def _execute(self, cursor, sql, args):
        """wrapper for execution to reconnect to the database"""
        self._conn.ping(reconnect=True)
        cursor.execute(sql, args)

    def _new_id(self, table, field, retries=5):
        """generate a random-id for the table until new"""
        sql = """SELECT 1 FROM {0} WHERE {1}=%s""".format(table, field)
        with self._conn.cursor() as cursor:
            for n in range(retries):
                rid = ''.join(random.choice(_id_chars) for _ in range(10))
                self._execute(cursor, sql, (rid))
                if cursor.fetchone() is None:
                    return rid
            raise Exception('id generation retries exceeded %d' % retries)

    def _id_exists(self, table, field, id_value, deleted=False):
        """raise an error if an id-field exists for the given table"""
        with self._conn.cursor() as cursor:
            sql = "SELECT 1 FROM {0} WHERE {1}=%s AND LogicalDelete=%s".format(
                table, field,
            )
            self._execute(cursor, sql, (id_value, int(deleted)))
            if cursor.fetchone() is None:
                raise Exception('%s: %r not found' % (field, id_value))

    #
    # Table: Users - operations
    #

    def user_new(self, firstname, lastname, email):
        """
        add a new user record under a unique user-id and return the id

        :param firstname: first name of the user
        :param lastname:  last name of the user
        :param email:     the email address of the user
        :return:
            user-id of the user
        """
        email   = email.lower()
        user_id = self._new_id('Users', 'UserID')
        # check if email already exists and then make user account
        self.user_email_exists(email)
        with self._conn.cursor() as cursor:
            sql = """
            INSERT INTO Users
            VALUES (%s, %s, %s, %s, now(), now(), 0)
            """
            self._execute(cursor, sql, (user_id, firstname, lastname, email))
        return user_id

    def user_exists(self, user_id, deleted=False):
        """
        raise an error if the userid does not exist in the database

        :param userid:  id associated with the user
        :param deleted: show deleted records instead if true
        """
        return self._id_exists('Users', 'UserID', user_id, deleted)

    def user_email_exists(self, email):
        """
        raise an error if the user email exists in the database
        """
        sql = """SELECT 1 FROM Users WHERE Email=%s AND LogicalDelete=0"""
        with self._conn.cursor() as cursor:
            self._execute(cursor, sql, (email))
            if cursor.fetchone() is not None:
                raise Exception('email: %s is already taken' % email)

    def user_summary(self, user_id, deleted=False):
        """
        collect a summary of the given user from the database

        :param userid: id associated with the user
        :return:
            dict_keys(
                FirstName,
                LastName,
                Email,
            )
        """
        with self._conn.cursor() as cursor:
            sql = """
            SELECT FirstName, LastName, Email
            FROM Users
            WHERE UserID=%s AND LogicalDelete=%s
            """
            self._execute(cursor, sql, (user_id, int(deleted)))
            return cursor.fetchone()

    def user_update(self, user_id, firstname=None, lastname=None, email=None):
        """
        update information about the given user based on the params given

        :param userid:    id associated witht the user
        :param firstname: new firstname connected w/ the user
        :param lastname:  new lastname connected w/ the user
        :param email:     new email connected w/ the user
        """
        # organize and collect fields that should be modified
        fields = {
            'FirstName': firstname,
            'LastName':  lastname,
            'Email':     email,
        }
        fields = {k:v for k,v in fields.items() if v is not None}
        if len(fields) == 0:
            raise Exception('must modify at least one value')
        # check unique field email
        if email is not None:
            self.user_email_exists(email)
        # make changes with sql
        self.user_exists(user_id)
        with self._conn.cursor() as cursor:
            keys   = ', '.join('%s=%%s' % k for k in fields.keys())
            values = list(fields.values()) + [user_id]
            sql = """
            UPDATE Users
            SET {0}, LastUpdated=now()
            WHERE UserID=%s AND LogicalDelete=0
            """.format(keys)
            self._execute(cursor, sql, values)

    def user_delete(self, user_id):
        """
        delete the given user from the database
        """
        self.user_exists(user_id)
        with self._conn.cursor() as cursor:
            sql = "UPDATE Users SET LogicalDelete=1 WHERE UserID=%s"
            self._execute(cursor, sql, (user_id))

    #
    # Table: Events - operations
    #

    def event_new(self, creator_id, title, description, start_date, end_date):
        """
        create a new event and add a record to the database

        :param creator_id:  user-id associated with the creator
        :param title:       title of the event
        :param description: description of the event
        :param start_date:  the start-date for the event
        :param end_date:    the end-date for the event
        :return:
            the event-id
        """
        assert isinstance(start_date, datetime.datetime)
        assert isinstance(end_date, datetime.datetime)
        self.user_exists(creator_id)
        event_id = self._new_id('Events', 'EventID')
        # check that dates are valid
        if start_date > end_date:
            raise Exception('start_date > end_date')
        # make changes with sql
        with self._conn.cursor() as cursor:
            sql = """
            INSERT INTO Events VALUES (
                %s, %s, %s,
                %s, %s, %s,
                now(), now(), 0
            )
            """
            self._execute(cursor, sql, (
                event_id, creator_id, title, description, start_date, end_date,
            ))
        return event_id

    def event_exists(self, event_id, deleted=False):
        """
        check if event-id already exists in the database

        :param event-id: id associated with the event
        :param deleted:  show deleted records instead if true
        """
        return self._id_exists('Events', 'EventID', event_id, deleted)

    def event_summary(self, event_id, deleted=False):
        """
        collect a summary of the given event from the database

        :param event_id: id associated with the user
        :return:
            dict_keys(
                Creator,
                Title,
                Description,
                StartDate,
                EndDate,
            )
        """
        with self._conn.cursor() as cursor:
            sql = """
            SELECT Creator, Title, Description, StartDate, EndDate
            FROM Events
            WHERE EventID=%s AND LogicalDelete=%s
            """
            self._execute(cursor, sql, (event_id, int(deleted)))
            return cursor.fetchone()

    def event_update(self, event_id,
        title=None,
        description=None,
        start_date=None,
        end_date=None
    ):
        """
        update an event with different information as it is given

        :param title:       title of the event to be changed
        :param description: description of the event to be changed
        :param start_date:   the new stardate of the event
        :param end_date:     the new endstae of the event
        """
        #TODO: check start/end date if they have been modified
        # right now start can be after end because there are no checks
        fields = {
            'Title':       title,
            'Description': description,
            'start_date':   start_date,
            'end_date':     end_date,
        }
        fields = {k:v for k,v in fields.items() if v is not None}
        if len(fields) == 0:
            raise Exception('must modify at least one value')
        # make changes with sql
        self.event_exists(event_id)
        with self._conn.cursor() as cursor:
            keys   = ', '.join('%s=%%s' % k for k in fields.keys())
            values = list(fields.values()) + [event_id]
            sql = """
            UPDATE Events
            SET {0}, LastUpdated=now()
            WHERE EventID=%s AND LogicalDelete=0
            """.format(keys)
            self._execute(cursor, sql, values)

    def event_delete(self, event_id):
        """
        delete the given event from the database

        :param event_id: id associated with the event
        """
        self.event_exists(event_id)
        with self._conn.cursor() as cursor:
            sql = "UPDATE Events SET LogicalDelete=1 WHERE EventID=%s"
            self._execute(cursor, sql, (event_id))
    #
    # Table: rUserToEvent - operations
    #

    def user_list_events(self, user_id, deleted=False):
        """
        list all events associated with the given user

        :param user_id: id associated with user
        :param deleted: show deleted records instead if true
        :return:
            list of event-ids user is enrolled in w/ permissions
        """
        self.user_exists(user_id)
        with self._conn.cursor() as cursor:
            sql = """
                SELECT EventID, Permission, Arrived
                FROM rUserToEvent
                WHERE UserID=%s AND LogicalDelete=%s
            """
            self._execute(cursor, sql, (user_id, int(deleted)))
            return cursor.fetchall()

    def user_event_status(self, user_id, event_id):
        """
        get status of a given user for a particular event

        :param user_id:  id associated with user
        :param event_id: id associated with event
        :return:
            dict_keys([Permission, Arrived])
        """
        self.user_exists(user_id)
        self.event_exists(event_id)
        with self._conn.cursor() as cursor:
            sql = """
            SELECT Permission, Arrived
            FROM rUserToEvent
            WHERE UserID=%s AND LogicalDelete=0 AND EventID=%s
            """
            self._execute(cursor, sql, (user_id, event_id))
            return cursor.fetchone()

    def user_checkin(self, user_id, event_id):
        """
        modify arrived status to true for the given event and user

        :param user_id:  id associated with user
        :param event_id: id associated with event
        """
        self.user_exists(user_id)
        self.event_exists(event_id)
        with self._conn.cursor() as cursor:
            sql = """
            UPDATE rUserToEvent
            SET Arrived=1
            WHERE UserID=%s AND LogicalDelete=0 AND EventID=%s
            """
            self._execute(cursor, sql, (user_id, event_id))
