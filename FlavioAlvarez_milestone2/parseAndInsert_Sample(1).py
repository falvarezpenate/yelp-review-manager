import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","''").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'

def insert2BusinessTable():
    #reading the JSON file
    with open('.//Yelp-CptS451/yelp_business.JSON','r') as f:
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='XaviErni12'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the cussent business
            # include values for all businessTable attributes
            sql_str = "INSERT INTO Business (business_id, name, address,city,state,postal_code,stars,review_count,number_checkins,review_rating) " + \
                      "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(data["name"]) + "','" + cleanStr4SQL(data["address"]) + "','" + \
                      cleanStr4SQL(data["city"]) + "','" + cleanStr4SQL(data["state"]) + "','" + cleanStr4SQL(data["postal_code"]) + "'," + \
                      str(data["stars"]) + "," + str(data["review_count"])  + ",0,0);"
            try:
                #print(sql_str)
                cur.execute(sql_str)
            except:
                print("Insert to businessTABLE failed!")
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2ReviewTable():
    #reading the JSON file
    with open('.//Yelp-CptS451/yelp_review.JSON','r') as f:
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='XaviErni12'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        '''
        CREATE TABLE Review (
            review_id CHAR(22) Primary Key,
            business_id REFERENCES business(business_id),
            review_text TEXT,
            stars INT,
            review_date DATE
        )
        '''
        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the cussent business
            # include values for all businessTable attributes
            sql_str = "INSERT INTO Review (review_id, business_id, review_text, stars, review_date) " + \
                      "VALUES ('" + cleanStr4SQL(data['review_id']) + "','" + cleanStr4SQL(data["business_id"]) + "','" + cleanStr4SQL(data["text"]) + "'," + \
                      str(data["stars"]) + ",'" + cleanStr4SQL(data["date"])  + "');"
            try:
                #print(sql_str)
                cur.execute(sql_str)
            except:
                print("Insert to reviewTABLE failed!")
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2CheckinTable():
    #reading the JSON file
    with open('.//Yelp-CptS451/yelp_checkin.JSON','r') as f:
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='XaviErni12'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        '''
        CREATE TABLE Checkin (
            business_id CHAR (22),
            FOREIGN KEY (business_id) REFERENCES business(business_id),
            day VARCHAR(9),
            hour VARCHAR(5),
            number_checkins INT
        )
        '''
        while line:
            data = json.loads(line)
            business_id = cleanStr4SQL(data['business_id'])
            for (dayofweek,time) in data['time'].items():
                for (hour,count) in time.items():
                    checkin_str = "'" + cleanStr4SQL(business_id) + "',"  \
                                  "'" + cleanStr4SQL(dayofweek) + "'," + \
                                  "'" + cleanStr4SQL(hour) + "'," + \
                                  str(count)
                    sql_str = "INSERT INTO Checkin (business_id, day, hour, number_checkins) " + \
                              "VALUES (" + checkin_str + ");"
                    try:
                        #print(sql_str)
                        cur.execute(sql_str)
                    except:
                        print("Insert to reviewTABLE failed!")
                    conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2CategoryTable():
    #reading the JSON file
    with open('.//Yelp-CptS451/yelp_business.JSON','r') as f:
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='XaviErni12'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the cussent business
            # include values for all businessTable attributes
            for category in data["categories"]:
                sql_str = "INSERT INTO Category (business_id, category) " + \
                      "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + (category) + "');"
                try:
                    #print(sql_str)
                    cur.execute(sql_str)
                except:
                    print("Insert to categoryTABLE failed!")
                conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

insert2BusinessTable()

insert2ReviewTable()

insert2CheckinTable()

insert2CategoryTable()