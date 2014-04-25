from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mrjob.protocol import PickleProtocol

# Use this class to more cleanly pass values
class user:
    """Stores user_id, a list of the ids for the businesses reviewed (bus_ids) and a 
       set version bus_ids_set"""
    def __init__ (self,user_id, bus_ids):
        self.user_id=user_id
        #self.bus_ids=bus_ids
        self.bus_ids_set=set(bus_ids) # This is an unecessary communication expense, but convenient here

class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    # Pickle when passing internal values, allows passing objects
    INTERNAL_PROTOCOL = PickleProtocol

    def get_users(self, _, record):
        """Take in a record, yield <user_id, business_id>"""
        if record['type'] == 'review':
            yield [record['user_id'],record['business_id']]
                                
    def reduce_users(self, user_id, business_ids):
        """ Take in <user_id, business_id> and yield <CONSTANT,user object> for each user that has more than one review"""
        temp=user(user_id,list(business_ids))
        if len(temp.bus_ids_set)>1:
            yield("ALL",temp)

    def jaccardSimilarity( self, key , users ):
        """Takes in all the users and compares them, computing the Jaccard similarity between all possible pairs
        Yields the pairs of user_ids by which have a similarity >= 0.5 and where both one contain at least two reviews"""
       
        # x is a list of the users which have the potential to be similar to another user
        x=list(users)

        # loop over all unique pairs of users
        for i in range(0, len(x)): 
            for j in range(i+1,len(x)):
                # Computes the Jaccard similarity
                jaccard = len(x[i].bus_ids_set & x[j].bus_ids_set) / float(len( x[i].bus_ids_set | x[j].bus_ids_set ))
              
                if jaccard >=0.5:
                    yield( [x[i].user_id,x[j].user_id] , jaccard )
                                            
    def steps(self):
            return [self.mr(mapper=self.get_users, reducer=self.reduce_users),
                    self.mr(reducer=self.jaccardSimilarity)]


if __name__ == '__main__':
    UserSimilarity.run()
