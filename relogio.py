#####################################################
## Curso de Tecnologia em Sistemas de Computação
## Disciplina: Programação Orientada a Objetos
## AD2 1° semestre de 2022.
## Aluno: Jackson Cardoso de Oliveira
####################################################
__author__ = "Jackson Cardoso de Oliveira"

from calendar import month
from datetime import datetime , timedelta
import json
from math import sin , cos , pi
import math
from tkinter import *
from localtime import Localtime

## classe clock tem os atributos e metodos necessarios pra se desenhar um relógio completo
class clock:

    ## Construtor da classe clock.
    # cria o canvas e inicializa as variaveis.
    # @param root contem os elementos do tinker.
    # @param deltahours fuso horario inicial default.
    def __init__(self, root, deltahours = 0):
        self.root        = root
        self.bgcolor     = '#000000'
        self.circlecolor = '#808080'
        self.timecolor   = 'green'
        self.gmtColor    = ""
        self.gmt_fuso    = 0
        self.delta       = deltahours
        self.timezone    = "Faroe"        
        self.main_tmz    = "Sao_Paulo"
        self._ALL        = 'all'
        self.menu        = None
        self.menu_btn    = None
        WIDTH, HEIGHT    = 512, 512

        self.canvas = Canvas(root,
            width        = WIDTH,
            height       = HEIGHT,
            background   = self.bgcolor)
        self.canvas.pack(fill=BOTH, expand=YES)

        self.poll()
  

    ## Converte um vetor de coordenadas polares para cartesianas.
    # - Note que três horas está em 0 graus .
    # - Para o relógio, no entanto , 0º está em doze horas.
    # @param angle ângulo do vetor.
    # @param radius comprimento do vetor.
    # @return um ponto 2D.
    def polar2Cartesian(self, angle, radius=1):
        angle = pi / 2 - angle
        return (radius * cos(angle), radius * sin(angle))
        

    ## Desenha um ponteiro.
    # Atribuindo-se o tag 'handles' aos ponteiros do relógio , a animação dos ponteiros
    # pode ser feita sem ter de redesenhar o canvascompletamente.
    # @param angle angulo do ponteiro.
    # @param len comprimento do ponteiro.
    # @param wid largura ponteiro.
    def draw_handle(self, angle, len, wid= None):
        x, y = self.polar2Cartesian(angle, len)
        cx, cy = self.polar2Cartesian(angle, 0.05)   
        # pega o meio vertical da tela e atribui a h
        h = self.canvas.winfo_height()/2
        w = h

        self.canvas.create_line((w-cx), (h-cy), (w+x), (h-y), fill= self.timecolor, tag= 'handles', width= wid, capstyle= ROUND)
        self.canvas.create_line((w-cx), (h-cy), (w+x), (h-y), fill= "#000", tag= 'handles', width= (wid*0.4), capstyle= ROUND)


    def draw_handle_gmt(self, angle, len, hour, wid= None):
        # pega o meio vertical da tela e atribui a h
        h = self.canvas.winfo_height()/2
        w = h

        x, y = self.polar2Cartesian(angle, len)
        cx, cy = self.polar2Cartesian(angle, 0.05)
        fontgmt = "TkDefaultFont "+ str(int(w*0.04)) +" bold"

        self.canvas.create_line((w-cx), (h-cy), (w+x), (h-y), fill= self.timecolor, tag= 'handles', width= wid, capstyle= ROUND)
        self.canvas.create_oval((w+x)+20,(h-y)+20, (w+x)-20, (h-y)-20, fill= self.gmtColor, tag='rounds')
        self.canvas.create_text((w+x), (h-y), fill="white", font=fontgmt, text= hour, tag='gmthandle')


    ## Desenha o numeral das horas em volta do circulo principal do relógio.
    # Atribuindo-se o tag 'circle' aos circulos 'fixos'
    # Pode ser feita sem ter de redesenhar o canvas completamente.
    #
    # @param w metade da dimensão horizontal da tela.
    # @param h metade da dimensão vertical da tela.
    def draw_hours(self, w, h):
        graus = 0
        scale = h*0.78 # escala numeral de horas 

        # a posição 0, quando o grau é zero representada pelo texto 12 seguindo pelo 1 e assim por diante. 
        array_horas = iter(['12','1','2','3','4','5','6','7','8','9','10','11'])
        # array_gmt = iter(['12','1','2','3','4','5','6','7','8','9','10','11'])

        font = "TkDefaultFont "+ str(int(w*0.06)) +" bold"

        # laço de 0 a 60 para formar um ciclo que inicia em 0 e vai até os 360 graus
        for i in range(0,60):
            radianos = math.radians(graus)

            x, y = self.polar2Cartesian(radianos, scale)

            # para o alinhamento do texto das horas só é desenhado caso o grau seja multiplo de 5.
            if(i%5==0):
                x1 = h + x # coordenadas horizontais para o texto das horas
                y1 = h - y # coordenadas verticais para o texto das horas
                # desenha o circulo com o numeral da hora dentro
                # self.canvas.create_oval(x1+(w*0.08),y1+(h*0.08), x1-(h*0.08), y1-(h*0.08) , fill= 'black', tag='rounds')
                self.canvas.create_text(x1,y1, fill=self.timecolor, font=font, text= next(array_horas), tag='hours')
                x1 = h + x*1.12 # coordenadas horizontais para o texto das horas
                y1 = h - y*1.12 # coordenadas verticais para o texto das horas

                # self.canvas.create_text(x1, y1, fill=self.gmtColor, font=fontgmt, text= int(next(array_gmt))*2, tag='gmtHours')
                ## faz os calculos das coordenadas de acordo com o tamanho da tela
                x2= w + x*1.24
                y2= h - y*1.24
                self.canvas.create_line(x1, y1, x2, y2, width=3, fill=self.gmtColor, tags='lines')

            ## pula as coordenadas aonde as horas foram desenhadas
            else:
                ## faz os calculos das coordenadas de acordo com o tamanho da tela
                x1= w + x*1.15
                y1= h - y*1.15
                x2= w + x*1.22
                y2= h - y*1.22
                ## desenha um linha nas coordenadas
                self.canvas.create_line(x1, y1, x2, y2, width=3, fill=self.gmtColor, tags='lines')
            
            graus += 6


    ## Desenha um menu com a lista das cidades de diferentes fuso horario.
    #
    def menuFuses(self):
        # Inicializa o array que vai armazenar os fusos horarios
        
        h = self.canvas.winfo_height()  # pega a altura da tela

        # Lê o arquivo json e atribui a vaariavel entrada
        with open ('localtime.json') as f:
            entrada = json.load(f)
        
        self.menu = Listbox(self.canvas)
        for i in entrada['cities']:
            city  = str(i['city']).replace("_", " ")
            self.menu.insert(0,(city))

        
        #cria o meno com os nomes das cidades
        self.menu.place(relwidth= 1, relheight=0.85)

        # define as caracteristicas visuais do Listbox
        font = "TkDefaultFont "+ str(int(h*0.04))
        self.menu["justify"] = ["center"]
        self.menu["font"] = font
        self.menu["background" ] = "black"
        self.menu['fg'] = "red"


    ## Desenha o botão e chama o menu com as cidades com fuso horario.
    #  - Ao clicar no botão "aplicar" chama o metodo getClockFuse
    #
    def getTimeFuse(self, event):

        self.menuFuses()
        self.menu_btn = Button(self.canvas, text='aplicar', command= self.setTimeFuse)
        self.menu_btn.place(relwidth= 1,relheight=0.15, rely=0.85)

        # define as caracteristicas visuais do botão
        self.menu_btn["background" ] = "blue"
        self.menu_btn['fg'] = "white"    


    ## Pega o nome da cidade passado pelo setClockFuse e atribui a variavel usada para definir o horarios dos ponteiros do relogio
    # @return fuso horario.
    #
    def setTimeFuse(self, *args):

        x = self.menu.get(ANCHOR)
        with open ('localtime.json') as f:
            entrada = json.load(f)
            
        for i in entrada['cities']:
            city  = str(i['city']).replace("_", " ")
            if city == x:
                self.gmt_fuso = int(i['offset'])
                break

        self.timezone = str(x).replace(" ", "_")
        self.menu.destroy()
        self.menu_btn.destroy()

        return self.timezone


    ## Desenha os elementos presentes na tela.
    # - ponteiros do relogio
    # - circulo onde as horas e ponteiros estão contidos
    # - relogio em formato digital
    #
    def paint_hms(self):
        # remove os componentes visuais de acordo com sua respectiva tag.
        self.canvas.delete('handles')
        self.canvas.delete('gmthandle')

        self.canvas.delete('digital')
        self.canvas.delete('fuso')
        self.canvas.delete('data')

        self.canvas.delete('circleClock')
        self.canvas.delete('circleTimezone')

        self.canvas.delete('hours')
        self.canvas.delete('gmtHours')

        self.canvas.delete('rounds')
        self.canvas.delete('lines')

        # pega a altura da tela e atribui a h
        height = self.canvas.winfo_height()
        # a largura do reloogio recebe altura da tela para manter a proporção
        width = height

        # pega o dia e mes atual
        date = datetime.today().strftime('%b %d')
        # date = datetime.today().strftime('%A, %B %d, %Y %H:%M:%S')[8:14]
        # Para o fuso horário do Rio de Janeiro, o delta vale -3
        # (tres horas para trás ou duas, no horário de verao).
        # hora, minutos e segundos: tempo UTC + delta horas
        h ,m , s = datetime.timetuple(datetime.utcnow()+ timedelta(hours = self.delta))[3:6]
        # horario no formato de 24 horas para o segundo fuso
        h_gmt, m_gmt, _ = datetime.timetuple(datetime.utcnow()+ timedelta(hours = self.gmt_fuso))[3:6]

        oneMin = pi / 30
        fiveMin = pi / 6

        # Um minuto vale 6 graus
        # cinco minutos ou uma hora vale 30 graus
        hora = fiveMin * (h + m / 60.0)
        minutos = oneMin * (m + s / 60.0)
        segundos = oneMin * s
                
        angle_gmt =  fiveMin * (+h_gmt + m_gmt / 60) * 0.5

        hour_text = str(h) + ':' + str(m) + ':' + str(s) # converte o horario em texo

        self.root.title('Relógio em Python - '+hour_text) # muda o titulo da janela

        # inicializa um novo localtime para o gmt
        gmt = Localtime(self.gmt_fuso)
        # pega a cor do periodo do dia para o horario do gmt
        self.gmtColor = gmt.getTimecolor()
        # pega o periodo do dia para o gmt
        gmt_period = gmt.getTPeriod()

        # inicializa um novo localtime para o horario principal
        main_hour = Localtime(self.delta)
        # pega a cor do periodo do dia para o horario principal
        self.timecolor = main_hour.getTimecolor()
        # pega o periodo do dia para o horario principal
        main_period = main_hour.getTPeriod()

        # cria um retângulo para conter a data
        self.canvas.create_rectangle((width*0.735), (height*0.555), (width*0.865), (height*0.605), outline="#2d3839", width=4, fill="", tags='data')

        # cria um circulo para ser o fundo do relogio.
        self.canvas.create_oval((width*0.04), (height*0.04), (width*0.96), (height*0.96), wid=height*0.06, outline='#2d3839', fill= '', tag='circleClock')

        # deixa a fonte em tamanho variavel de acordo com a resolução
        font = "TkDefaultFont "+ str(int(width*0.03)) +" bold"
        # Cria o relogio digital com o fuso principal
        self.canvas.create_text(width/2, height-height/4,text=hour_text, fill=self.timecolor, font=font, tag='digital')

        # remove o inderline do nome da região do fuso
        self.timezone = self.timezone.replace("_"," ")
        font_fuso = "TkDefaultFont "+ str(int(width*0.02)) +" bold"
        # Cria um texto com o nome da região do fuso e o periodo do dia dessa região
        self.canvas.create_text(width/2, height-height/1.3,text=self.timezone +" "+ gmt_period , fill=self.gmtColor, font=font_fuso, tag='fuso')

        # remove o underline do nome da região do horario principal
        self.main_tmz = self.main_tmz.replace("_"," ")
        # Cria um texto com o nome da região do horario principal e o periodo do dia dessa região
        self.canvas.create_text(width/2, height-height/3.5,text=self.main_tmz +" "+ main_period , fill=self.timecolor, font=font_fuso, tag='fuso')

        # desenha um texto com o mês e o dia.
        self.canvas.create_text((width*0.80), (height*0.58),text=date, fill=self.timecolor, font=font_fuso, tag='data')

        # chama o metodo que desenha n atela o numeral das horas dentro de um circulo cada e as linhas da coroa.
        self.draw_hours(width*0.5, height*0.5)


        # Desenha os ponteiros do relogio
        self.timecolor = 'red' # muda a cor do ponteiro do relogio
        # ponteiro com a Hora alternativa (segundo fuso horario) com esala de 24 horas.
        self.draw_handle_gmt(angle_gmt, width*0.45, h_gmt, width*0.008) # Desenha o ponteiro das hora secundária
        # Ponteiros com a Hora normal(primeiro fuso horario) com  esacla de 12 horas, ou seja, 12 horas AM e PM
        self.timecolor = '#fff'
        self.draw_handle(hora, width*0.2, width*0.030) 	     # Desenha o ponteiro das horas
        self.timecolor = '#fff'
        self.draw_handle(minutos, width*0.3, width*0.030)    # Desenha o ponteiro dos minutos
        self.timecolor = '#a8636e'
        self.draw_handle(segundos, width*0.35, width*0.0136)  # Desenha o ponteiro dos segundos

        # Cria dois circulos pequenos no centro, acima dos ponteiros do relogio
        self.canvas.create_oval((width/2)+10, (height/2)+10, (width/2)-10, (height/2)-10, fill= '#fff', tag='circleTimezone')
        self.canvas.create_oval((width/2)+5, (height/2)+5, (width/2)-5, (height/2)-5, fill= '#000', tag='circleTimezone')

        # Pega o click no circulo aconde estão as horas e chama o metodo para alterar o fuso
        self.canvas.bind('<Button>', self.getTimeFuse)

 
    ## Movimenta o relógio, redesenhando os ponteiros
    # após um certo intervalo de tempo.
    #
    def poll(self):
        self.paint_hms() # só é necessário redesenhar os ponteiros a cada 200 ms
        self.root.after(200, self.poll)



def main():
    root= Tk()
    clock(root, -3)
    root.mainloop()

if __name__=='__main__':
    main()
