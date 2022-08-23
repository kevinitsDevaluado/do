from ntpath import join

from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.usuario.mixins import SuperStaffMixin, ValidarPermisosRequeridosMixin
from django.urls import reverse_lazy
from apps.archivero.models import *
from apps.archivero.forms import *
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from django.db import connection
from django.contrib import messages
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
 
import cv2
import pytesseract
from pdf2image import convert_from_path
import os
import re
from distutils.dir_util import remove_tree

# Create your views here.
#////////////////////////////////////CRUD PARA  AÑOS ////////////////////////////////////////////////////////////
class Inicio_Anios(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,TemplateView):
    template_name = 'archivero/anios/listaranio.html'

# funcion para listar archivo y contenido de la seccion programa
class ListarAnios(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,ListView):
    model =  Anios
    def get_queryset(self):
        return self.model.objects.all()
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('archivero:inicio_anios')
    
    
# funcion para agregar archivo y contenido de la seccion programa
class CrearAnios(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,CreateView):
    model = Anios
    template_name = 'archivero/anios/agregaranio.html'
    form_class = AnioForm    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                nuevo_anio = Anios(
                    nombre_ani=form.cleaned_data.get('nombre_ani'),
                )
                nuevo_anio.save()
                mensaje = 'Registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = 'No se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('archivero:inicio_anios')

# funcion para editar archivo y contenido de la seccion programa
class EditarAnios(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,UpdateView):
    model = Anios
    template_name = 'archivero/anios/actualizaranio.html'
    form_class = AnioForm

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = 'Modificado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = 'No se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('archivero:inicio_anios')

# funcion para eliminar archivo y contenido de la seccion programa
class EliminarAnios(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,DeleteView):
    model = Anios
    template_name = 'archivero/anios/eliminaranio.html'
  
    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            anio = self.get_object()
            anio.delete()
            mensaje = 'Eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('archivero:inicio_anios')




#////////////////////////////////////CRUD PARA  TEMAS ////////////////////////////////////////////////////////////
class Inicio_Temas(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,TemplateView):
    template_name = 'archivero/temas/listartemas.html'

# funcion para listar archivo y contenido de la seccion programa
class ListarTemas(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,ListView):
    model =  Temas
    def get_queryset(self):
        return self.model.objects.all()
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('archivero:inicio_temas')
    
    
# funcion para agregar archivo y contenido de la seccion programa
class CrearTemas(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,CreateView):
    model = Temas
    template_name = 'archivero/temas/agregartemas.html'
    form_class = TemasForm   
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                nuevo_tema = Temas(
                    nombre_tem=form.cleaned_data.get('nombre_tem'),
                )
                nuevo_tema.save()
                mensaje = 'Registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = 'No se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('archivero:inicio_temas')

# funcion para editar archivo y contenido de la seccion programa
class EditarTemas(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,UpdateView):
    model = Temas
    template_name = 'archivero/temas/actualizartemas.html'
    form_class = TemasForm

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = 'Modificado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = 'No se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('archivero:inicio_temas')

# funcion para eliminar archivo y contenido de la seccion programa
class EliminarTemas(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,DeleteView):
    model = Temas
    template_name = 'archivero/temas/eliminartemas.html'
  
    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            temas = self.get_object()
            temas.delete()
            mensaje = 'Eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('archivero:inicio_temas')
   



#////////////////////////////////////CRUD PARA  ANO/TEMAS ////////////////////////////////////////////////////////////
class Inicio_Anios_Temas(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,TemplateView):
    template_name = 'archivero/aniostemas/listaraniotemas.html'

# funcion para listar archivo y contenido de la seccion programa
class ListarAniosTemas(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,ListView):
    model =  Anios_Temas
    def get_queryset(self):
        return self.model.objects.all()
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('archivero:inicio_anios_temas')
    
    
# funcion para agregar archivo y contenido de la seccion programa
class CrearAniosTemas(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,CreateView):
    
    template_name = 'archivero/aniostemas/agregaraniotemas.html'

    def get(self, request, *args, **kwargs):
    
    
    
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                nueva_relacion = Anios_Temas(
                    fk_id_ani=form.cleaned_data.get('fk_id_ani'),
                    fk_id_tem=form.cleaned_data.get('fk_id_tem'),
                )
                nueva_relacion.save()
                mensaje = 'Registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = 'No se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('archivero:inicio_anios_temas')



# funcion para editar archivo y contenido de la seccion programa
class EditarAniosTemas(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,UpdateView):
    model = Anios_Temas
    template_name = 'archivero/aniostemas/actualizaraniotemas.html'
    form_class = Anio_TemasForm

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = 'Modificado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = 'No se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('archivero:inicio_anios_temas')

# funcion para eliminar archivo y contenido de la seccion programa
class EliminarAniosTemas(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,DeleteView):
    model = Anios_Temas
    template_name = 'archivero/aniostemas/eliminaraniotemas.html'
  
    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            temas = self.get_object()
            temas.delete()
            mensaje = 'Eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('archivero:inicio_anios_temas')
   


#////////////////////////////////////CRUD PARA  DOCUMENTOS ////////////////////////////////////////////////////////////
class Inicio_Documentos(LoginRequiredMixin,TemplateView):
    template_name = 'archivero/documento/listardocumento.html'
    def get(self, request,*args,**kwargs):

        cursor = connection.cursor()#Linea para establecer la coneccion al Gestor
        sql = ("SELECT anio.nombre_ani, anio.id FROM anio") #Filtrado de consulta SQL
        cursor.execute(sql) #Lee el filtrado y realiza la lectura del SQL en Django
        inner = cursor.fetchall() #Asigna una variable para usar como un dicionario en la plantilla
        sql2 = ("SELECT temas.nombre_tem, temas.id, anio_tema.fk_id_tem_id, anio_tema.id, anio.id FROM anio inner join anio_tema on (anio.id=anio_tema.fk_id_ani_id) inner join  temas on (temas.id=anio_tema.fk_id_tem_id)") 
        cursor.execute(sql2) 
        inner2 = cursor.fetchall()
        sql3 = ("SELECT * FROM documento") 
        cursor.execute(sql3) 
        inner3 = cursor.fetchall()
 

        return render(request,self.template_name,{'join':inner,'join2':inner2,'join3':inner3})


# funcion para listar archivo y contenido de la seccion programa
class ListarDocumentos(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,ListView):
    model =  Documentos
    def get_queryset(self):
        
        return self.model.objects.all()
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('archivero:inicio_documentos')


    
    
    
# funcion para agregar archivo y contenido de la seccion programa
class CrearDocumentos(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,CreateView):
    model = Documentos
    template_name = 'archivero/documento/agregardocumento.html'
    form_class = DocumentosForm 
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES)
            if form.is_valid():
                
                form.save()
                mensaje = 'Registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                
                if form.save():
                    documento=Documentos.objects.all().last()
                    
                    if ((os.path.exists('pdfaimglecturadoc') == True ) ): #condicion si carpeta esta creada pdfaimglecturadoc creada
                        remove_tree("pdfaimglecturadoc") 
                        if (documento.contenido_doc == "True" ):
                            
                            archivoaleer=documento.documento_doc
                            archivoseleccionado=documento.id
                            doc=str(archivoaleer)
                            
                            images = convert_from_path(f"../asociacionutc/media/{doc}", 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
                            os.mkdir('pdfaimglecturadoc') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                            fotos="../asociacionutc/pdfaimglecturadoc/" #redireccion a la carpeta correspondiente
                            lista = []
                            for i, image in enumerate(images):
                                fname =fotos+'image'+str(i)+'.png' 
                                image.save(fname)
                                #transformacipn de imagenes a informacion en consola
                                pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'
                                imagen = cv2.imread(fname) #lee todos las imagenes creadas recientemente        
                                lectura = pytesseract.image_to_string(imagen,lang='spa')
                                textopdf=str(lectura)
                                caracteres=" '  "
                                for a in range (len(caracteres)):
                                    textopdf=textopdf.replace(caracteres[a],"")    
                                #transformacion de caracter a string
                                texto=str(textopdf)
                                text= re.escape(texto) #secuencia de escape permite añadir caracteres especiales al atributo de la base
                                lista.append(text) #aumento de contenido a la lectura segun las paginas del pdf
                                textop=str(lista) #transformacion a string
                                #quitando caracter 
                                caracteres=" '  " 
                                for a in range (len(caracteres)):
                                    textop=textop.replace(caracteres[a],"")    
                                #transformacion de caracter a string
                                textof=str(textop)
                                texttex= re.escape(textof) #permite escapar de lienas especiales (permite lectura en base  sin ningun error ) 
                                sql10=(f"UPDATE documento set contenido_doc = 'r{texttex}\' where documento.id={archivoseleccionado}")
                                cursor=connection.cursor()
                                cursor.execute(sql10)
                            
                            if (os.path.isdir('pdfaimglecturadoc/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                                remove_tree("pdfaimglecturadoc")  #eliminacion de carpeta (pdfaimglecturadoc) con imagenes creadas las que fueron usadas para la lectura 
                    
                    else: #condicion  carpeta no esta creada pdfaimglecturadoc creada 
                        if (documento.contenido_doc == "True" ):
                            archivoaleer=documento.documento_doc
                            archivoseleccionado=documento.id
                            doc=str(archivoaleer)
                            print(doc,documento.contenido_doc)
                            #transformacion de pdf a imagenes
                            images = convert_from_path(f"../asociacionutc/media/{doc}", 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
                            os.mkdir('pdfaimglecturadoc') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                            fotos="../asociacionutc/pdfaimglecturadoc/" #redireccion a la carpeta correspondiente
                            lista = []
                            for i, image in enumerate(images):
                                fname =fotos+'image'+str(i)+'.png' 
                                image.save(fname)
                                #transformacipn de imagenes a informacion en consola
                                pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'
                                imagen = cv2.imread(fname) #lee todos las imagenes creadas recientemente        
                                lectura = pytesseract.image_to_string(imagen,lang='spa')
                                textopdf=str(lectura)
                                caracteres=" '  "
                                for a in range (len(caracteres)):
                                    textopdf=textopdf.replace(caracteres[a],"")    
                                #transformacion de caracter a string
                                texto=str(textopdf)
                                text= re.escape(texto) #secuencia de escape permite añadir caracteres especiales al atributo de la base
                                lista.append(text) #aumento de contenido a la lectura segun las paginas del pdf
                                textop=str(lista) #transformacion a string
                                #quitando caracter 
                                caracteres=" '  " 
                                for a in range (len(caracteres)):
                                    textop=textop.replace(caracteres[a],"")    
                                #transformacion de caracter a string
                                textof=str(textop)
                                texttex= re.escape(textof) #permite escapar de lienas especiales (permite lectura en base  sin ningun error ) 
                                sql10=(f"UPDATE documento set contenido_doc = 'r{texttex}\' where documento.id={archivoseleccionado}")
                                cursor=connection.cursor()
                                cursor.execute(sql10)
                            if (os.path.isdir('pdfaimglecturadoc/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                                remove_tree("pdfaimglecturadoc")  #eliminacion de carpeta (pdfaimglecturadoc) con imagenes creadas las que fueron usadas para la lectura 
                return response
            else:
                mensaje = 'No se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('archivero:inicio_documentos')

# funcion para editar archivo y contenido de la seccion programa
class EditarDocumentos(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,UpdateView):
    model = Documentos
    template_name = 'archivero/documento/actualizardocumento.html'
    form_class = EditarDocumentosForm

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES,instance=self.get_object())
            Documentosmodelo=list(Documentos.objects.values_list('id','documento_doc'))    
            datosdocumentos=[]  #Asignacion de variable tipo lista 
            # metodo para quitar los caracteres especiales de la matriz aniotema
            for g in Documentosmodelo :  
                listado=str(g)
                caracteres=" '()"
                for a in range (len(caracteres)):
                    listado=listado.replace(caracteres[a],"")    
                    #transformacion de caracter a string
                    listadosz=str(listado)
                listados=str(listadosz)
                datosdocumentos.append(listados) #Seguir agregando a la lista 
                                
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} Modificado Correctamente!'
                error = 'No hay error '
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 201
                
                if(form.save()):
                    documentomodi=list(Documentos.objects.values_list('id','documento_doc'))    
                    datosdocumentosmodi=[]  #Asignacion de variable tipo lista 
                    # metodo para quitar los caracteres especiales de la matriz aniotema
                    for g in documentomodi :  
                        listado=str(g)
                        caracteres=" '()"
                        for a in range (len(caracteres)):
                            listado=listado.replace(caracteres[a],"")    
                            #transformacion de caracter a string
                            listadosz=str(listado)
                        listados=str(listadosz)
                        datosdocumentosmodi.append(listados) #Seguir agregando a la lista 
                    #obtener el archivo modificado
                    setA = set(datosdocumentosmodi)
                    datosdocumentosmodi = list(setA.difference(datosdocumentos))
                    
                    if not datosdocumentosmodi:
                        pass
                    else:
                        for modelo in datosdocumentosmodi:
                            idparacambio=(modelo[0])
                            #sql para validar si el archivo fue leido con anterioridad
                            cursor=connection.cursor()
                            sql9=(f"select contenido_doc from  documento where documento.id={idparacambio}")
                            cursor.execute(sql9)
                            contenidoactual=cursor.fetchall()
                            stringactual=str(contenidoactual)
                            caracteres="[( ,')]"
                            for x in range (len(caracteres)):
                                stringactual=stringactual.replace(caracteres[x],"")
                            if(stringactual != "False"):
                                #actualizacion de documento //sql para cambiar el contenido del mismo para que se haga una nueva lectura
                                sql10=(f"UPDATE documento set contenido_doc = 'Modificar' where documento.id={idparacambio}")
                                cursor.execute(sql10)
                return response
            else:
                mensaje = 'No se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('archivero:inicio_documentos')

# funcion para eliminar archivo y contenido de la seccion programa
class EliminarDocumentos(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,DeleteView):
    model = Documentos
    template_name = 'archivero/documento/eliminardocumento.html'
  
    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            documentos = self.get_object()
            documentos.delete()
            mensaje = 'Eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('archivero:inicio_documentos')
   





class VistaDocs(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,View):
    template_name = 'archivero/vistadocs/vistadocs.html'

    def get(self, request, *args, **kwargs):
        cursor = connection.cursor()#Linea para establecer la coneccion al Gestor
        sql = ("Select * From anio") #Filtrado de consulta SQL
        cursor.execute(sql) #Lee el filtrado y realiza la lectura del SQL en Django
        inner = cursor.fetchall() #Asigna una variable para usar como un dicionario en la plantilla
        sql2 = ("Select * From temas") #Filtrado de consulta SQL
        cursor.execute(sql2) #Lee el filtrado y realiza la lectura del SQL en Django
        inner2 = cursor.fetchall() #Asigna una variable para usar como un dicionario en la plantilla
        aniotema=list(Anios_Temas.objects.values_list('fk_id_ani_id','fk_id_tem_id'))    
        datosfkaniotema=[]  #Asignacion de variable tipo lista 

        # metodo para quitar los caracteres especiales de la matriz aniotema
        for g in aniotema :  
            listado=str(g)
            caracteres=" ',()"
            for a in range (len(caracteres)):
                listado=listado.replace(caracteres[a],"")    
                #transformacion de caracter a string
                listadosz=str(listado)
            listados=str(listadosz)
            
            datosfkaniotema.append(listados) #Seguir agregando a la lista 


        '''Condicion para la creacion de las relaciones  Anios temas de Seleccionj multiple 
                if (request.GET.get('enviar3') != None):#Condicion si el envio del tema se realiza continua a la siguiente condicion
                    if (request.GET.get('enviar4') == ""):#Si elaño no se realiza se pedira un mensaje correspondiente 
                     return   : Se redirigue al template para nuevamente seleccionar las opciones y kla URL quede limpia
                    elif  : Si el año ha sido seleccionado entonces se realizara la condicion 

                listaenviar3x=enviar3x.split(',') #Metodo usado como separador de cada elemento de un string 
            Caso contrario 1
                No se ha seleccionado nada
            Caso contrario 2 
                No se ha seleccionado el Tema           
        '''
        if (request.GET.get('enviar3') != None):
            if (request.GET.get('enviar4') == ""):
                messages.error(request,'No se ha seleccionado el año')
                return redirect('archivero:vista_documentos')

            elif(request.GET.get('enviar4') != None):
                envioanio = request.GET.get('enviar4')     #Envio del Año
                enviotema = request.GET.getlist('enviar3')  #Envio del Tema
                stringenviotema=str(enviotema)
                caracteres="[( ')]"
                for x in range (len(caracteres)):
                    stringenviotema=stringenviotema.replace(caracteres[x],"")
                listastringenviotema=stringenviotema.split(',') #Metodo usado como separador de cada elemento de un string
               
                #metodo para separar caracteres en posiciones
                for i in listastringenviotema: #matriz i
                    for j in envioanio: #matriz j 
                        data=j+i
                        #print('envio',data)
                        envio=[]
                        envio.append(data)
                        #print(type(envio),envio)
                        #print('iguales',set(datosfkaniotema) & set(envio))
                        comparacion=(set(datosfkaniotema) & set(envio))
                        print('compa',comparacion)
                        listacomparada=list(comparacion)
                        print(type(listacomparada),listacomparada)
                        

                    '''Condicion para validar de que la lista existe elementos repetidos o no existe elementos repetidos
                            sql2 = (f"do $$ begin i) Explica sobre la insercion de la tabla y el tema a la tabla muchos a muchos anio_temas
                            Para mayor seguridad esta validado en el SQL si existe o no existen los datos que puedan registrar 
                            cursor.execute(sql2) Lee el filtrado y realiza la lectura del SQL en Django  
                            cursor.execute(f"SELECT anio.nombre_ani, temas.nombre_tem FROM ) Nos muestra el año y el tema que se ha registrado 
                            anioytema=cursor.fetchone() = Lectura de la ejecucion del SQL y pernmite traer en consola la peticion 
                            
                            { caracteres="( ')"                           }
                            { for x in range (len(caracteres)):           }Eliminacion de caracteres de la peticion SQL   
                            {     ver=ver.replace(caracteres[x],"")       }
                            { vistaexitosa=str(ver)                                  }Transformacion String 

                            messages.add_message(request, messages.SUCCESS, f"Creado exitosamente  ({vistaexitosa}).")  Mensaje de confirmacion o error
                            
                        CASO CONTRARIO
                            solo se mostrara la carpeta y los temas que ya existen con su respectivo mensaje confirmativo
                    '''
                    if not listacomparada:
                        
                        sql2 = (f"do $$ begin if exists(select id from anio_tema where fk_id_ani_id = {j} and fk_id_tem_id={i}) then Raise Notice'id existen'; else Insert into anio_tema(fk_id_ani_id,fk_id_tem_id) values ({j},{i}); end if; end $$") 
                        cursor.execute(sql2)
                        cursor.execute(f"SELECT anio.nombre_ani, temas.nombre_tem FROM anio inner join anio_tema on (anio.id=anio_tema.fk_id_ani_id)inner join  temas on (temas.id=anio_tema.fk_id_tem_id)where anio.id={j} and temas.id={i}")
                        anioytema=cursor.fetchone()
                        ver=str(anioytema)
                        caracteres="( ')"
                        for x in range (len(caracteres)):
                            ver=ver.replace(caracteres[x],"")
                        vistaexitosa=str(ver)
                        messages.add_message(request, messages.SUCCESS, f"Creado exitosamente  ({vistaexitosa}).")
                        
                        
                    else:
                        cursor.execute(f"SELECT anio.nombre_ani, temas.nombre_tem  FROM anio inner join anio_tema on (anio.id=anio_tema.fk_id_ani_id)inner join  temas on (temas.id=anio_tema.fk_id_tem_id)where anio.id={j} and temas.id={i}")
                        anioytema=cursor.fetchone()
                        ver=str(anioytema)
                        print('si',listacomparada)
                        
                        caracteres="( ')"
                        for x in range (len(caracteres)):
                            ver=ver.replace(caracteres[x],"")
                        vistarepetida=str(ver)
                        
                        messages.add_message(request=request,level=messages.ERROR,message=f"Ya existe ({vistarepetida}).")
                       
                    
                return redirect('archivero:vista_documentos')

        elif(request.GET.get('enviar4')== ""):
            messages.error(request,'No se ha seleccionado el año y el tema')
            return redirect('archivero:vista_documentos')
        elif(request.GET.get('enviar4')!= None):
            messages.error(request,'Falta seleccionar el Tema')
            return redirect('archivero:vista_documentos')
            
        

        return render(request,self.template_name,{'join':inner,'join2':inner2})


class LecturaDocumentos(LoginRequiredMixin,SuperStaffMixin, ValidarPermisosRequeridosMixin,View):
    template_name = 'archivero/lectura/lectura.html'

    def get(self, request, *args, **kwargs):
        listardocumento=Documentos.objects.all().order_by('-id')
        archivoseleccionado=(request.GET.get('lectura')) #carga de pagina no hay envio resultado none
        if ((os.path.exists('pdfaimglecturadoc') == True ) ): #condicion si carpeta esta creada pdfaimglecturadoc creada
            remove_tree("pdfaimglecturadoc") 
            if (archivoseleccionado != None ): #si el envio es distinto de none realizar la condicion
                archivoseleccionado=(request.GET.get('lectura')) 
                #pdf _________________________________________________
                sql9=(f"SELECT documento_doc From documento where id={archivoseleccionado}")
                cursor=connection.cursor()
                cursor.execute(sql9)
                PDF_file=cursor.fetchall()
                #Quitando caracteres 
                pdf=str(PDF_file) #transformando a string 
                caracteres="[(, )]''"
                for s in range (len(caracteres)):
                    pdf=pdf.replace(caracteres[s],"")    
                        #transformacion de caracter a string
                doc=str(pdf)
                #transformacion de pdf a imagenes
                
                images = convert_from_path(f"../asociacionutc/media/{doc}", 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
                os.mkdir('pdfaimglecturadoc') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                fotos="../asociacionutc/pdfaimglecturadoc/" #redireccion a la carpeta correspondiente
                lista = []
                for i, image in enumerate(images):
                    fname =fotos+'image'+str(i)+'.png' 
                    image.save(fname)
                    #transformacipn de imagenes a informacion en consola
                    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'
                    imagen = cv2.imread(fname) #lee todos las imagenes creadas recientemente        
                    lectura = pytesseract.image_to_string(imagen,lang='spa')
                    textopdf=str(lectura)
                    caracteres=" '  "
                    for a in range (len(caracteres)):
                        textopdf=textopdf.replace(caracteres[a],"")    
                    #transformacion de caracter a string
                    texto=str(textopdf)
                    text= re.escape(texto) #secuencia de escape permite añadir caracteres especiales al atributo de la base
                    lista.append(text) #aumento de contenido a la lectura segun las paginas del pdf
                    textop=str(lista) #transformacion a string
                    #quitando caracter 
                    caracteres=" '  " 
                    for a in range (len(caracteres)):
                        textop=textop.replace(caracteres[a],"")    
                    #transformacion de caracter a string
                    textof=str(textop)
                    texttex= re.escape(textof) #permite escapar de lienas especiales (permite lectura en base  sin ningun error ) 
                    sql10=(f"UPDATE documento set contenido_doc = 'r{texttex}\' where documento.id={archivoseleccionado}")
                    cursor=connection.cursor()
                    cursor.execute(sql10)
                
                if (os.path.isdir('pdfaimglecturadoc/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                    remove_tree("pdfaimglecturadoc")  #eliminacion de carpeta (pdfaimglecturadoc) con imagenes creadas las que fueron usadas para la lectura 
                    return redirect('archivero:lectura_documentos') #redireccionamiento a la plantilla de listar sirve para que en la url no asome el valor del envio
        
        else: #condicion  carpeta no esta creada pdfaimglecturadoc creada 
            if (archivoseleccionado != None ): #si el envio es distinto de none realizar la condicion
                archivoseleccionado=(request.GET.get('lectura')) 
                print('la id es',archivoseleccionado) # envio del id del archivo seleccionado
                #pdf _________________________________________________
                sql9=(f"SELECT documento_doc From documento where id={archivoseleccionado}")
                cursor=connection.cursor()
                cursor.execute(sql9)
                PDF_file=cursor.fetchall()
                #Quitando caracteres 
                pdf=str(PDF_file) #transformando a string 
                caracteres="[(, )]''"
                for s in range (len(caracteres)):
                    pdf=pdf.replace(caracteres[s],"")    
                        #transformacion de caracter a string
                doc=str(pdf)
                #transformacion de pdf a imagenes
                images = convert_from_path(f"../asociacionutc/media/{doc}", 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
                os.mkdir('pdfaimglecturadoc') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                fotos="../asociacionutc/pdfaimglecturadoc/" #redireccion a la carpeta correspondiente
                lista = []
                for i, image in enumerate(images):
                    fname =fotos+'image'+str(i)+'.png' 
                    image.save(fname)
                    #transformacipn de imagenes a informacion en consola
                    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'
                    imagen = cv2.imread(fname) #lee todos las imagenes creadas recientemente        
                    lectura = pytesseract.image_to_string(imagen,lang='spa')
                    textopdf=str(lectura)
                    caracteres=" '  "
                    for a in range (len(caracteres)):
                        textopdf=textopdf.replace(caracteres[a],"")    
                    #transformacion de caracter a string
                    texto=str(textopdf)
                    text= re.escape(texto) #secuencia de escape permite añadir caracteres especiales al atributo de la base
                    lista.append(text) #aumento de contenido a la lectura segun las paginas del pdf
                    textop=str(lista) #transformacion a string
                    #quitando caracter 
                    caracteres=" '  " 
                    for a in range (len(caracteres)):
                        textop=textop.replace(caracteres[a],"")    
                    #transformacion de caracter a string
                    textof=str(textop)
                    texttex= re.escape(textof) #permite escapar de lienas especiales (permite lectura en base  sin ningun error ) 
                    sql10=(f"UPDATE documento set contenido_doc = 'r{texttex}\' where documento.id={archivoseleccionado}")
                    cursor=connection.cursor()
                    cursor.execute(sql10)
                if (os.path.isdir('pdfaimglecturadoc/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                    remove_tree("pdfaimglecturadoc")  #eliminacion de carpeta (pdfaimglecturadoc) con imagenes creadas las que fueron usadas para la lectura 
                    return redirect('archivero:lectura_documentos') #redireccionamiento a la plantilla de listar sirve para que en la url no asome el valor del envio
        
        return render(request,self.template_name,{'listardocumentos':listardocumento})


 



class ReporteDocumentos(LoginRequiredMixin, View):
    
    def link_callback(self,uri, rel):
            
        sUrl = settings.STATIC_URL     
        
        sRoot = settings.STATIC_ROOT   
        mUrl = settings.MEDIA_URL       
        mRoot = settings.MEDIA_ROOT     

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  

        # condicion si el archivo existe
        if not os.path.isfile(path):
                raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path
                        
        
    def get(self, request,reporte_documento,*args,**kwargs):
        try:
            template = get_template('dashboard/reportes/reportedocumento.html')
            
            id_doc_rep=reporte_documento
            cursor=connection.cursor()
            sql=(f"select *from documento inner join anio_tema on (anio_tema.id=documento.fk_id_atem_id) where anio_tema.fk_id_ani_id= {id_doc_rep}")
            cursor.execute(sql)
            documento=cursor.fetchall()
            
            sql2=(f"select anio.nombre_ani from anio where anio.id = {id_doc_rep}")
            cursor.execute(sql2)
            anionombre=cursor.fetchall()
            anio=str(anionombre)               
            caracteres="[(, )]"
            for l in range (len(caracteres)):
                anio=anio.replace(caracteres[l],"")
           
            
            context = {
                'titulo': f' Reporte de Documentos del archivero {anio}',
                'documentos':documento,

                'icon': '{}{}'.format(settings.STATIC_URL,'./assets/images/sello_white.png')
            }
            
            
            html = template.render(context)
            
            response=   HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reporte_documentos_archivero.pdf"'
            
            pisaStatus = pisa.CreatePDF(
                html, dest=response,link_callback=self.link_callback
            )

            
            return response
            #return HttpResponse('hola mundo')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('archivero:inicio_documentos'))
        

