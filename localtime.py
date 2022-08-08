import json
from astral import LocationInfo
from astral.sun import sun
import pytz
from datetime import datetime , timedelta


## classe clock tem os atributos e metodos necessarios pra se desenhar um relógio completo
class Localtime:

    ## Construtor da classe Localtime.
    # inicializa as variaveis, varre o arquivo procurando a hora com base no offset.
    # atribui as variaveis a cor e o periodo do dia de acordo com a região
    # @param deltahours fuso horario inicial default.
    def __init__(self, deltahours = 0):

        self.timezone = ""
        self.timecolor = ""
        self.period = ""
        self.places = []
        self.latitude = 0
        self.longitude = 0

        try:
            f = open( './localtime.json' , 'r')
            # returns JSON object as a dictionary
            data = json.load(f)
            for c in data['cities']:
                if int(c['offset']) == deltahours:
                    self.timezone = c['region']+'/'+c['city']
                    self.longitude = c['coordinates']['longitude']
                    self.latitude = c['coordinates']['latitude']
            f.close()
        except Exception as e :
            print(e)
            print("No localtime file available")


        self.region, self.local = self.timezone.split("/" )
        self.deltahours = pytz.timezone(self.timezone).utcoffset(datetime.now()).total_seconds()/ 3600


        city = LocationInfo(self.local, self.region, self.timezone, latitude=self.latitude, longitude=self.longitude) 
        
        today = datetime.date(datetime.now())

        h, m, s = datetime.timetuple(datetime.utcnow()+ timedelta(hours = deltahours))[3:6]

        # Sun rise x sun set
        sun_data = sun( city.observer, today, tzinfo = pytz.timezone(self.timezone))

        h_dawn , m_dawn, _         = datetime.timetuple( sun_data['dawn'])[3:6]
        h_sunrise , m_sunrise , _ = datetime.timetuple( sun_data['sunrise'])[3:6]
        h_sunset , ms_sunset, _    = datetime.timetuple( sun_data['sunset'])[3:6]
        h_dusk , m_dusk , _        = datetime.timetuple( sun_data['dusk'])[3:6]

        now = h+m/60

        if now < h_dawn+m_dawn/60:
            #night
            self.timecolor = "#005bc5"
            self.period = "Night"
            return 
        elif now < h_sunrise+m_sunrise/60:
            #sunrise
            self.timecolor = "#fedc57"
            self.period = "Sunrise"
            return 
        elif now < h_sunset+ms_sunset/60:
            #day
            self.timecolor = "#ffb914"
            self.period = "Day"
            return 
        elif now < h_dusk+m_dusk/60:
            #sunset
            self.timecolor = "#6f95ff"
            self.period = "Dusk"
            return 
        else:
            #night
            self.timecolor = "#005bc5"
            self.period = "Night"
            return 


    ## metodo get timecolor da classe Localtime.
    # retorna a cor de acordo com o periodo do dia.  
    def getTimecolor(self):
        return self.timecolor

    ## metodo get Period da classe Localtime.
    # retorna a o periodo do dia.  
    def getTPeriod(self):
        return self.period


# def main():
#     Localtime(0)

# if __name__=='__main__':
#     main()
