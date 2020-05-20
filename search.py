import datetime

class Search:

    def __init__(self,location,arrival_date=None,departure_date=None,visitors_num=None):
    #constructor tis klasis Search kai einai i methodos +enterSearchFields() apo to sequence diagram

        self.location=location
        self.arrival_date=arrival_date
        self.departure_date=departure_date
        self.visitors_num=visitors_num

    def getAreaList():
        pass

#     def __repr__(self):
#         return f'{self.location}, {self.arrival_date}'


# search1 = Search(location='Patra')
# print(search1)
