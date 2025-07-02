import requests
import json
from django.core.management.base import BaseCommand
from django.db import transaction
from production.models import Departamento, Provincia, Distrito


class Command(BaseCommand):
    help = 'Carga datos de ubigeos del Peru desde API externa'
   
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpiar datos existentes antes de cargar',
        )
   
    def handle(self, *args, **options):
        self.stdout.write('Iniciando carga de ubigeos del Peru...')
       
        try:
            with transaction.atomic():
                if options['clear']:
                    self.limpiar_datos()
               
                self.cargar_departamentos()
                self.cargar_provincias()
                self.cargar_distritos()
                self.mostrar_resumen()
               
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error durante la carga: {str(e)}')
            )
            raise
   
    def limpiar_datos(self):
        self.stdout.write('Limpiando datos existentes...')
        Distrito.objects.all().delete()
        Provincia.objects.all().delete()
        Departamento.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Datos limpiados'))
   
    def descargar_archivo(self, url):
        self.stdout.write(f'Descargando desde {url}...')
       
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f'Error descargando: {str(e)}')
   
    def cargar_departamentos(self):
        self.stdout.write('Cargando departamentos...')
       
        url = 'https://raw.githubusercontent.com/joseluisq/ubigeos-peru/master/json/departamentos.json'
        data = self.descargar_archivo(url)
       
        departamentos = []
       
        for item in data:
            departamentos.append(Departamento(
                id=int(item['id_ubigeo']),
                nombre=item['nombre_ubigeo'].upper(),
                codigo=item['codigo_ubigeo']
            ))
       
        Departamento.objects.bulk_create(departamentos, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'{len(departamentos)} departamentos cargados'))
   
    def cargar_provincias(self):
        self.stdout.write('Cargando provincias...')
       
        url = 'https://raw.githubusercontent.com/joseluisq/ubigeos-peru/master/json/provincias.json'
        data = self.descargar_archivo(url)
       
        provincias = []
       
        # data es un dict donde cada key es un departamento_id y el value es lista de provincias
        for departamento_id, lista_provincias in data.items():
            try:
                # Buscar el departamento por id_ubigeo
                departamento = Departamento.objects.get(id=int(departamento_id))
               
                for provincia_data in lista_provincias:
                    provincias.append(Provincia(
                        id=int(provincia_data['id_ubigeo']),
                        nombre=provincia_data['nombre_ubigeo'].upper(),
                        codigo=provincia_data['codigo_ubigeo'],
                        departamento=departamento
                    ))
                   
            except Departamento.DoesNotExist:
                self.stdout.write(f'Departamento no encontrado para id: {departamento_id}')
                continue
            except Exception as e:
                self.stdout.write(f'Error procesando departamento {departamento_id}: {str(e)}')
                continue
       
        # Insertar en lotes
        batch_size = 100
        for i in range(0, len(provincias), batch_size):
            batch = provincias[i:i + batch_size]
            Provincia.objects.bulk_create(batch, ignore_conflicts=True)
       
        self.stdout.write(self.style.SUCCESS(f'{len(provincias)} provincias cargadas'))
   
    def cargar_distritos(self):
        self.stdout.write('Cargando distritos...')
       
        url = 'https://raw.githubusercontent.com/joseluisq/ubigeos-peru/master/json/distritos.json'
        data = self.descargar_archivo(url)
       
        distritos = []
        errores = 0
       
        # data es un dict donde cada key es una provincia_id y el value es lista de distritos
        for provincia_id, lista_distritos in data.items():
            try:
                # Buscar la provincia por id_ubigeo
                provincia = Provincia.objects.get(id=int(provincia_id))
               
                for distrito_data in lista_distritos:
                    distritos.append(Distrito(
                        id=int(distrito_data['id_ubigeo']),
                        nombre=distrito_data['nombre_ubigeo'].upper(),
                        codigo=distrito_data['codigo_ubigeo'],
                        provincia=provincia
                    ))
                   
            except Provincia.DoesNotExist:
                errores += 1
                if errores <= 10:
                    self.stdout.write(f'Provincia no encontrada para id: {provincia_id}')
                continue
            except Exception as e:
                errores += 1
                if errores <= 10:
                    self.stdout.write(f'Error procesando provincia {provincia_id}: {str(e)}')
                continue
       
        if errores > 10:
            self.stdout.write(f'Y {errores - 10} errores más...')
       
        # Insertar en lotes
        batch_size = 200
        for i in range(0, len(distritos), batch_size):
            batch = distritos[i:i + batch_size]
            Distrito.objects.bulk_create(batch, ignore_conflicts=True)
            self.stdout.write(f'Procesados {min(i + batch_size, len(distritos))}/{len(distritos)} distritos')
       
        self.stdout.write(self.style.SUCCESS(f'{len(distritos)} distritos cargados'))
   
    def mostrar_resumen(self):
        self.stdout.write('Carga completada exitosamente!')
        dept_count = Departamento.objects.count()
        prov_count = Provincia.objects.count()
        dist_count = Distrito.objects.count()
       
        self.stdout.write(f'Resumen: {dept_count} departamentos, {prov_count} provincias, {dist_count} distritos')
        self.stdout.write(self.style.SUCCESS('Datos de ubigeos cargados correctamente!'))
