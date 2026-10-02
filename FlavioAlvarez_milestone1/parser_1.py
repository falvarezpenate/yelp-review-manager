# References parser provided by professor.

import json

def formatStr(s):
    return s.replace("'","''").replace("\n"," ")

# helper function to extract attributes
def getBusinessAtt(atts):
    attList = []
    for (att, val) in list(atts.items()):
        # I plan to use these 2 attributes to determine whether a business is pricy, and whether it is popular.
        # Note: for determining if a business is successful, I plan to use the user reviews and none of the attributes for businesses.
        if att == "RestaurantsPriceRange2" or att == "trendy":
            if isinstance(val, dict):
                attList += getBusinessAtt(val)
            else:
                attList.append((att,val))

    return attList


def parseBusinessData():
    with open('.//yelp_business.JSON','r') as file:
        outfile =  open('.//yelp_business.txt', 'w')
        line = file.readline()
        i = 0
        # read all of the lines and extract data
        while line:
            data = json.loads(line)
            business = data['business_id'] #business id
            business_str =  "'" + business + "'," + \
                            "'" + formatStr(data['name']) + "'," + \
                            "'" + formatStr(data['address']) + "'," + \
                            "'" + formatStr(data['city']) + "'," +  \
                            "'" + data['state'] + "'," + \
                            "'" + data['postal_code'] + "'," +  \
                            str(data['stars']) + "," + \
                            str(data['review_count']) + "," + \
            outfile.write(business_str + '\n')

            # extract categories
            for category in data['categories']:
                category_str = "'" + business + "','" + category + "'"
                outfile.write(category_str + '\n')

            # extract attributes using helper function
            for (attr,value) in getBusinessAtt(data['attributes']):
                if str(attr) == "RestaurantsPriceRange2" or str(attr) == "trendy":
                    attr_str = "'" + business + "','" + str(attr) + "','" + str(value)  + "'"
                    outfile.write(attr_str +'\n')

            line = file.readline()
            i +=1

    outfile.close()
    file.close()

# parses all review data.
# Note: got rid of funny and cool because they are irrelevant to the information used for the UI app.
# Kept text because I plan to use it for determining if a business is successful.
# For example, a lot of businesses with loyal customers have reviews such as "I have been going here for at least 5 years..."
# Looking for keywords used in these sort of reviews is what I have in mind for figuring out if a business is successful.
def parseReviewData():
    with open('.//yelp_review.JSON','r') as file:
        outfile =  open('.//yelp_review.txt', 'w')
        line = file.readline()
        i = 0
        while line:
            data = json.loads(line)
            review_str = "'" + data['review_id'] + "'," +  \
                         "'" + data['user_id'] + "'," + \
                         "'" + data['business_id'] + "'," + \
                         str(data['stars']) + "," + \
                         "'" + data['date'] + "'," + \
                         "'" + formatStr(data['text'])
            outfile.write(review_str +'\n')
            line = file.readline()
            i +=1

    outfile.close()
    file.close()

# parses through all user data getting anything that could be useful
# Note: decided to ignore a lot of irrelevant data that will not be useful to the UI shown in the project description.
# For example, got rid of friends, cool, useful, etc.
def parseUserData():
    with open('.//yelp_user.JSON','r') as file:
        outfile =  open('.//yelp_user.txt', 'w')
        line = file.readline()
        i = 0
        while line:
            data = json.loads(line)
            user_id = data['user_id']
            user_str = "'" + user_id + "'," + \
                       "'" + formatStr(data["name"]) + "'," + \
                       str(data["review_count"]) + "," + \
                       str(data["average_stars"])
            outfile.write(user_str+"\n")
            line = file.readline()
            i +=1

    outfile.close()
    file.close()

# parses all checkin data
# every aspect of checkin data is used in the UI, so nothing removed.
def parseCheckinData():
    with open('.//yelp_checkin.JSON','r') as file:
        outfile = open('.//yelp_checkin.txt', 'w')
        line = file.readline()
        i = 0
        while line:
            data = json.loads(line)
            business_id = data['business_id']
            for (dayofweek,time) in data['time'].items():
                for (hour,count) in time.items():
                    checkin_str = "'" + business_id + "',"  \
                                  "'" + dayofweek + "'," + \
                                  "'" + hour + "'," + \
                                  str(count)
                    outfile.write(checkin_str + "\n")
            line = file.readline()
            i +=1

    outfile.close()
    file.close()

# execute all of the parsing
def main():
    print("Starting parser...")
    
    parseBusinessData()
    print("     Finished parsing business data.")

    parseUserData()
    print("     Finished parsing user data.")

    parseCheckinData()
    print("     Finished parsing checkin data.")

    parseReviewData()
    print("     Finished parsing review data.")

    print("All files parsed.")


main()