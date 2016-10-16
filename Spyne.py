import logging
import requests
import json
import datetime 
import re
logging.basicConfig(level=logging.DEBUG)
from spyne import Application, srpc, ServiceBase, Integer, Unicode
from spyne import Iterable
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication

var1,var2,var3,var4,var5,var6,var7,var8=0,0,0,0,0,0,0,0

class GetCrimeData(ServiceBase):
    
    @srpc(float,float,float,_returns=Unicode)
    def checkcrime(lat, lon, radius):
        global var1,var2,var3,var4,var5,var6,var7,var8
        parameters = {'lat':lat,'lon':lon,'radius':radius,'key':'.'}
        response = requests.get("https://api.spotcrime.com/crimes.json", params=parameters)
        data= response.json()
        crime_count=len(data['crimes'])
        #(crime_count)
        dict2={}
        dict={}
        address=1
        for k in range(crime_count):
            crime_location=data['crimes'][k]['address']
            #return(crime_location)
            if(crime_location.find('ST')!=-1 and crime_location.find('OF')!=-1 and crime_location.find('&')==-1):
                x=crime_location.split('OF ',1)[1]
                Present=x in dict2
                if(Present==False):
                    dict2[x]=1
                else:
                    count=dict2.get(x)
                    count+=1
                    dict2[x]=count
            elif(crime_location.find('&')!=-1):
                y=crime_location.split('&',1)[1]
                z=crime_location.split('&',1)[0]
                Present=y in dict2
                if(Present==False):
                   dict2[y]=1
                else:
                    count1=dict2.get(y)
                    count1+=1
                    dict2[y]=count1
                Present=z in dict2
                if(Present==False):
                    dict2[z]=1
                else:
                    count2=dict2.get(z)
                    count2+=1
                    dict2[z]=count2


            elif(crime_location.find('ST')==-1 and crime_location.find('&')==-1 and crime_location.find('OF')!=-1):
                u=crime_location.split('OF ',1)[1]
                #return(u)
                Present=u in dict2
                if(Present==False):
                    dict2[u]=1
                else:
                    count3=dict2.get(u)
                    count3+=1
                    dict2[u]=count3
            elif(crime_location.find('@')!=-1):
                f=crime_location.split('@',1)[1]
                Present=f in dict2
                if(Present==False):
                    dict2[f]=1
                else:
                    count4=dict2.get(f)
                    count4+=1
                    dict2[f]=count4

        
        if(bool(dict2)==False):
            return "No crimes returned"
        else:    
            Top_3= sorted(dict2.iteritems(), key=lambda x:-x[1])[:3]
            #if(Top_3!="[]"):
            Street1=Top_3[0][0]
            Street2=Top_3[1][0]
            Street3=Top_3[2][0]
            Final_Street=[Street1,Street2,Street3]
        
        dict={}
        
        for i in range(crime_count):
            crime_type=data['crimes'][i]['type']
            Ispresent=crime_type in dict
            if(Ispresent==False):
                dict[crime_type]=1
            else:
                value=dict.get(crime_type)
                value+=1
                dict[crime_type]=value
     
    
        for j in range(crime_count):
            crime_date=data['crimes'][j]['date']
            crime_hour=crime_date[9:11]
            crime_minute=crime_date[12:14]
            #return(crime_date.find('AM'))
            if(crime_date.find('AM')!=-1):
                
                if((crime_hour=='12' and crime_minute!='00') or crime_hour=='01' or crime_hour=='02' or (crime_hour=='03' and crime_minute=='00')):
                    var1+=1
                elif((crime_hour=='03' and crime_minute!='00') or crime_hour=='04' or crime_hour=='05' or (crime_hour=='06' and crime_minute=='00')):
                    var2+=1
                elif((crime_hour=='06' and crime_minute!='00') or crime_hour=='07' or crime_hour=='08' or (crime_hour=='09' and crime_minute=='00')): 
                    var3+=1
                elif((crime_hour=='09' and crime_minute!='00') or crime_hour=='10' or crime_hour=='11' or (crime_hour=='12' and crime_minute=='00')):    
                    var4+=1
            elif(crime_date.find('PM')!=-1):

                if((crime_hour=='12' and crime_minute!='00') or crime_hour=='01' or crime_hour=='02' or (crime_hour=='03' and crime_minute=='00')):
                    var5+=1
                elif((crime_hour=='03' and crime_minute!='00') or crime_hour=='04' or crime_hour=='05' or (crime_hour=='06' and crime_minute=='00')):
                    var6+=1
                elif((crime_hour=='06' and crime_minute!='00') or crime_hour=='07' or crime_hour=='08' or (crime_hour=='09' and crime_minute=='00')): 
                    var7+=1
                elif((crime_hour=='09' and crime_minute!='00') or crime_hour=='10' or crime_hour=='11' or (crime_hour=='12' and crime_minute=='00')):    
                    var8+=1                   


            time={'12:01am-3am':var1,'3:01am-6am':var2,'6:01am-9am':var3,'9:01am-12noon':var4,'12:01pm-3pm':var5,'3:01pm-6pm':var6,'6:01pm-9pm':var7,'9:01pm-12midnight':var8} 
            
        crime_final={"total_crime":crime_count,"the_most_dangerous_streets": Final_Street,"crime_type_count":dict,'event_time_count':time}                
        var1,var2,var3,var4,var5,var6,var7,var8=0,0,0,0,0,0,0,0
        return(crime_final)


application = Application([GetCrimeData],
    tns='spyne.examples.hello',
    in_protocol=HttpRpc(validator='soft'),
    out_protocol=JsonDocument()
)               
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
