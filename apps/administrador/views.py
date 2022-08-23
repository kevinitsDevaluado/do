
from distutils.dir_util import remove_tree
import json
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize

# Create your views here.
from apps.administrador.models import *
from apps.administrador.forms import *
from django.db import connection
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView,View

from apps.usuario.mixins import SuperStaffMixin, ValidarPermisosRequeridosMixin

 # ===============================Panel adminitracion (CRUD) para el administrador==============================================================================================
#Pagina Principal Dashboard
class Paneladministracion(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/paneladministracion.html'
    def get(self, request,*args,**kwargs):
        #contadoooor
        Archivo.objects.all()
        Directorio.objects.all()
        #contador para los archivos de transparencia
        cursor=connection.cursor() #conector
        sql1=(f"select count(archivo.archivo_arch) FROM archivo")
        cursor.execute(sql1)
        contadortransparencia=cursor.fetchall()
        #fin contrador archivos de transparencia
        #contador para los archivos de directorio
        sql2=(f"select count(directorio.archivo_dir) FROM directorio")
        cursor.execute(sql2)
        contadordirectorio=cursor.fetchall()
        #fin contrador archivos de directorio
        #contador para los archivos de asamblea
        sql3=(f"select count (asamblea.archivo_asa) from asamblea")
        cursor.execute(sql3)
        contadorasamblea=cursor.fetchall()
        #fin contrador archivos de asamblea 
        #contador para los archivos de galeria
        sql4=(f"select count(imagen_gal) from galeria")
        cursor.execute(sql4)
        contadorgaleria=cursor.fetchall()
        #fin contrador archivos de galeria 
        #contador para los archivos de programa
        sql5=(f"select count(imagen_pro) from programa")
        cursor.execute(sql5)
        contadorprograma=cursor.fetchall()
        #fin contrador archivos de galeria          
        #eliminarcion de ciertos caracteres de una cadena (transparencia)
        totaltransparenciastring=str(contadortransparencia)
        caracteres="[(,)]"
        for x in range (len(caracteres)):
            totaltransparenciastring=totaltransparenciastring.replace(caracteres[x],"")
        #eliminarcion de ciertos caracteres de una cadena (asamblea)
        totalasambleastring=str(contadorasamblea)
        caracteres="[(,)]"
        for x in range (len(caracteres)):
            totalasambleastring=totalasambleastring.replace(caracteres[x],"")
        #eliminarcion de ciertos caracteres de una cadena (directorio)
        totaldirectoriostring=str(contadordirectorio)
        caracteres="[(,)]"
        for x in range (len(caracteres)):
            totaldirectoriostring=totaldirectoriostring.replace(caracteres[x],"")          
        # transformacion de caracter a string
        xa=str(totaltransparenciastring)
        xb=str(totalasambleastring)
        xc=str(totaldirectoriostring)
        # transformacion de string a entero
        xac=int(xa)
        xbc=int(xb)
        xcc=int(xc)
        contadortotal=int(xac+xbc+xcc) #contador total de archivos de todo el sistema

        #sql para visualizar la suma total de vistas del archivo de todos los años de la seccion directorio en la pagina de administracion 
        sql7=(f"select sum(directorio_con) from contadorvistasdirectorio")
        cursor.execute(sql7)
        contadord=cursor.fetchall()
        contadordirectorios=str(contadord)
        caracteress="[(, )]"
        for t in range (len(caracteress)):
            contadordirectorios=contadordirectorios.replace(caracteress[t],"")    
        #sql para visualizar la suma total de vistas del archivo de todos los años de la seccion directorio en la pagina de administracion 
        sql8=(f"select sum(asamblea_cont) from contadorvistasasamblea")
        cursor.execute(sql8)
        contador=cursor.fetchall()
        contadorasambleas=str(contador)
        caracteres="[(, )]"
        for u in range (len(caracteres)):
            contadorasambleas=contadorasambleas.replace(caracteres[u],"")
        #sql  para consultar el contador total de vista directorio y asamblea
        
        sql9=(f"SELECT SUM(T.Cantidad) FROM (select sum(asamblea_cont) as Cantidad from contadorvistasasamblea UNION ALL select sum(directorio_con)as Cantidad from contadorvistasdirectorio) T")
        cursor.execute(sql9)
        contadorvistas=cursor.fetchall()
        contadortotalvistas=str(contadorvistas)
        caracteres="[(Decimal(''),)]"
        for u in range (len(caracteres)):
            contadortotalvistas=contadortotalvistas.replace(caracteres[u],"")
        print(type(contadortotalvistas),contadortotalvistas)
        return render(request,self.template_name,{
            'contadores1':contadortransparencia,
            'contadores2':contadordirectorio,
            'contadores3':contadorasamblea,
            'contadorestotales':contadortotal,
            'contadores4':contadorgaleria,
            'contadores5':contadorprograma,
            'num1':xac,
            'num2':xbc,
            'num3':xcc,
            'contadores6':contadordirectorios,
            'contadores7':contadorasambleas,
            'contadores8':contadortotalvistas,
            'navbar':'Paneladministracion'
        })






    
#_____________///////////////////////////____________CRUD PARA AÑOS__________________////////////////////////////////////____________-   
#Clase para listar las carpetas de años de la seccion Transparencia
class InicioTransparencia(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/anios/listartranspariencia.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,{'navbar':'InicioTransparencia'})
    
class ListarTransparencia(LoginRequiredMixin,ListView):
    model =  Carpeta
    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('administrador:inicio_transparencia')

# Clase para agregar las carpetas de años de la seccion Transparenciade la seccion Transparencia
class CrearTransparencia(LoginRequiredMixin,CreateView):
    model = Carpeta
    template_name = 'dashboard/anios/creartransparencia.html'
    form_class = CarpetaForm       
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                nuevo_anio = Carpeta(
                    nombre_car=form.cleaned_data.get('nombre_car'),
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
            return redirect('administrador:inicio_transparencia')

# Clase para editar las carpetas de años de la seccion Transparencia
class ActualizarTransparencia(LoginRequiredMixin,UpdateView):
    model = Carpeta
    template_name = 'dashboard/anios/actualizartransparencia.html'
    form_class = CarpetaForm
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
            return redirect('administrador:inicio_transparencia')

# Clase para eliminar las carpetas de años de la seccion Transparencia
class EliminarTransparencia(LoginRequiredMixin,DeleteView):
    model = Carpeta
    template_name = 'dashboard/anios/eliminartransparencia.html'
    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            mestra = self.get_object()
            mestra.delete()
            mensaje = 'Eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('administrador:inicio_transparencia')



#_____________///////////////////////////____________CRUD PARA MESES TRANSPARENCIA__________________////////////////////////////////////____________-

#Clase para renderizar el tamplate de inicio de MES Carpeta para las peticiones AJAX
class InicioMesTransparencia(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/mesestransparencia/listarmestransparencia.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{'navbar':'InicioMesTransparencia'})

#Clase para listar las carpetas de meses de la seccion Transparencia
class ListarMesTransparencia(LoginRequiredMixin,ListView):
    model =  Subcarpeta
    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('administrador:inicio_mes_transparencia')
    
# Clase para agregar las carpetas de meses a la seccion transparencia
class CrearMesTransparencia(LoginRequiredMixin,CreateView):
    model = Subcarpeta
    template_name = 'dashboard/mesestransparencia/crearmestransparencia.html'
    form_class = SubcarpetaForm     
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                nueva_mes = Subcarpeta(
                    nombre_sub=form.cleaned_data.get('nombre_sub'),
                )
                nueva_mes.save()
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
            return redirect('administrador:inicio_mes_transparencia')

# Clase para editar las carpetas de meses la seccion Transparencia
class EditarMesTransparencia(LoginRequiredMixin,UpdateView):
    model = Subcarpeta
    template_name = 'dashboard/mesestransparencia/editarmestransparencia.html'
    form_class = SubcarpetaForm
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
            return redirect('administrador:inicio_mes_transparencia')

# Clase para eliminar las carpetas de meses de la seccion Transparencias
class EliminarMesTransparencia(LoginRequiredMixin,DeleteView):
    model = Subcarpeta
    template_name = 'dashboard/mesestransparencia/eliminarmestransparencia.html'
    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            mestra = self.get_object()
            mestra.delete()
            mensaje = 'Eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('administrador:inicio_mes_transparencia')


#_____________///////////////////////////____________CRUD PARA RELACION DE AÑO MES__________________////////////////////////////////////____________-

class InicioAnioMesTransparencia(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/relacionaniomes/listaraniomestransparencia.html'

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{'navbar':'InicioAnioMesTransparencia'})

#funcion para listar las carpetas de años y meses de la seccion Transparencia
class ListarAnioMesTransparencia(LoginRequiredMixin,ListView):
    model =  Carpeta_Subcarpeta
    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('administrador:inicio_anio_mes_transparencia')

# funcion para agregar las carpetas de archivos a la seccion resoluciones
class CrearAnioMesTransparencia(LoginRequiredMixin,CreateView):
    model: Carpeta_Subcarpeta
    form_class = Carpeta_SubcarpetaForm
    template_name = 'dashboard/relacionaniomes/crearaniomestransparencia.html'
    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                nueva_relacion = Carpeta_Subcarpeta(
                    fk_id_car=form.cleaned_data.get('fk_id_car'),
                    fk_id_sub=form.cleaned_data.get('fk_id_sub'),
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
            return redirect('administrador:inicio_anio_mes_transparencia')
    
# funcion para editar las carpetas de aniomes la seccion resoluciones
class EditarAnioMesTransparencia(LoginRequiredMixin,UpdateView):
    model = Carpeta_Subcarpeta
    form_class =Carpeta_SubcarpetaForm
    template_name = 'dashboard/relacionaniomes/editaraniomestransparencia.html'
    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
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
            return redirect('administrador:inicio_anio_mes_transparencia')

# funcion para eliminar las carpetas de aniomes de la seccion resoluciones
class EliminarAnioMesTransparencia(LoginRequiredMixin,DeleteView):
    model = Carpeta_Subcarpeta
    template_name = 'dashboard/relacionaniomes/eliminaraniomestransparencia.html'
    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            aniomestra = self.get_object()
            aniomestra.delete()
            mensaje = 'Eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('administrador:inicio_anio_mes_transparencia')


#/////////////////////////////////////CRUD PARA ARCHIVOS DE TRANSPARENCIA///////////////////////////////////////////////////////////

class InicioArchivosTransparencia(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/archivostransparencia/listararchivostransparencia.html'
    def get(self, request, *args, **kwargs):
        
        cursor=connection.cursor()
        #sql para consultar el modelo carpeta(año)
        sql=(f"select *from carpeta ")
        cursor.execute(sql)
        carpeta=cursor.fetchall() 
        #sql para consultar el modelo transparencia 
        sql=(f"select *from archivo ")
        cursor.execute(sql)
        transparencia=cursor.fetchall()   
        return render(request,self.template_name,{'navbar':'InicioArchivosTransparencia','transparencias':transparencia,'carpetas':carpeta})

        

#funcion para listar las carpetas de meses de la seccion Transparencia
class ListarArchivosTransparencia(LoginRequiredMixin,ListView):
    model =  Archivo

    def get_queryset(self):
        
        
        return self.model.objects.all()
    
    def get(self, request, *args, **kwargs  ):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(), use_natural_foreign_keys=True),'application/json')
        else:
            return  redirect('administrador:inicio_archivos_transparencia')

# funcion para agregar las carpetas de archivos a la seccion resoluciones
class CrearArchivosTransparencia(LoginRequiredMixin,CreateView):
    model = Archivo
    template_name = 'dashboard/archivostransparencia/creararchivostransparencia.html'
    form_class = ArchivoForm   

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES)
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                
                
                if(form.save()):
                    archivo=Archivo.objects.all().last()
                    if ((os.path.exists('pdfaimglecturaarch') == True ) ): #condicion si carpeta esta creada pdfaimglecturaarch creada
                        remove_tree("pdfaimglecturaarch") 
                        if (archivo.contenido_arch == "True" ):
                            
                            archivoaleer=archivo.archivo_arch
                            archivoseleccionado=archivo.id
                            doc=str(archivoaleer)
                            
                            images = convert_from_path(f"../asociacionutc/media/{doc}", 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
                            os.mkdir('pdfaimglecturaarch') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                            fotos="../asociacionutc/pdfaimglecturaarch/" #redireccion a la carpeta correspondiente
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
                                sql10=(f"UPDATE archivo set contenido_arch = 'r{texttex}\' where archivo.id={archivoseleccionado}")
                                cursor=connection.cursor()
                                cursor.execute(sql10)
                            
                            if (os.path.isdir('pdfaimglecturaarch/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                                remove_tree("pdfaimglecturaarch")  #eliminacion de carpeta (pdfaimglecturaarch) con imagenes creadas las que fueron usadas para la lectura 
                    
                    else: #condicion  carpeta no esta creada pdfaimglecturaarch creada 
                        if (archivo.contenido_arch == "True" ):
                            archivoaleer=archivo.archivo_arch
                            archivoseleccionado=archivo.id
                            doc=str(archivoaleer)
                            print(doc,archivo.contenido_arch)
                            #transformacion de pdf a imagenes
                            images = convert_from_path(f"../asociacionutc/media/{doc}", 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
                            os.mkdir('pdfaimglecturaarch') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                            fotos="../asociacionutc/pdfaimglecturaarch/" #redireccion a la carpeta correspondiente
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
                                sql10=(f"UPDATE archivo set contenido_arch = 'r{texttex}\' where archivo.id={archivoseleccionado}")
                                cursor=connection.cursor()
                                cursor.execute(sql10)
                            if (os.path.isdir('pdfaimglecturaarch/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                                remove_tree("pdfaimglecturaarch")  #eliminacion de carpeta (pdfaimglecturaarch) con imagenes creadas las que fueron usadas para la lectura 
                
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        return redirect('administrador:inicio_archivos_transparencia')
     
# funcion para editar las carpetas de archivos la seccion resoluciones
class EditarArchivosTransparencia(LoginRequiredMixin,UpdateView):
    model = Archivo
    template_name = 'dashboard/archivostransparencia/editararchivostransparencia.html'
    form_class = ActualizarArchivoForm
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES,instance=self.get_object())
            Archivomodelo=list(Archivo.objects.values_list('id','archivo_arch'))    
            datosarchivo=[]  #Asignacion de variable tipo lista 
            # metodo para quitar los caracteres especiales de la matriz aniotema
            for g in Archivomodelo :  
                listado=str(g)
                caracteres=" '()"
                for a in range (len(caracteres)):
                    listado=listado.replace(caracteres[a],"")    
                    #transformacion de caracter a string
                    listadosz=str(listado)
                listados=str(listadosz)
                datosarchivo.append(listados) #Seguir agregando a la lista 
                                
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} Modificado Correctamente!'
                error = 'No hay error '
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 201
                
                if(form.save()):
                    Archivoomodi=list(Archivo.objects.values_list('id','archivo_arch'))    
                    datosarchivomodi=[]  #Asignacion de variable tipo lista 
                    # metodo para quitar los caracteres especiales de la matriz aniotema
                    for g in Archivoomodi :  
                        listado=str(g)
                        caracteres=" '()"
                        for a in range (len(caracteres)):
                            listado=listado.replace(caracteres[a],"")    
                            #transformacion de caracter a string
                            listadosz=str(listado)
                        listados=str(listadosz)
                        datosarchivomodi.append(listados) #Seguir agregando a la lista 
                    #obtener el archivo modificado
                    setA = set(datosarchivomodi)
                    datosarchivomodi = list(setA.difference(datosarchivo))
                    if not datosarchivomodi:
                        print("no lectura")
                    else:
                        for modelo in datosarchivomodi:
                            idparacambio=(modelo[0])
                             #sql para validar si el archivo fue leido con anterioridad
                            cursor=connection.cursor()
                            sql9=(f"select contenido_arch from  archivo where archivo.id={idparacambio}")
                            cursor.execute(sql9)
                            contenidoactual=cursor.fetchall()
                            stringactual=str(contenidoactual)
                            caracteres="[( ,')]"
                            for x in range (len(caracteres)):
                                stringactual=stringactual.replace(caracteres[x],"")
                            if(stringactual != "False"):
                                #actualizacion de documento //sql para cambiar el contenido del mismo para que se haga una nueva lectura
                                sql10=(f"UPDATE archivo set contenido_arch = 'Modificar' where archivo.id={idparacambio}")
                                cursor.execute(sql10)
                return response
            
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('administrador:inicio_archivos_transparencia')

# funcion para eliminar las carpetas de archivos de la seccion resoluciones
class EliminarArchivoTransparencia(LoginRequiredMixin,DeleteView):
    model = Archivo
    template_name = 'dashboard/archivostransparencia/eliminararchivotransparencia.html'
    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            archivotra = self.get_object()
            archivotra.delete()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('administrador:inicio_archivos_transparencia')

#/////////////////////////////////////FIN DEL CRUD PARA ARCHIVOS DE TRANSPARENCIA///////////////////////////////////////////////////////////

    

#_________________________CRUD PARA DIRECTORIO_________________________________--

class InicioDirectorio(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/directorio/listardirectorio.html'
  

    def get(self, request,*args, **kwargs):
        cursor=connection.cursor()
        #sql para consultar el modelo carpeta(año)
        sql=(f"select *from carpeta ")
        cursor.execute(sql)
        carpeta=cursor.fetchall() 
        #sql para consultar el modelo directorio   
        sql=(f"select *from directorio ")
        cursor.execute(sql)
        directorio=cursor.fetchall()   
        return render(request,self.template_name,{'navbar':'InicioDirectorio','directorios':directorio,'carpetas':carpeta})
    

class  ListarDirectorio(LoginRequiredMixin,ListView):
    model =  Directorio
    
    
    
    def get(self, request, *args, **kwargs  ):
        
        
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(), use_natural_foreign_keys=True),'application/json')
        else:
            return  redirect('administrador:inicio_directorio')

class CrearDirectorio(LoginRequiredMixin,CreateView):
    model = Directorio
    form_class = ResolucionesdedirectorioForm  
    template_name = 'dashboard/directorio/agregardirectorio.html'
    
    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES)
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                
                if form.save():
                    directorio=Directorio.objects.all().last()
                    if ((os.path.exists('pdfaimgdirectorio') == True ) ): #condicion si carpeta esta creada pdfaimgdirectorio creada
                        remove_tree("pdfaimgdirectorio")  
                        if (directorio.contenido_dir == "True" ):
                            archivoaleer=directorio.archivo_dir
                            archivoseleccionado=directorio.id
                            doc=str(archivoaleer)
                            #transformacion de pdf a imagenes
                            images = convert_from_path(f"../asociacionutc/media/{doc}", 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
                            os.mkdir('pdfaimgdirectorio') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                            fotos="../asociacionutc/pdfaimgdirectorio/" #redireccion a la carpeta correspondiente
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
                                sql10=(f"UPDATE directorio set contenido_dir = 'r{texttex}\' where directorio.id={archivoseleccionado}")
                                cursor=connection.cursor()
                                cursor.execute(sql10)
                            if (os.path.isdir('pdfaimgdirectorio/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                                remove_tree("pdfaimgdirectorio")  #eliminacion de carpeta (pdfaimgdirectorio) con imagenes creadas las que fueron usadas para la lectura 
                    else: #condicion  carpeta no esta creada pdfaimgdirectorio creada 
                          if (directorio.contenido_dir == "True" ):
                                archivoaleer=directorio.archivo_dir
                                archivoseleccionado=directorio.id
                                doc=str(archivoaleer)
                                #transformacion de pdf a imagenes
                                images = convert_from_path(f"../asociacionutc/media/{doc}", 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
                                os.mkdir('pdfaimgdirectorio') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                                fotos="../asociacionutc/pdfaimgdirectorio/" #redireccion a la carpeta correspondiente
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
                                    sql10=(f"UPDATE directorio set contenido_dir = 'r{texttex}\' where directorio.id={archivoseleccionado}")
                                    cursor=connection.cursor()
                                    cursor.execute(sql10)
                                if (os.path.isdir('pdfaimgdirectorio/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                                    remove_tree("pdfaimgdirectorio")  #eliminacion de carpeta (pdfaimgdirectorio) con imagenes creadas las que fueron usadas para la lectura                         
                return response
            
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        return redirect('administrador:inicio_directorio')

class EditarDirectorio(LoginRequiredMixin,UpdateView):
    model = Directorio
    template_name = 'dashboard/directorio/editardirectorio.html'
    form_class = EditarResolucionesdedirectorioForm
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES,instance=self.get_object())
            Directoriomodelo=list(Directorio.objects.values_list('id','archivo_dir'))    
            datosdirectorio=[]  #Asignacion de variable tipo lista 
            # metodo para quitar los caracteres especiales de la matriz aniotema
            for g in Directoriomodelo :  
                listado=str(g)
                caracteres=" '()"
                for a in range (len(caracteres)):
                    listado=listado.replace(caracteres[a],"")    
                    #transformacion de caracter a string
                    listadosz=str(listado)
                listados=str(listadosz)
                datosdirectorio.append(listados) #Seguir agregando a la lista 
                                
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} Modificado Correctamente!'
                error = 'No hay error '
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 201
                
                if(form.save()):
                    Directoriomodi=list(Directorio.objects.values_list('id','archivo_dir'))    
                    datosdirectoriomodi=[]  #Asignacion de variable tipo lista 
                    # metodo para quitar los caracteres especiales de la matriz aniotema
                    for g in Directoriomodi :  
                        listado=str(g)
                        caracteres=" '()"
                        for a in range (len(caracteres)):
                            listado=listado.replace(caracteres[a],"")    
                            #transformacion de caracter a string
                            listadosz=str(listado)
                        listados=str(listadosz)
                        datosdirectoriomodi.append(listados) #Seguir agregando a la lista 
                    #obtener el archivo modificado
                    setA = set(datosdirectoriomodi)
                    datosdirectoriomodi = list(setA.difference(datosdirectorio))
                    
                    if not datosdirectoriomodi:
                        print("no lectura")
                    else:
                        for modelo in datosdirectoriomodi:
                            idparacambio=(modelo[0])
                            #sql para validar si el archivo fue leido con anterioridad
                            cursor=connection.cursor()
                            sql9=(f"select contenido_dir from directorio where directorio.id={idparacambio}")
                            cursor.execute(sql9)
                            contenidoactual=cursor.fetchall()
                            stringactual=str(contenidoactual)
                            caracteres="[( ,')]"
                            for x in range (len(caracteres)):
                                stringactual=stringactual.replace(caracteres[x],"")
                            if(stringactual != "False"):
                                #actualizacion de documento //sql para cambiar el contenido del mismo para que se haga una nueva lectura
                                sql10=(f"UPDATE directorio set contenido_dir = 'Modificar' where directorio.id={idparacambio}")
                                cursor.execute(sql10)
                       
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('administrador:inicio_directorio')

class EliminarDirectorio(LoginRequiredMixin,DeleteView):
    model = Directorio
    template_name = 'dashboard/directorio/eliminardirectorio.html'
    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            asamblea = self.get_object()
            asamblea.delete()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('administrador:inicio_directorio')



#///////////////////////CRUD  PARA ASAMBLEA///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class InicioAsamblea(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/asamblea/listarasamblea.html'
    def get(self, request, *args, **kwargs):
        cursor=connection.cursor()
        sql=(f"select *from carpeta ")
        cursor.execute(sql)
        carpeta=cursor.fetchall() 
           
        sql=(f"select *from asamblea ")
        cursor.execute(sql)
        asamblea=cursor.fetchall()  
        
        
        return render(request,self.template_name,{'navbar':'InicioAsamblea','asambleas':asamblea,'carpetas':carpeta})

#funcion para listar las resoluciones de asamblea
class  ListarAsamblea(LoginRequiredMixin,ListView):
    model =  Asamblea
    def get_queryset(self):
        return self.model.objects.all()
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True),'application/json')#Retornar esa informacionen una aplicacion Json 
        else:
            return redirect('administrador:inicio_asamblea')
  
# funcion para agregar archivos a las resoluciones de asamblea
class CrearAsamblea(LoginRequiredMixin,CreateView):
    model = Asamblea
    form_class = AsambleaForm
    template_name = 'dashboard/asamblea/agregarasamblea.html'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES)
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                
                if form.save():
                    asamblea=Asamblea.objects.all().last()
                    if ((os.path.exists('pdfaimgasamblea') == True ) ): #condicion si carpeta esta creada pdfaimgasamblea creada
                        remove_tree("pdfaimgasamblea") 
                        if (asamblea.contenido_asa == "True" ):
                            archivoaleer=asamblea.archivo_asa
                            archivoseleccionado=asamblea.id
                            doc=str(archivoaleer)
                            #transformacion de pdf a imagenes
                            images = convert_from_path(f"../asociacionutc/media/{doc}", 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
                            os.mkdir('pdfaimgasamblea') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                            fotos="../asociacionutc/pdfaimgasamblea/" #redireccion a la carpeta correspondiente
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
                                sql10=(f"UPDATE asamblea set contenido_asa = 'r{texttex}\' where asamblea.id={archivoseleccionado}")
                                cursor=connection.cursor()
                                cursor.execute(sql10)
                            if (os.path.isdir('pdfaimgasamblea/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                                remove_tree("pdfaimgasamblea")  #eliminacion de carpeta (pdfaimgasamblea) con imagenes creadas las que fueron usadas para la lectura 
                    else: #condicion  carpeta no esta creada pdfaimgasamblea creada 
                        if (asamblea.contenido_asa == "True" ):
                            archivoaleer=asamblea.archivo_asa
                            archivoseleccionado=asamblea.id
                            doc=str(archivoaleer)
                            #transformacion de pdf a imagenes
                            images = convert_from_path(f"../asociacionutc/media/{doc}", 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
                            os.mkdir('pdfaimgasamblea') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                            fotos="../asociacionutc/pdfaimgasamblea/" #redireccion a la carpeta correspondiente
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
                                sql10=(f"UPDATE asamblea set contenido_asa = 'r{texttex}\' where asamblea.id={archivoseleccionado}")
                                cursor=connection.cursor()
                                cursor.execute(sql10)
                            if (os.path.isdir('pdfaimgasamblea/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                                remove_tree("pdfaimgasamblea")  #eliminacion de carpeta (pdfaimgasamblea) con imagenes creadas las que fueron usadas para la lectura 
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        return redirect('administrador:inicio_asamblea')
      
# funcion para editar los archivos de las resoluciones de asamblea
class EditarAsamblea(LoginRequiredMixin,UpdateView):
    model = Asamblea
    form_class = EditarAsambleaForm
    template_name = 'dashboard/asamblea/editarasamblea.html'
    
    
    def post(self,request, *args, **kwargs):
          
        if request.is_ajax():  
            form = self.form_class(data=request.POST, files = request.FILES,instance=self.get_object()) 
            Asambleamodelo=list(Asamblea.objects.values_list('id','archivo_asa'))    
            datosasamblea=[]  #Asignacion de variable tipo lista 
            # metodo para quitar los caracteres especiales de la matriz aniotema
            for g in Asambleamodelo :  
                listado=str(g)
                caracteres=" '()"
                for a in range (len(caracteres)):
                    listado=listado.replace(caracteres[a],"")    
                    #transformacion de caracter a string
                    listadosz=str(listado)
                listados=str(listadosz)
                datosasamblea.append(listados) #Seguir agregando a la lista 
                                
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} Modificado Correctamente!'
                error = 'No hay error '
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 201
                
                if(form.save()):
                    Asambleamodi=list(Asamblea.objects.values_list('id','archivo_asa'))    
                    datosasambleamodi=[]  #Asignacion de variable tipo lista 
                    # metodo para quitar los caracteres especiales de la matriz aniotema
                    for g in Asambleamodi :  
                        listado=str(g)
                        caracteres=" '()"
                        for a in range (len(caracteres)):
                            listado=listado.replace(caracteres[a],"")    
                            #transformacion de caracter a string
                            listadosz=str(listado)
                        listados=str(listadosz)
                        datosasambleamodi.append(listados) #Seguir agregando a la lista 
                    #obtener el archivo modificado
                    setA = set(datosasambleamodi)
                    datosasambleamodi = list(setA.difference(datosasamblea))
                    
                    if not datosasambleamodi:
                        print("no lectura")
                    else:
                        for modelo in datosasambleamodi:
                            idparacambio=(modelo[0])
                             #sql para validar si el archivo fue leido con anterioridad
                            cursor=connection.cursor()
                            sql9=(f"select contenido_asa from  asamblea where asamblea.id={idparacambio}")
                            cursor.execute(sql9)
                            contenidoactual=cursor.fetchall()
                            stringactual=str(contenidoactual)
                            caracteres="[( ,')]"
                            for x in range (len(caracteres)):
                                stringactual=stringactual.replace(caracteres[x],"")
                            if(stringactual != "False"):
                                #actualizacion de documento //sql para cambiar el contenido del mismo para que se haga una nueva lectura
                                sql10=(f"UPDATE asamblea set contenido_asa = 'Modificar' where asamblea.id={idparacambio}")
                                cursor.execute(sql10)
                            
                            
                            
                        
                return response
                
            else:
                mensaje = 'No se ha podido Registrar el usuario!'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('administrador:inicio_asamblea')
   
# funcion para eliminar los archivos del asamblea
class EliminarAsamblea(LoginRequiredMixin,DeleteView):
    model = Asamblea
    template_name = 'dashboard/asamblea/eliminarasamblea.html'

    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            asamblea = self.get_object()
            asamblea.delete()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('administrador:inicio_asamblea')

#//////////////////////////CRUD PARA GALERIA//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


class InicioGaleria(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/galeria/listargaleria.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{'navbar':'InicioGaleria'})
    
# funcion para redireccionamiento de Galeria
class ListarGaleria(LoginRequiredMixin,ListView):
    model =  Galeria

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')

    '''Funcion para retornar dicinario de datos de tipo JSON'''
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json',self.get_queryset()),'application/json')#Retornar esa informacionen una aplicacion Json 
        else:
            return redirect('administrador:inicio_galeria')

# funcion para agregar las carpetas de archivos a la seccion resoluciones
class CrearGaleria(LoginRequiredMixin,CreateView):
    model = Galeria
    form_class = Galeriaform
    template_name = 'dashboard/galeria/agregargaleria.html'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES)
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        return redirect('administrador:inicio_galeria')
     
# funcion para editar las carpetas de archivos la seccion resoluciones
class EditarGaleria(LoginRequiredMixin,UpdateView):
    model = Galeria
    form_class = Galeriaform
    template_name = 'dashboard/galeria/editargaleria.html'
    def post(self,request, *args, **kwargs):
        if request.is_ajax():  
            form = self.form_class(data=request.POST, files = request.FILES,instance=self.get_object()) 
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} Registrado Correctamente!'
                error = 'No hay error '
                response = JsonResponse({'mensaje':mensaje,'error':error})
                response.status_code = 201
                return response
            else:
                mensaje = 'No se ha podido Registrar el usuario!'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('administrador:inicio_galeria')

# funcion para eliminar las carpetas de archivos de la seccion resoluciones
class EliminarGaleria(LoginRequiredMixin,DeleteView):
    model = Galeria
    template_name = 'dashboard/galeria/eliminargaleria.html'
    def delete(self, request,pk, *args, **kwargs):
        if request.is_ajax():
            galeria = self.get_object()
            galeria.estado_gal = False
            galeria.save()
            mensaje = f'{self.model.__name__} Eliminado Correctamente!'
            error = 'No hay error '
            response = JsonResponse({'mensaje':mensaje,'error':error})
            response.status_code = 201
            return response
        else:
            return redirect('administrador:inicio_galeria')



#////////////////////////////////////CRUD PARA  PROGRAMA ////////////////////////////////////////////////////////////

# funcion para listar archivo y contenido de la seccion programa
class ListarPrograma(LoginRequiredMixin,ListView):
    model =  Programa
    template_name = 'dashboard/programa/listarprograma.html'
    context_object_name = 'programas'
    queryset = Programa.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['navbar'] = 'ListarPrograma' 
        return context


    
# funcion para agregar archivo y contenido de la seccion programa
class CrearPrograma(LoginRequiredMixin,CreateView):
    model = Programa
    template_name = 'dashboard/programa/agregarprograma.html'
    form_class = Programaform
    success_url = reverse_lazy('administrador:listarprograma')
   
# funcion para editar archivo y contenido de la seccion programa
class EditarPrograma(LoginRequiredMixin,UpdateView):
    model = Programa
    template_name = 'dashboard/programa/editarprograma.html'
    form_class = Programaform
    success_url = reverse_lazy('administrador:listarprograma')

# funcion para eliminar archivo y contenido de la seccion programa
class EliminarPrograma(LoginRequiredMixin,DeleteView):
    model = Programa
    template_name = 'dashboard/programa/eliminarprograma.html'
    context_object_name = 'programas'
    def post(self,request,pk,*args,**kwargs):
        programas = Programa.objects.get(id=pk)
        programas.estado_pro=False
        programas.save()
        return redirect('administrador:listarprograma') 
  


#//////////////////////////CRUD PARA  CONTADOR DE VISTA DE RESOLUCIONES DE DIRECTORIO  ///////////////////
# Clase para listar contador de vista de directorio
class Iniciocontadorvistadirectorio(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,TemplateView):
    template_name = 'dashboard/contadores/directorio/listarcontadorvistadirectorio.html'
    
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{'navbar':'Iniciocontadorvistadirectorio'})

class Listarcontadorvistadirectorio(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,ListView):  
    model =  Contadorvistasdirectorio
    def get_queryset(self):
        return self.model.objects.filter(estado_con=True)
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True),'application/json')#Retornar esa informacionen una aplicacion Json 
        else:
            return redirect('administrador:inicio_contador_vista_directorio')
  
# Clase para crear contador de vista de directorio
class Crearcontadorvistadirectorio(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,CreateView):
    model = Contadorvistasdirectorio
    template_name = 'dashboard/contadores/directorio/crearcontadorvistadirectorio.html'
    form_class = ContadorvistasdirectorioForm    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
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
            return redirect('administrador:inicio_contador_vista_directorio')

# Clase para eliminar contador de vista de directorio
class Eliminarcontadorvistadirectorio(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,DeleteView):
    model = Contadorvistasdirectorio
    template_name = 'dashboard/contadores/directorio/eliminarcontadorvistadirectorio.html'
    
    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            contador = self.get_object()
            contador.estado_con=False
            contador.save()
            mensaje = 'Eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('administrador:inicio_contador_vista_directorio')




#//////////////////////////CRUD PARA  CONTADOR DE VISTA DE RESOLUCIONES DE ASAMBLEA  ///////////////////
# Clase para listar contador de vista de asamblea

class Iniciocontadorvistaasamblea(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,TemplateView):
    template_name = 'dashboard/contadores/asamblea/listarcontadorvistaasamblea.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{'navbar':'Iniciocontadorvistaasamblea'})

class Listarcontadorvistaasamblea(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,ListView):  
    model =  Contadorvistasasamblea
    def get_queryset(self):
            return self.model.objects.filter(estado_cont=True)
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset(),use_natural_foreign_keys = True),'application/json')#Retornar esa informacionen una aplicacion Json 
        else:
            return redirect('administrador:inicio_contador_vista_asamblea')
# Clase para crear contador de vista de asamblea
class Crearcontadorvistaasamblea(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,CreateView):
    model = Contadorvistasasamblea
    template_name = 'dashboard/contadores/asamblea/crearcontadorvistaasamblea.html'
    form_class = ContadorvistasasambleaForm    
    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
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
            return redirect('administrador:inicio_contador_vista_asamblea')

# Clase para eliminar contador de vista de asamblea
class Eliminarcontadorvistaasamblea(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,DeleteView):
    model = Contadorvistasasamblea
    template_name = 'dashboard/contadores/asamblea/eliminarcontadorvistaasamblea.html'
    
    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            contador = self.get_object()
            contador.estado_cont=False
            contador.save()
            mensaje = 'Eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('administrador:inicio_contador_vista_asamblea')



import pytesseract
from pdf2image import convert_from_path
import os, cv2
import re
#lectura de pdf (reconocimiento optico de caracteres) para archivos directorio
class Iniciolecturadirectorio(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,TemplateView):
    template_name = 'dashboard/lecturas/lecturadirectorio/lecturadirectorio.html'
    def get(self, request,*args,**kwargs):
        listardirectorio=Directorio.objects.all().order_by('-id')
        archivoseleccionado=(request.GET.get('lectura')) #carga de pagina no hay envio resultado none
        if ((os.path.exists('pdfaimgdirectorio') == True ) ): #condicion si carpeta esta creada pdfaimgdirectorio creada
            remove_tree("pdfaimgdirectorio") 
            if (archivoseleccionado != None ): #si el envio es distinto de none realizar la condicion
                archivoseleccionado=(request.GET.get('lectura')) 
                #pdf _________________________________________________
                sql9=(f"SELECT archivo_dir From directorio where id={archivoseleccionado}")
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
                os.mkdir('pdfaimgdirectorio') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                fotos="../asociacionutc/pdfaimgdirectorio/" #redireccion a la carpeta correspondiente
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
                    sql10=(f"UPDATE directorio set contenido_dir = 'r{texttex}\' where directorio.id={archivoseleccionado}")
                    cursor=connection.cursor()
                    cursor.execute(sql10)
                
                if (os.path.isdir('pdfaimgdirectorio/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                    remove_tree("pdfaimgdirectorio")  #eliminacion de carpeta (pdfaimgdirectorio) con imagenes creadas las que fueron usadas para la lectura 
                    return redirect('administrador:Inicio_lectura_directorio') #redireccionamiento a la plantilla de listar sirve para que en la url no asome el valor del envio
        
        else: #condicion  carpeta no esta creada pdfaimgdirectorio creada 
            if (archivoseleccionado != None ): #si el envio es distinto de none realizar la condicion
                archivoseleccionado=(request.GET.get('lectura')) 
                #pdf _________________________________________________
                sql9=(f"SELECT archivo_dir From directorio where id={archivoseleccionado}")
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
                os.mkdir('pdfaimgdirectorio') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                fotos="../asociacionutc/pdfaimgdirectorio/" #redireccion a la carpeta correspondiente
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
                    sql10=(f"UPDATE directorio set contenido_dir = 'r{texttex}\' where directorio.id={archivoseleccionado}")
                    cursor=connection.cursor()
                    cursor.execute(sql10)
                if (os.path.isdir('pdfaimgdirectorio/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                    remove_tree("pdfaimgdirectorio")  #eliminacion de carpeta (pdfaimgdirectorio) con imagenes creadas las que fueron usadas para la lectura 
                    return redirect('administrador:Inicio_lectura_directorio') #redireccionamiento a la plantilla de listar sirve para que en la url no asome el valor del envio
        return render(request,self.template_name,{'listardirectorios':listardirectorio,'navbar':'Iniciolecturadirectorio'})
    


#lectura de pdf (reconocimiento optico de caracteres) para archivos asambleea
class Iniciolecturaasamblea(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,TemplateView):
    template_name = 'dashboard/lecturas/lecturaasamblea/lecturaasamblea.html'
    def get(self, request,*args,**kwargs):
        listarasamblea=Asamblea.objects.all().order_by('-id')
        
       
        archivoseleccionado=(request.GET.get('lectura')) #carga de pagina no hay envio resultado none
        if ((os.path.exists('pdfaimgasamblea') == True ) ): #condicion si carpeta esta creada pdfaimgasamblea creada
            remove_tree("pdfaimgasamblea") 
            if (archivoseleccionado != None ): #si el envio es distinto de none realizar la condicion
                archivoseleccionado=(request.GET.get('lectura')) 
                print('la id es',archivoseleccionado) # envio del id del archivo seleccionado
                #pdf _________________________________________________
                sql9=(f"SELECT archivo_asa From asamblea where id={archivoseleccionado}")
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
                os.mkdir('pdfaimgasamblea') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                fotos="../asociacionutc/pdfaimgasamblea/" #redireccion a la carpeta correspondiente
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
                    sql10=(f"UPDATE asamblea set contenido_asa = 'r{texttex}\' where asamblea.id={archivoseleccionado}")
                    cursor=connection.cursor()
                    cursor.execute(sql10)
                if (os.path.isdir('pdfaimgasamblea/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                    remove_tree("pdfaimgasamblea")  #eliminacion de carpeta (pdfaimgasamblea) con imagenes creadas las que fueron usadas para la lectura 
                    return redirect('administrador:Inicio_lectura_asamblea') #redireccionamiento a la plantilla de listar sirve para que en la url no asome el valor del envio
        else: #condicion  carpeta no esta creada pdfaimgasamblea creada 
            if (archivoseleccionado != None ): #si el envio es distinto de none realizar la condicion
                archivoseleccionado=(request.GET.get('lectura')) 
                print('la id es',archivoseleccionado) # envio del id del archivo seleccionado
                #pdf _________________________________________________
                sql9=(f"SELECT archivo_asa From asamblea where id={archivoseleccionado}")
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
                os.mkdir('pdfaimgasamblea') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                fotos="../asociacionutc/pdfaimgasamblea/" #redireccion a la carpeta correspondiente
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
                    sql10=(f"UPDATE asamblea set contenido_asa = 'r{texttex}\' where asamblea.id={archivoseleccionado}")
                    cursor=connection.cursor()
                    cursor.execute(sql10)
                if (os.path.isdir('pdfaimgasamblea/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                    remove_tree("pdfaimgasamblea")  #eliminacion de carpeta (pdfaimgasamblea) con imagenes creadas las que fueron usadas para la lectura 
                    return redirect('administrador:Inicio_lectura_asamblea') #redireccionamiento a la plantilla de listar sirve para que en la url no asome el valor del envio
        return render(request,self.template_name,{'listarasambleas':listarasamblea,'navbar':'Iniciolecturaasamblea'})
    
    
    
class Iniciolecturatransparencia(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin,TemplateView):
    template_name = 'dashboard/lecturas/lecturatransparencia/lecturatransparencia.html'
    def get(self, request,*args,**kwargs):
        listartransparencia=Archivo.objects.all().order_by('-id')
        archivoseleccionado=(request.GET.get('lectura')) #carga de pagina no hay envio resultado none
        print(archivoseleccionado)
        
        
        
        if ((os.path.exists('pdfaimglecturaarch') == True ) ): #condicion si carpeta esta creada pdfaimglecturaarch creada
            remove_tree("pdfaimglecturaarch") 
            if (archivoseleccionado != None ): #si el envio es distinto de none realizar la condicion
                archivoseleccionado=(request.GET.get('lectura')) 
                #pdf _________________________________________________
                sql9=(f"SELECT archivo_arch From archivo where id={archivoseleccionado}")
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
                os.mkdir('pdfaimglecturaarch') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                fotos="../asociacionutc/pdfaimglecturaarch/" #redireccion a la carpeta correspondiente
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
                    sql10=(f"UPDATE archivo set contenido_arch = 'r{texttex}\' where archivo.id={archivoseleccionado}")
                    cursor=connection.cursor()
                    cursor.execute(sql10)
                
                if (os.path.isdir('pdfaimglecturaarch/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                    remove_tree("pdfaimglecturaarch")  #eliminacion de carpeta (pdfaimglecturaarch) con imagenes creadas las que fueron usadas para la lectura 
                    return redirect('administrador:Inicio_lectura_transparencia') #redireccionamiento a la plantilla de listar sirve para que en la url no asome el valor del envio
        
        else: #condicion  carpeta no esta creada pdfaimglecturaarch creada 
            if (archivoseleccionado != None ): #si el envio es distinto de none realizar la condicion
                archivoseleccionado=(request.GET.get('lectura')) 
                #pdf _________________________________________________
                sql9=(f"SELECT archivo_arch From archivo where id={archivoseleccionado}")
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
                os.mkdir('pdfaimglecturaarch') #nombre de carpeta donde van almacenarce las imagenes de cada pdf
                fotos="../asociacionutc/pdfaimglecturaarch/" #redireccion a la carpeta correspondiente
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
                    sql10=(f"UPDATE archivo set contenido_arch = 'r{texttex}\' where archivo.id={archivoseleccionado}")
                    cursor=connection.cursor()
                    cursor.execute(sql10)
                if (os.path.isdir('pdfaimglecturaarch/')): #verifica que la carpeta este creada y luego de la lectura se elimine automaticamente
                    remove_tree("pdfaimglecturaarch")  #eliminacion de carpeta (pdfaimglecturaarch) con imagenes creadas las que fueron usadas para la lectura 
                    return redirect('administrador:Inicio_lectura_transparencia') #redireccionamiento a la plantilla de listar sirve para que en la url no asome el valor del envio
        
        
        
        return render(request,self.template_name,{'listartransparencias':listartransparencia,'navbar':'Iniciolecturatransparencia'})
       
    
    
    
    
    
    
    
    

import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa



        
class Reportedirectorio(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin, View):
        
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
                        
        
    def get(self, request,  reporte_directorio,*args,**kwargs):
        try:
            template = get_template('dashboard/reportes/reportedirectorio.html')
            id_dir_rep=reporte_directorio
            cursor=connection.cursor()
            sql=(f"select *from directorio where directorio.fk_id_dir_id = {id_dir_rep}")
            cursor.execute(sql)
            directorio=cursor.fetchall()
            
            sql2=(f"select carpeta.nombre_car from carpeta where carpeta.id = {id_dir_rep}")
            cursor.execute(sql2)
            anionombre=cursor.fetchall()
            anio=str(anionombre)               
            caracteres="[(, )]"
            for l in range (len(caracteres)):
                anio=anio.replace(caracteres[l],"")
            
            context = {
                'titulo': f' Reporte de Archivos de Directorio {anio}',
                'directorios':directorio,
                'icon': '{}{}'.format(settings.STATIC_URL,'./assets/images/sello_white.png')
            }
            
            
            html = template.render(context)
            
            response=   HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reporte_directorio.pdf"'
            
            
            pisaStatus = pisa.CreatePDF(
                html, dest=response,link_callback=self.link_callback
                )
            
            return response
            #return HttpResponse('hola mundo')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('administrador:inicio_directorio'))
               
        
class Reporteasamblea(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin, View):
    
    
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
                        
        
    def get(self, request,reporte_asamblea,*args,**kwargs):
        try:
            template = get_template('dashboard/reportes/reporteasamblea.html')
            id_asa_rep=reporte_asamblea
            cursor=connection.cursor()
            sql=(f"select *from asamblea where asamblea.fk_id_asa_id = {id_asa_rep}")
            cursor.execute(sql)
            asamblea=cursor.fetchall()
            
            sql2=(f"select carpeta.nombre_car from carpeta where carpeta.id = {id_asa_rep}")
            cursor.execute(sql2)
            anionombre=cursor.fetchall()
            anio=str(anionombre)               
            caracteres="[(, )]"
            for l in range (len(caracteres)):
                anio=anio.replace(caracteres[l],"")
            
            context = {
                'titulo': f' Reporte de Archivos de Asamblea {anio}',
                'asambleas':asamblea,
                'icon': '{}{}'.format(settings.STATIC_URL,'./assets/images/sello_white.png')
            }
            
            
            html = template.render(context)
            
            response=   HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reporte_asamblea.pdf"'
            
            
            pisaStatus = pisa.CreatePDF(
                html, dest=response,link_callback=self.link_callback
                )
          
            return response
            #return HttpResponse('hola mundo')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('inicio_asamblea'))


class ReporteArchivosTransparencia(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin, View):
    
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
                        
        
    def get(self, request,reporte_transparencia,*args,**kwargs):
        try:
            template = get_template('dashboard/reportes/archivostrasnparencia.html')
            
            id_tran_rep=reporte_transparencia
            cursor=connection.cursor()
            sql=(f"select *from archivo inner join carpeta_subcarpeta on (carpeta_subcarpeta.id=archivo.fk_id_carsub_id) where carpeta_subcarpeta.fk_id_car_id= {id_tran_rep}")
            cursor.execute(sql)
            archivo=cursor.fetchall()
            
            sql2=(f"select carpeta.nombre_car from carpeta where carpeta.id = {id_tran_rep}")
            cursor.execute(sql2)
            anionombre=cursor.fetchall()
            anio=str(anionombre)               
            caracteres="[(, )]"
            for l in range (len(caracteres)):
                anio=anio.replace(caracteres[l],"")
            
           
            context = {
                'titulo': f' Reporte de Archivos de Transparencia {anio}',
                'archivos':archivo,
                'icon': '{}{}'.format(settings.STATIC_URL,'./assets/images/sello_white.png')
            }
            
            
            html = template.render(context)
            
            response=   HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reporte_transparencia.pdf"'
            
            
            pisaStatus = pisa.CreatePDF(
                html, dest=response,link_callback=self.link_callback
                )

            return response
            #return HttpResponse('hola mundo')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('inicio_archivos_transparencia'))


class ReporteProgramas(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin, View):
    
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
                        
        
    def get(self, request,*args,**kwargs):
        try:
            template = get_template('dashboard/reportes/reporteprograma.html')
            programa=Programa.objects.all()
            
            context = {
                'titulo': ' Reporte de Programa',
                'programas':programa,
                'icon': '{}{}'.format(settings.STATIC_URL,'./assets/images/sello_white.png')
            }
            
            
            html = template.render(context)
            
            response=   HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reporte_programa.pdf"'
            
            
            pisaStatus = pisa.CreatePDF(
                html, dest=response,link_callback=self.link_callback
                )

            return response
            #return HttpResponse('hola mundo')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('administrador:listarprograma'))


class ReporteGaleria(LoginRequiredMixin,SuperStaffMixin,ValidarPermisosRequeridosMixin, View):
    
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
                        
        
    def get(self, request,*args,**kwargs):
        try:
            template = get_template('dashboard/reportes/reportegaleria.html')
            galeria=Galeria.objects.all()
            
            context = {
                'titulo': ' Reporte de Galeria',
                'galerias':galeria,
                'icon': '{}{}'.format(settings.STATIC_URL,'./assets/images/sello_white.png')
            }
            
            
            html = template.render(context)
            
            response=   HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reporte_galeria.pdf"'
            
            
            pisaStatus = pisa.CreatePDF(
                html, dest=response,link_callback=self.link_callback
                )
           
            return response
            #return HttpResponse('hola mundo')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('administrador:inicio_galeria'))




#_____________///////////////////////////____________CRUD PARA INSTITUCIÓN__________________////////////////////////////////////____________-   

class InicioInstitucion(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/interfaz/institucion.html'
    def get(self, request, *args, **kwargs):
        institucion=Institucion.objects.all()
   
        gal=list(institucion)
        texto=str(gal)
        caracteres=" []  "
        for a in range (len(caracteres)):
            texto=texto.replace(caracteres[a],"")

          
        #transformacion de caracter a string
        return render(request, self.template_name,{'textos':texto,'navbar':'InicioInstitucion'})	
    

    
class ListarInstitucion(LoginRequiredMixin,ListView):
    model =  Institucion
    
    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        print(self.model.objects.count())
        if request.is_ajax():
            
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('administrador:inicio_institucion')

# Clase para crear contador de vista de directorio
class CrearInstitucion(LoginRequiredMixin,CreateView):
    model = Institucion
    template_name = 'dashboard/interfaz/crearinstitucion.html'
    form_class = InstitucionForm  
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data = request.POST,files = request.FILES)
            if form.is_valid():
                form.save()
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
            return redirect('administrador:inicio_institucion')

# Clase para editar las carpetas de años de la seccion Transparencia
class ActualizarInstitucion(LoginRequiredMixin,UpdateView):
    model = Institucion
    template_name = 'dashboard/interfaz/actualizarinstitucion.html'
    form_class = InstitucionForm
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(data=request.POST, files = request.FILES,instance=self.get_object())
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
            return redirect('administrador:inicio_institucion')


#_____________///////////////////////////____________CRUD PARA Preguntas Frecuentes__________________////////////////////////////////////____________-   
#Clase para listar las preguntas frecuentes
class InicioPreguntas(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/interfaz/preguntas/listarpreguntas.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,{'navbar':'InicioPreguntas'})
    
class ListarPreguntas(LoginRequiredMixin,ListView):
    model =  Preguntas

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('administrador:inicio_preguntas')

# Clase para agregar las carpetas de años de la seccion Transparenciade la seccion Transparencia
class CrearPreguntas(LoginRequiredMixin,CreateView):
    model = Preguntas
    template_name = 'dashboard/interfaz/preguntas/agregarpreguntas.html'
    form_class = PreguntasForm
           
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                nueva_pregunta = Preguntas(
                    pregunta=form.cleaned_data.get('pregunta'),
                    respuesta=form.cleaned_data.get('respuesta'),

                )
                nueva_pregunta.save()
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
            return redirect('administrador:inicio_preguntas')

# Clase para editar las carpetas de años de la seccion Transparencia
class ActualizarPreguntas(LoginRequiredMixin,UpdateView):
    model = Preguntas
    template_name = 'dashboard/interfaz/preguntas/actualizarpreguntas.html'
    form_class = PreguntasForm
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
            return redirect('administrador:inicio_preguntas')

# Clase para eliminar las carpetas de años de la seccion Transparencia
class EliminarPreguntas(LoginRequiredMixin,DeleteView):
    model = Preguntas
    template_name = 'dashboard/interfaz/preguntas/eliminarpreguntas.html'
    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            pregunta = self.get_object()
            pregunta.delete()
            mensaje = 'Eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('administrador:inicio_preguntas')



