'''
Created on 5. 1. 2017

@author: ppavlu
'''

import requests, json

class sparkAccess:
    '''
    classdocs
    '''
    


    def __init__(self, Token):
        '''
        Constructor
        '''
        self.APIURL="https://api.ciscospark.com/hydra/api/v1"
        self.AuthorizationInfo={'content-type':'application/json','Authorization': "Bearer "+Token}
        
    def GetRoomsFromSpark(self):
        # Returns list of rooms the user is member of (in the plain response of the API call)
        r=""
        try:
            r=requests.get(self.APIURL+'/rooms',headers=self.AuthorizationInfo)
        except (IOError):
            print ("Access to network server failed: ",self.APIURL)
        return r
    
    def IsRoomInSpark(self, room, roomlist):
        # room is the (text) name of Spark room, roomlist is the JSON structure with room list
        # Returns roomId if the room is in the response, and empty string if the room is not present
        roomId=''
        jsonData=json.loads(roomlist)
        jsonList=jsonData['items']
        for roomItem in jsonList:
            if roomItem['title']==room:
                roomId=roomItem['id']
        return roomId
    
    def PostMessageToSparkRoom(self, roomId, MessageText):
        # Posts MessageText to spark room roomId, returns the response of the API call used
        DataString={"roomId": roomId, "text": MessageText}
        r=""
        try:
            r=requests.post(self.APIURL+'/messages',headers=self.AuthorizationInfo,data=json.dumps(DataString))
        except (IOError):
            print ("Access to network server failed: ",self.APIURL)
        return r
    
    def PostMessageToSparkRoomByName(self, roomName, MessageText):
        # Posts MessageText to spark room roomName, returns the response of the API post call or 0 if error encountered
        roomList=self.GetRoomsFromSpark()
        roomid=self.IsRoomInSpark(roomName, roomList.text)
        if roomid == '':
            print("Requested room not found, exiting.")
            return 0
        else:
            result=self.PostMessageToSparkRoom(roomid, MessageText)
            return result.status_code
    
    