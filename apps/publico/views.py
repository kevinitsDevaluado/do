from datetime import datetime
from importlib.metadata import files
from traceback import extract_tb
from venv import create
from django.shortcuts import redirect, render
from numpy import extract
from apps.administrador.models import *
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import connection
from django.views.generic import  TemplateView, View


import datetime


# Create your views here.

class Home(View):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        galeria=Galeria.objects.filter(estado_gal=True).order_by('-id')[:8]
        institucion = Institucion.objects.all()
        answer= Preguntas.objects.all()
        return render(request,self.template_name,{'galerias':galeria,'instituciones':institucion,'answers':answer,'navbar':'Home'})




"_______________________________________________clases para vistas de usuarios publicos_________________________________"
#Pagina Principal Dashboard
class Transparencia(TemplateView):
    template_name = 'transparencia.html'
    def get(self, request,*args,**kwargs):
        #llamar a los modelos 
        #fin llamar a los modelos
        # comandos para consultas sql 
        cursor=connection.cursor()
        sql=(f"select  carpeta.nombre_car, carpeta.id from carpeta order by  carpeta.nombre_car desc")
        cursor.execute(sql)
        inner=cursor.fetchall()
        # fin comando para consultas sql
        # comandos para consultas sql 1
        sql2=(f"select subcarpeta.id,subcarpeta.nombre_sub,carpeta_subcarpeta.fk_id_sub_id,carpeta.id,carpeta_subcarpeta.id  from carpeta inner join carpeta_subcarpeta on (carpeta.id=carpeta_subcarpeta.fk_id_car_id)  inner join subcarpeta on (subcarpeta.id=carpeta_subcarpeta.fk_id_sub_id)  order by CASE subcarpeta.nombre_sub  WHEN 'Enero'  THEN 1 WHEN 'Febrero' THEN 2 WHEN 'Marzo' THEN 3	WHEN 'Abril' THEN 4	WHEN 'Mayo' THEN 5	WHEN 'Junio' THEN 6	WHEN 'Julio' THEN 7 	WHEN 'Agosto' THEN 8 WHEN 'Septiembre' THEN 9 WHEN 'Octubre' THEN 10 	WHEN 'Noviembre' THEN 11 WHEN 'Diciembre' THEN 12    ELSE '0' END;")
        cursor.execute(sql2)
        inner2=cursor.fetchall()
        # fin comando para consultas sql 2
        # comandos para consultas sql 3
        sql3=(f"select *from archivo ")
        cursor.execute(sql3)
        inner3=cursor.fetchall()
        # fin comando para consultas sql 3
        # redireccionamiento a las vistas 
        
        return render(request,self.template_name,{'join':inner,'join2':inner2,'join3':inner3,'navbar':'Transparencia'})
        # fin redireccionamiento a las vistas 
        
        
    def post(self, request, *args, **kwargs):
        queryset = request.POST.get("buscar")
        cursor=connection.cursor()
        sql=(f"select  carpeta.nombre_car, carpeta.id from carpeta order by  carpeta.nombre_car desc")
        cursor.execute(sql)
        inner=cursor.fetchall()
        sql2=(f"select subcarpeta.id,subcarpeta.nombre_sub,carpeta_subcarpeta.fk_id_sub_id,carpeta.id,carpeta_subcarpeta.id  from carpeta inner join carpeta_subcarpeta on (carpeta.id=carpeta_subcarpeta.fk_id_car_id)  inner join subcarpeta on (subcarpeta.id=carpeta_subcarpeta.fk_id_sub_id)  order by CASE subcarpeta.nombre_sub  WHEN 'Enero'  THEN 1 WHEN 'Febrero' THEN 2 WHEN 'Marzo' THEN 3	WHEN 'Abril' THEN 4	WHEN 'Mayo' THEN 5	WHEN 'Junio' THEN 6	WHEN 'Julio' THEN 7 	WHEN 'Agosto' THEN 8 WHEN 'Septiembre' THEN 9 WHEN 'Octubre' THEN 10 	WHEN 'Noviembre' THEN 11 WHEN 'Diciembre' THEN 12    ELSE '0' END;")
        cursor.execute(sql2)
        inner2=cursor.fetchall()
        sql3=(f"select *from archivo ")
        cursor.execute(sql3)
        inner3=cursor.fetchall()
        s='datos actuales'
        if queryset:
            archivo = Archivo.objects.filter(
            Q(nombre_arch__icontains = queryset) |
            Q(contenido_arch__icontains = queryset) 
        ).distinct()#Funcion para que la consulta tome los valores con el conector logico O
            
        if(request.POST.get("buscar") =="" ):
            sql=(f"select  carpeta.nombre_car, carpeta.id from carpeta order by  carpeta.nombre_car desc")
            cursor.execute(sql)
            inner=cursor.fetchall()
            sql2=(f"select subcarpeta.id,subcarpeta.nombre_sub,carpeta_subcarpeta.fk_id_sub_id,carpeta.id,carpeta_subcarpeta.id  from carpeta inner join carpeta_subcarpeta on (carpeta.id=carpeta_subcarpeta.fk_id_car_id)  inner join subcarpeta on (subcarpeta.id=carpeta_subcarpeta.fk_id_sub_id)  order by CASE subcarpeta.nombre_sub  WHEN 'Enero'  THEN 1 WHEN 'Febrero' THEN 2 WHEN 'Marzo' THEN 3	WHEN 'Abril' THEN 4	WHEN 'Mayo' THEN 5	WHEN 'Junio' THEN 6	WHEN 'Julio' THEN 7 	WHEN 'Agosto' THEN 8 WHEN 'Septiembre' THEN 9 WHEN 'Octubre' THEN 10 	WHEN 'Noviembre' THEN 11 WHEN 'Diciembre' THEN 12    ELSE '0' END;")
            cursor.execute(sql2)
            inner2=cursor.fetchall()
            sql3=(f"select *from archivo ")
            cursor.execute(sql3)
            inner3=cursor.fetchall()
            x='no'
            return render(request,'transparencia.html',{'no':x,'join':inner,'join2':inner2,'join3':inner3,'navbar':'Transparencia'})
        
        elif(request.POST.get("buscar") != None):
            return render(request,'transparencia.html',{'archivos':archivo,'join':inner,'join2':inner2,'join3':inner3,'navbar':'Transparencia'})

        elif(request.POST.get("buscar") == None):
            return render(request,'transparencia.html',{'archivos':archivo,'join':inner,'join2':inner2,'join3':inner3,'navbar':'Transparencia'})

        return render(request,'transparencia.html',{'actual':s,'join':inner,'join2':inner2,'join3':inner3,'navbar':'Transparencia'})


    


class Resoluciones(TemplateView):
    template_name = 'resoluciones.html'
    def get(self, request,*args,**kwargs):
        #sql de transparencia
        cursor=connection.cursor()
        sql11=(f"select  carpeta.nombre_car,carpeta.id from carpeta order by  carpeta.nombre_car desc")
        cursor.execute(sql11)
        inner=cursor.fetchall()
        #fin sql de transparencia

        return render(request,self.template_name,{'join':inner,'navbar':'Resoluciones'})


from django.core.validators import URLValidator
from django.core.exceptions import ValidationError



class Verdirectorio(TemplateView):
    template_name = 'resolucionesdirectorio.html'
    def get(self, request,directorio_id,*args,**kwargs):
        # captura de variable de id
        x=directorio_id
        #sql de directorio
        cursor=connection.cursor()
        sql1=(f"SELECT *From directorio Where directorio.fk_id_dir_id={x}")
        cursor.execute(sql1)
        join=cursor.fetchall()
        #fin sql de directorio
        #sql de año que pertenece el directorio
        sql2=(f" SELECT carpeta.nombre_car from carpeta inner join directorio on (carpeta.id=directorio.fk_id_dir_id) where directorio.fk_id_dir_id={x}")
        cursor.execute(sql2)
        anio=cursor.fetchall()
        #fin sql de año que pertenece el directorio
        #sql para obtener el año del modelo carpeta
        sql3=(f"SELECT *from carpeta where carpeta.id='{x}'")
        cursor.execute(sql3)
        ir=cursor.fetchall()
        #------obtener el contador segun la id del fk de directorio que se obtiene al ingresar a la página-------
        #servira para validar el envio y las vistas
        sql10=(f"SELECT contadorvistasdirectorio.directorio_con from contadorvistasdirectorio where contadorvistasdirectorio.fk_id_con_id={x}   ")
        cursor.execute(sql10)
        verea=cursor.fetchall()
        ###id de la columna del directorio para poder obtener el archivo segun la fila seleccionada
        #sql para obtener el id de directorio para redireccionar el boton al template vista de archivo
        sql5=(f"SELECT directorio.id from directorio inner join carpeta on (carpeta.id=directorio.fk_id_dir_id) where directorio.fk_id_dir_id={x}")
        cursor.execute(sql5)
        iddir=cursor.fetchall()    
        #condicion de vista de directorio cuando exista el contador 
        if request.GET.get('contador') != None :###si el envio se ha realizado 
            listaenvio=(request.GET.get('contador')) 
            for i in iddir:
                idsbase=str(i)
                caracteres="(, )"
                for s in range (len(caracteres)):
                    idsbase=idsbase.replace(caracteres[s],"")    
                comparacion=(idsbase,idsbase == listaenvio)
                for e in comparacion:
                    if e == True:
                        idigualado=(request.GET.get('contador'))
                        print(idigualado)          
                        if (idigualado == request.GET.get('contador')): # si el envio es igual al id existente en la base de datos modelo directorio
                            sql7=(f"SELECT contadorvistasdirectorio.directorio_con from contadorvistasdirectorio where contadorvistasdirectorio.fk_id_con_id={x}   ")
                            cursor.execute(sql7)
                            contadorvisita=cursor.fetchall()
                            #eliminacion de parametros caracteres sobrantes 
                            contadorvistastring=str(contadorvisita)
                            caracteres="[(, )]"
                            for s in range (len(caracteres)):
                                contadorvistastring=contadorvistastring.replace(caracteres[s],"")    
                            #transformacion de string a entero
                            print(contadorvistastring)
                            contadorenvio=int(contadorvistastring)
                            valor=int(1)
                            contador=(contadorenvio+valor) #valor suma 1 cada vez que visualiza el archivo valor para usar en el update del sql de abajo
                            sql9=(f"SELECT carpeta.id from carpeta inner join contadorvistasdirectorio on (carpeta.id=contadorvistasdirectorio.fk_id_con_id) where contadorvistasdirectorio.fk_id_con_id={x}")
                            cursor.execute(sql9)
                            con=cursor.fetchall()
                            cambio=str(con)
                            caracteres="[(, )]"
                            for l in range (len(caracteres)):
                                cambio=cambio.replace(caracteres[l],"")    
                                #transformacion de string a int
                            convertido=int(cambio) ##valor del id de la carpeta para validar en el update del sql de abajo
                            #aumento de 1 a la descarga cada vez que realice la accion actualizacion del contador
                            sql8=(f"UPDATE contadorvistasdirectorio set directorio_con = {contador} where fk_id_con_id={convertido}")
                            cursor.execute(sql8)
                            ############seccion de envio para vista del pdf
                            selects=request.GET.get('contador') #id de la fila de la tabla seleccionada en directorio
                            if(request.GET.get('contador') == selects): #condicion si el id escogido es igual a la fila seleccionada
                                sql91=(f"SELECT archivo_dir from directorio where directorio.id= {selects} ")#obteniendo el archivo segun el id de la fila seleccionado
                                cursor.execute(sql91)
                                archivo=cursor.fetchall()
                                return render(request,'contadorvistadirectorios.html',{'archivos':archivo})
                            return redirect('publico:resolucionesdedirectorio', directorio_id=directorio_id)
            return redirect('publico:resolucionesdedirectorio', directorio_id=directorio_id)
        elif (request.GET.get('sincontador') != None): ###si la vista se ha hecho y el envio 
            listaenvio=(request.GET.get('sincontador')) #lista del contador de envio
            for i in iddir:
                idsbase=str(i)
                caracteres="(, )"
                for s in range (len(caracteres)):
                    idsbase=idsbase.replace(caracteres[s],"")    
                comparacion=(idsbase,idsbase == listaenvio)
                for e in comparacion:
                    if e == True:
                        idigualado=(request.GET.get('sincontador'))
                        if (idigualado == request.GET.get('sincontador')):#visualizacion del archivo correpondiente al boton seleccionado
                            sql94=(f"SELECT archivo_dir from directorio where directorio.id= {idigualado} ")#obteniendo el archivo segun el id de la fila seleccionado
                            cursor.execute(sql94)
                            archivo=cursor.fetchall()
                            return render(request,'contadorvistadirectorios.html',{'archivos':archivo})
        return render(request,self.template_name,{'inner':join,'anios':anio,'is':ir,'iddirs':iddir,'veras':verea})
    

class Contadorvistadirectorios(TemplateView):
    template_name = 'contadorvistadirectorios.html'
    def get(self, request,vista_id,*args,**kwargs):
        return render(request,self.template_name)
      
        
class Verasamblea(TemplateView):
    template_name = 'resolucionesdeasamblea.html'
    def get(self, request,asamblea_id,*args,**kwargs):        
        # captura de variable de id
        y=asamblea_id
        #sql de asamblea
        cursor=connection.cursor()
        sql15=(f"select *from asamblea where asamblea.fk_id_asa_id='{y}'")
        cursor.execute(sql15)
        join=cursor.fetchall()
        #fin sql de asamblea
        #sql de año que pertenece al asamblea 
        sql25=(f"select carpeta.nombre_car from carpeta inner join asamblea on (carpeta.id=asamblea.fk_id_asa_id) where asamblea.fk_id_asa_id='{y}'")
        cursor.execute(sql25)
        anio=cursor.fetchall()
        #fin sql de año que pertenece al asamblea
        #sql para obtener el año del modelo carpeta
        sql26=(f"select *from carpeta where carpeta.id='{y}'")
        cursor.execute(sql26)
        ir=cursor.fetchall()
        #fin sql para obtener el año del modelo carpeta
        #------obtener el contador segun la id del fk de asamblea que se obtiene al ingresar a la página-------
        sql10=(f"SELECT contadorvistasasamblea.asamblea_cont from contadorvistasasamblea where contadorvistasasamblea.fk_id_cont_id={y}   ")
        cursor.execute(sql10)
        verea=cursor.fetchall()
        #id asamblea
        sql4=(f"SELECT asamblea.id from asamblea inner join carpeta on (carpeta.id=asamblea.fk_id_asa_id) where asamblea.fk_id_asa_id={y}")
        cursor.execute(sql4)
        idasa=cursor.fetchall()
    
        if request.GET.get('contador') != None:
            listaenvio=(request.GET.get('contador')) 
            for i in idasa:
                idsbase=str(i)
                caracteres="(, )"
                for s in range (len(caracteres)):
                    idsbase=idsbase.replace(caracteres[s],"")    
                comparacion=(idsbase,idsbase == listaenvio)
                for e in comparacion:
                    if e == True:
                        idigualado=(request.GET.get('contador'))                        
                        if(idigualado == request.GET.get ('contador')):
                            sql7=(f"SELECT contadorvistasasamblea.asamblea_cont from contadorvistasasamblea where contadorvistasasamblea.fk_id_cont_id={y}   ")
                            cursor.execute(sql7)
                            countasa=cursor.fetchall()
                            
                            sumas=str(countasa)
                            caracteres="[(, )]"
                            for s in range (len(caracteres)):
                                sumas=sumas.replace(caracteres[s],"")    
                                #transformacion de caracter a string
                            contadorenvio=int(sumas)
                            
                            valor = 1
                            vista = (contadorenvio+valor)
                            
                            sql9=(f"SELECT carpeta.id from carpeta inner join contadorvistasasamblea on (carpeta.id=contadorvistasasamblea.fk_id_cont_id) where contadorvistasasamblea.fk_id_cont_id={y}")
                            cursor.execute(sql9)
                            con=cursor.fetchall()
                            #transformacion de lista a string
                            anio=str(con)

                            
                            caracteres="[(, )]"
                            for l in range (len(caracteres)):
                                anio=anio.replace(caracteres[l],"")    
                            #transformacion de string a entero
                            int_anio=int(anio) ##valor del id de la carpeta para validar en el update del sql de abajo

                            sql8=(f"UPDATE contadorvistasasamblea set asamblea_cont ={vista} where contadorvistasasamblea.fk_id_cont_id={int_anio}")
                            cursor.execute(sql8)

                            seleccion = request.GET.get('contador')

                            if request.GET.get('contador') == seleccion:
                                sql94=(f"SELECT archivo_asa from asamblea where asamblea.id= {idigualado} ")#obteniendo el archivo segun el id de la fila seleccionado
                                cursor.execute(sql94)
                                archivo=cursor.fetchall()
                                return render(request,'contadorvisitasasamblea.html',{'archivos':archivo})
                            return redirect('publico:resolucionesdeasamblea', asamblea_id=asamblea_id)
            return redirect('publico:resolucionesdeasamblea', asamblea_id=asamblea_id)


        elif(request.GET.get('sincontador') != None):
            listaenvio=(request.GET.get('sincontador'))
            for i in idasa:
                idsbase=str(i)
                caracteres="(, )"
                for s in range (len(caracteres)):
                    idsbase=idsbase.replace(caracteres[s],"")    
                comparacion=(idsbase,idsbase == listaenvio)
                for e in comparacion:
                    if e == True:
                        idigualado=(request.GET.get('sincontador'))
                        if (idigualado == request.GET.get('sincontador')):#visualizacion del archivo correpondiente al boton seleccionado
                            sql94=(f"SELECT archivo_asa from asamblea where asamblea.id= {idigualado} ")#obteniendo el archivo segun el id de la fila seleccionado
                            cursor.execute(sql94)
                            archivo=cursor.fetchall()
                            return render(request,'contadorvisitasasamblea.html',{'archivos':archivo})

        return render(request,self.template_name,{'inner':join, 'anios':anio,'is':ir,'idasam':idasa,'veras':verea})
        

class Contadorvistaasambleas(TemplateView):
    template_name = 'contadorvisitasasamblea.html'
    def get(self, request,vistaasamblea_id,*args,**kwargs):
        return render(request,self.template_name)


def nosotros(request):
    return render(request,'nosotros.html',{'navbar':'nosotros'})


def programas(request):
    queryset = request.GET.get("buscar")
    programa=Programa.objects.filter(estado_pro=True)
    if queryset:
        programa = Programa.objects.filter(
            Q(fechacreacion_pro__icontains = queryset) |
            Q(titulo_pro__icontains= queryset)
           
        ).distinct()#Funcion para que la consulta tome los valores con el conector logico O

    paginator = Paginator(programa,10) #Instanciamos la clase paginator en donde recibe la lista de objetos y el numero de elementos a mostrar por cada pagina 
    page = request.GET.get('page') or 1 #En la variable page guarda la pagina actual en la que nos encontramos navegando en el template 
    programa = paginator.get_page(page) #Redefinimos programa para enviarle al template aquellos elementos pertenecientes a la pagina que se esta solicitando 
    
    pagina_actual = int(page)
    pages = range(1, programa.paginator.num_pages + 1) 
    return render(request,'programas.html',{'programas':programa, "pages":pages, "pagina_actual":pagina_actual,'navbar':'programas'})

def detalleprograma(request, slug):
    programa = get_object_or_404(Programa, slug=slug)
    return render(request,'vistaprograma.html',{'detalleprograma':programa})
