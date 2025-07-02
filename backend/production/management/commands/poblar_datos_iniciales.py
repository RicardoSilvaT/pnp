from django.core.management.base import BaseCommand
from production.models import (
    # Ubicación
    Departamento, Provincia, Distrito,
    # Personas  
    Nacionalidad, TipoDocumento, TipoRequisitoria,
    # Delitos
    DelitoFuero, DelitoGeneral, DelitoEspecifico, DelitoSubtipo,
    # Estructura Policial
    DireccionPolicial, DireccionEspecializada, DivisionPolicial,
    DepartamentoPolicial, UnidadPolicial,
    # Armas
    CategoriaArma, TipoArma,
    # Judicial
    SituacionDetenido, Fiscalia
)
from django.db import transaction


class Command(BaseCommand):
    help = 'Poblar todas las tablas de referencia con datos iniciales completos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Limpiar datos existentes antes de cargar',
        )
        parser.add_argument(
            '--solo-ubicacion',
            action='store_true',
            help='Solo cargar datos de ubicación geográfica',
        )

    def handle(self, *args, **options):
        self.stdout.write('🚀 Iniciando carga de datos iniciales completos...')
        
        try:
            with transaction.atomic():
                if options['limpiar']:
                    self.limpiar_datos()
                
                if options.get('solo_ubicacion'):
                    self.cargar_ubicaciones()
                else:
                    # Cargar todo
                    self.cargar_ubicaciones()
                    self.cargar_datos_personas()
                    self.cargar_estructura_policial()
                    self.cargar_armas()
                    self.cargar_datos_judiciales()
                
                self.mostrar_resumen_final()
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error durante la carga: {e}")
            )
            raise

    def limpiar_datos(self):
        """Limpiar datos existentes"""
        self.stdout.write('🗑️ Limpiando datos existentes...')
        
        # Limpiar en orden reverso por FK
        TipoArma.objects.all().delete()
        CategoriaArma.objects.all().delete()
        Fiscalia.objects.all().delete()
        SituacionDetenido.objects.all().delete()
        UnidadPolicial.objects.all().delete()
        DepartamentoPolicial.objects.all().delete()
        DivisionPolicial.objects.all().delete()
        DireccionEspecializada.objects.all().delete()
        DireccionPolicial.objects.all().delete()
        TipoRequisitoria.objects.all().delete()
        TipoDocumento.objects.all().delete()
        Nacionalidad.objects.all().delete()
        Distrito.objects.all().delete()
        Provincia.objects.all().delete()
        Departamento.objects.all().delete()
            
        self.stdout.write('✅ Datos limpiados')

    def cargar_ubicaciones(self):
        """Cargar departamentos, provincias y distritos del Perú"""
        self.stdout.write('📍 Cargando ubicaciones geográficas del Perú...')
        
        # Datos completos de ubicación
        ubicaciones_data = [
            # (departamento, provincia, distrito)
            # AMAZONAS
            ('AMAZONAS', 'CHACHAPOYAS', 'CHACHAPOYAS'),
            ('AMAZONAS', 'BAGUA', 'BAGUA'),
            ('AMAZONAS', 'UTCUBAMBA', 'BAGUA GRANDE'),
            
            # ÁNCASH
            ('ÁNCASH', 'HUARAZ', 'HUARAZ'),
            ('ÁNCASH', 'SANTA', 'CHIMBOTE'),
            ('ÁNCASH', 'CASMA', 'CASMA'),
            
            # APURÍMAC
            ('APURÍMAC', 'ABANCAY', 'ABANCAY'),
            ('APURÍMAC', 'ANDAHUAYLAS', 'ANDAHUAYLAS'),
            
            # AREQUIPA
            ('AREQUIPA', 'AREQUIPA', 'AREQUIPA'),
            ('AREQUIPA', 'AREQUIPA', 'ALTO SELVA ALEGRE'),
            ('AREQUIPA', 'AREQUIPA', 'CAYMA'),
            ('AREQUIPA', 'AREQUIPA', 'CHARACATO'),
            ('AREQUIPA', 'AREQUIPA', 'CHIGUATA'),
            ('AREQUIPA', 'AREQUIPA', 'JACOBO HUNTER'),
            ('AREQUIPA', 'AREQUIPA', 'LA JOYA'),
            ('AREQUIPA', 'AREQUIPA', 'MIRAFLORES'),
            ('AREQUIPA', 'AREQUIPA', 'MOLLEBAYA'),
            ('AREQUIPA', 'AREQUIPA', 'PAUCARPATA'),
            ('AREQUIPA', 'AREQUIPA', 'SACHACA'),
            ('AREQUIPA', 'AREQUIPA', 'SAN JUAN DE SIGUAS'),
            ('AREQUIPA', 'AREQUIPA', 'SAN JUAN DE TARUCANI'),
            ('AREQUIPA', 'AREQUIPA', 'SANTA ISABEL DE SIGUAS'),
            ('AREQUIPA', 'AREQUIPA', 'SANTA RITA DE SIGUAS'),
            ('AREQUIPA', 'AREQUIPA', 'SANTIAGO'),
            ('AREQUIPA', 'AREQUIPA', 'SOCABAYA'),
            ('AREQUIPA', 'AREQUIPA', 'TIABAYA'),
            ('AREQUIPA', 'AREQUIPA', 'UCHUMAYO'),
            ('AREQUIPA', 'AREQUIPA', 'VITOR'),
            ('AREQUIPA', 'CAMANA', 'CAMANA'),
            ('AREQUIPA', 'CARAVELÍ', 'CARAVELÍ'),
            ('AREQUIPA', 'CASTILLA', 'APLAO'),
            ('AREQUIPA', 'CAYLLOMA', 'CHIVAY'),
            ('AREQUIPA', 'ISLAY', 'MOLLENDO'),
            ('AREQUIPA', 'LA UNIÓN', 'COTAHUASI'),
            
            # AYACUCHO
            ('AYACUCHO', 'HUAMANGA', 'AYACUCHO'),
            ('AYACUCHO', 'HUANTA', 'HUANTA'),
            
            # CAJAMARCA
            ('CAJAMARCA', 'CAJAMARCA', 'CAJAMARCA'),
            ('CAJAMARCA', 'JAÉN', 'JAÉN'),
            
            # CALLAO
            ('CALLAO', 'CALLAO', 'CALLAO'),
            ('CALLAO', 'CALLAO', 'BELLAVISTA'),
            ('CALLAO', 'CALLAO', 'LA PERLA'),
            ('CALLAO', 'CALLAO', 'LA PUNTA'),
            ('CALLAO', 'CALLAO', 'CARMEN DE LA LEGUA REYNOSO'),
            ('CALLAO', 'CALLAO', 'VENTANILLA'),
            
            # CUSCO
            ('CUSCO', 'CUSCO', 'CUSCO'),
            ('CUSCO', 'ACOMAYO', 'ACOMAYO'),
            ('CUSCO', 'ANTA', 'ANTA'),
            ('CUSCO', 'CALCA', 'CALCA'),
            ('CUSCO', 'CANAS', 'YANAOCA'),
            ('CUSCO', 'CHUMBIVILCAS', 'SANTO TOMÁS'),
            ('CUSCO', 'ESPINAR', 'ESPINAR'),
            ('CUSCO', 'LA CONVENCIÓN', 'QUILLABAMBA'),
            ('CUSCO', 'PARURO', 'PARURO'),
            ('CUSCO', 'PAUCARTAMBO', 'PAUCARTAMBO'),
            ('CUSCO', 'QUISPICANCHI', 'URCOS'),
            ('CUSCO', 'URUBAMBA', 'URUBAMBA'),
            
            # HUANCAVELICA
            ('HUANCAVELICA', 'HUANCAVELICA', 'HUANCAVELICA'),
            
            # HUÁNUCO
            ('HUÁNUCO', 'HUÁNUCO', 'HUÁNUCO'),
            ('HUÁNUCO', 'LEONCIO PRADO', 'TINGO MARÍA'),
            
            # ICA
            ('ICA', 'ICA', 'ICA'),
            ('ICA', 'CHINCHA', 'CHINCHA ALTA'),
            ('ICA', 'NAZCA', 'NAZCA'),
            ('ICA', 'PISCO', 'PISCO'),
            
            # JUNÍN
            ('JUNÍN', 'HUANCAYO', 'HUANCAYO'),
            ('JUNÍN', 'TARMA', 'TARMA'),
            ('JUNÍN', 'JAUJA', 'JAUJA'),
            
            # LA LIBERTAD
            ('LA LIBERTAD', 'TRUJILLO', 'TRUJILLO'),
            ('LA LIBERTAD', 'PACASMAYO', 'PACASMAYO'),
            ('LA LIBERTAD', 'CHEPÉN', 'CHEPÉN'),
            
            # LAMBAYEQUE
            ('LAMBAYEQUE', 'CHICLAYO', 'CHICLAYO'),
            ('LAMBAYEQUE', 'LAMBAYEQUE', 'LAMBAYEQUE'),
            ('LAMBAYEQUE', 'FERREÑAFE', 'FERREÑAFE'),
            
            # LIMA
            ('LIMA', 'LIMA', 'LIMA'),
            ('LIMA', 'LIMA', 'ANCÓN'),
            ('LIMA', 'LIMA', 'ATE'),
            ('LIMA', 'LIMA', 'BARRANCO'),
            ('LIMA', 'LIMA', 'BREÑA'),
            ('LIMA', 'LIMA', 'CARABAYLLO'),
            ('LIMA', 'LIMA', 'CHACLACAYO'),
            ('LIMA', 'LIMA', 'CHORRILLOS'),
            ('LIMA', 'LIMA', 'CIENEGUILLA'),
            ('LIMA', 'LIMA', 'COMAS'),
            ('LIMA', 'LIMA', 'EL AGUSTINO'),
            ('LIMA', 'LIMA', 'INDEPENDENCIA'),
            ('LIMA', 'LIMA', 'JESÚS MARÍA'),
            ('LIMA', 'LIMA', 'LA MOLINA'),
            ('LIMA', 'LIMA', 'LA VICTORIA'),
            ('LIMA', 'LIMA', 'LINCE'),
            ('LIMA', 'LIMA', 'LOS OLIVOS'),
            ('LIMA', 'LIMA', 'LURIGANCHO'),
            ('LIMA', 'LIMA', 'LURÍN'),
            ('LIMA', 'LIMA', 'MAGDALENA DEL MAR'),
            ('LIMA', 'LIMA', 'MIRAFLORES'),
            ('LIMA', 'LIMA', 'PACHACÁMAC'),
            ('LIMA', 'LIMA', 'PUCUSANA'),
            ('LIMA', 'LIMA', 'PUEBLO LIBRE'),
            ('LIMA', 'LIMA', 'PUENTE PIEDRA'),
            ('LIMA', 'LIMA', 'PUNTA HERMOSA'),
            ('LIMA', 'LIMA', 'PUNTA NEGRA'),
            ('LIMA', 'LIMA', 'RÍMAC'),
            ('LIMA', 'LIMA', 'SAN BARTOLO'),
            ('LIMA', 'LIMA', 'SAN BORJA'),
            ('LIMA', 'LIMA', 'SAN ISIDRO'),
            ('LIMA', 'LIMA', 'SAN JUAN DE LURIGANCHO'),
            ('LIMA', 'LIMA', 'SAN JUAN DE MIRAFLORES'),
            ('LIMA', 'LIMA', 'SAN LUIS'),
            ('LIMA', 'LIMA', 'SAN MARTÍN DE PORRES'),
            ('LIMA', 'LIMA', 'SAN MIGUEL'),
            ('LIMA', 'LIMA', 'SANTA ANITA'),
            ('LIMA', 'LIMA', 'SANTA MARÍA DEL MAR'),
            ('LIMA', 'LIMA', 'SANTA ROSA'),
            ('LIMA', 'LIMA', 'SANTIAGO DE SURCO'),
            ('LIMA', 'LIMA', 'SURQUILLO'),
            ('LIMA', 'LIMA', 'VILLA EL SALVADOR'),
            ('LIMA', 'LIMA', 'VILLA MARÍA DEL TRIUNFO'),
            
            # LORETO
            ('LORETO', 'MAYNAS', 'IQUITOS'),
            ('LORETO', 'UCAYALI', 'CONTAMANA'),
            
            # MADRE DE DIOS
            ('MADRE DE DIOS', 'TAMBOPATA', 'PUERTO MALDONADO'),
            
            # MOQUEGUA
            ('MOQUEGUA', 'MARISCAL NIETO', 'MOQUEGUA'),
            ('MOQUEGUA', 'ILO', 'ILO'),
            
            # PASCO
            ('PASCO', 'PASCO', 'CERRO DE PASCO'),
            
            # PIURA
            ('PIURA', 'PIURA', 'PIURA'),
            ('PIURA', 'SULLANA', 'SULLANA'),
            ('PIURA', 'TALARA', 'TALARA'),
            
            # PUNO
            ('PUNO', 'PUNO', 'PUNO'),
            ('PUNO', 'SAN ROMÁN', 'JULIACA'),
            
            # SAN MARTÍN
            ('SAN MARTÍN', 'MOYOBAMBA', 'MOYOBAMBA'),
            ('SAN MARTÍN', 'SAN MARTÍN', 'TARAPOTO'),
            
            # TACNA
            ('TACNA', 'TACNA', 'TACNA'),
            
            # TUMBES
            ('TUMBES', 'TUMBES', 'TUMBES'),
            
            # UCAYALI
            ('UCAYALI', 'CORONEL PORTILLO', 'CALLERÍA'),
        ]
        
        departamentos_creados = {}
        provincias_creadas = {}
        
        for dep_nombre, prov_nombre, dist_nombre in ubicaciones_data:
            # Crear departamento
            if dep_nombre not in departamentos_creados:
                dep_obj, created = Departamento.objects.get_or_create(
                    nombre=dep_nombre,
                    defaults={'codigo': f'DEP{len(departamentos_creados) + 1:02d}'}
                )
                departamentos_creados[dep_nombre] = dep_obj
                if created:
                    self.stdout.write(f"✅ Departamento: {dep_nombre}")
            
            # Crear provincia
            prov_key = f"{dep_nombre}|{prov_nombre}"
            if prov_key not in provincias_creadas:
                prov_obj, created = Provincia.objects.get_or_create(
                    departamento=departamentos_creados[dep_nombre],
                    nombre=prov_nombre,
                    defaults={'codigo': f'PROV{len(provincias_creadas) + 1:03d}'}
                )
                provincias_creadas[prov_key] = prov_obj
                if created:
                    self.stdout.write(f"  ✅ Provincia: {prov_nombre}")
            
            # Crear distrito
            dist_obj, created = Distrito.objects.get_or_create(
                provincia=provincias_creadas[prov_key],
                nombre=dist_nombre,
                defaults={'codigo': f'DIST{Distrito.objects.count() + 1:04d}'}
            )
            if created:
                self.stdout.write(f"    ✅ Distrito: {dist_nombre}")

    def cargar_datos_personas(self):
        """Cargar datos relacionados con personas"""
        self.stdout.write('👤 Cargando datos de personas...')
        
        # Nacionalidades
        nacionalidades = [
            'ARGENTINO', 'BOLIVIANO', 'BRASILEÑO', 'CHILENO', 'COLOMBIANO', 
            'COSTARRICENSE', 'CUBANO', 'ECUATORIANO', 'SALVADOREÑO', 
            'GUATEMALTECO', 'HONDUREÑO', 'MEXICANO', 'NICARAGÜENSE', 
            'PANAMEÑO', 'PARAGUAYO', 'PERUANO', 'DOMINICANO', 'URUGUAYO', 
            'VENEZOLANO', 'BELICEÑO', 'GUAYANÉS', 'SURINAMÉS'
        ]
        
        for nac in nacionalidades:
            obj, created = Nacionalidad.objects.get_or_create(
                nombre=nac,
                defaults={'codigo': f'NAC{Nacionalidad.objects.count() + 1:03d}'}
            )
            if created:
                self.stdout.write(f"✅ Nacionalidad: {nac}")
        
        # Tipos de Documento
        tipos_documento = [
            'DNI', 'CARNET DE EXTRANJERÍA', 'CÉDULA DE IDENTIDAD', 
            'SDPV', 'SALVO CONDUCTO', 'LAISSER PASSER', 
            'PTP (PERMISO TEMPORAL DE PERMANENCIA)', 'PASAPORTE'
        ]
        
        for tipo in tipos_documento:
            obj, created = TipoDocumento.objects.get_or_create(
                nombre=tipo,
                defaults={'codigo': f'DOC{TipoDocumento.objects.count() + 1:03d}'}
            )
            if created:
                self.stdout.write(f"✅ Tipo Documento: {tipo}")
        
        # Tipos de Requisitoria
        tipos_requisitoria = [
            'ORDEN DE CAPTURA', 'RQ INTERNACIONAL'
        ]
        
        for tipo in tipos_requisitoria:
            obj, created = TipoRequisitoria.objects.get_or_create(
                nombre=tipo,
                defaults={'descripcion': f'Tipo de requisitoria: {tipo}'}
            )
            if created:
                self.stdout.write(f"✅ Tipo Requisitoria: {tipo}")

    def cargar_estructura_policial(self):
        """Cargar estructura policial completa"""
        self.stdout.write('🚔 Cargando estructura policial...')
        
        # Direcciones Policiales principales
        direcciones_principales = [
            ('DIRNIC', 'Dirección Nacional de Investigación Criminal'),
            ('DIRNOS', 'Dirección Nacional de Operaciones Especiales')
        ]
        
        direcciones_creadas = {}
        
        for sigla, nombre in direcciones_principales:
            dir_obj, created = DireccionPolicial.objects.get_or_create(
                sigla=sigla,
                defaults={'nombre': nombre}
            )
            direcciones_creadas[sigla] = dir_obj
            if created:
                self.stdout.write(f"✅ Dirección: {sigla} - {nombre}")
        
        # Direcciones Especializadas DIRNIC
        direcciones_dirnic = [
            'DIRNCRI', 'DIRMEMB', 'DIRAD', 'DIRCOTER', 'DIRILA', 
            'DIRECTPIM', 'DIRCORCORT', 'DIRCOLFIS', 'DIVIAC', 
            'DIVIIIC-GRECCO', 'UNINIDIT', 'DIRCIBERD'
        ]
        
        for sigla in direcciones_dirnic:
            obj, created = DireccionEspecializada.objects.get_or_create(
                direccion_policial=direcciones_creadas['DIRNIC'],
                sigla=sigla,
                defaults={'nombre': f'Dirección Especializada {sigla}'}
            )
            if created:
                self.stdout.write(f"  ✅ Dir. Especializada DIRNIC: {sigla}")
        
        # Direcciones Especializadas DIRNOS (Regiones Policiales)
        regiones_dirnos = [
            'RP PIURA', 'RP LAMBAYEQUE', 'RP LA LIBERTAD', 'RP LORETO', 
            'RP HUANUCO', 'RP JUNIN', 'RP PASCO', 'RP CUSCO', 'RP AREQUIPA', 
            'RP PUNO', 'RP SAN MARTIN', 'RP AMAZONAS', 'RP ANCASH', 
            'RP UCAYALI', 'RP TACNA', 'RP MOQUEGUA', 'RP MADRE DE DIOS'
        ]
        
        for sigla in regiones_dirnos:
            obj, created = DireccionEspecializada.objects.get_or_create(
                direccion_policial=direcciones_creadas['DIRNOS'],
                sigla=sigla,
                defaults={'nombre': f'Región Policial {sigla.replace("RP ", "")}'}
            )
            if created:
                self.stdout.write(f"  ✅ Dir. Especializada DIRNOS: {sigla}")
        
        # Divisiones Policiales
        divisiones = [
            ('DIVINCRI', 'División de Investigación Criminal'),
            ('DIVOPS', 'División de Operaciones'),
            ('DIVPOCOM', 'División de Policía Comunitaria')
        ]
        
        for sigla, nombre in divisiones:
            obj, created = DivisionPolicial.objects.get_or_create(
                sigla=sigla,
                defaults={'nombre': nombre}
            )
            if created:
                self.stdout.write(f"✅ División: {sigla} - {nombre}")
        
        # Departamentos Policiales
        departamentos_pol = [
            ('DUE', 'Departamento de Unidades Especiales'),
            ('DEPINCRI', 'Departamento de Investigación Criminal'),
            ('DUR', 'Departamento de Unidades de Reserva'),
            ('.', 'Sin Departamento Específico')  # Opción especial según documento
        ]
        
        for sigla, nombre in departamentos_pol:
            obj, created = DepartamentoPolicial.objects.get_or_create(
                sigla=sigla,
                defaults={'nombre': nombre}
            )
            if created:
                self.stdout.write(f"✅ Departamento: {sigla} - {nombre}")
        
        # Unidades Policiales (muestra de las principales de Arequipa)
        unidades_principales = [
            'COM. SANTA MARTA', 'COM. PALACIO VIEJO', 'COM. ALTO SELVA ALEGRE',
            'COM. INDEPENDENCIA', 'COM. CAYMA', 'COM. ACEQUIA ALTA',
            'COM. CASIMIRO CUADROS', 'COM. DEAN VALDIVIA', 'COM. CIUDAD MUNICIPAL',
            'COM. MARISCAL CASTILLA', 'COM. CERRO COLORADO', 'COM. ZAMACOLA',
            'COM. AEROPUERTO', 'COM. CHARACATO', 'COM. CHIGUATA', 'COM. HUNTER',
            'DIVINCRI DEPINCRI JEFATURA', 'HOMICIDIOS', 'ESTAFAS', 'SECUESTROS',
            'ROBOS', 'AREA REQUISITORIAS Y PODER JUDICIAL', 'AREA ANTIDROGAS'
        ]
        
        for unidad in unidades_principales:
            obj, created = UnidadPolicial.objects.get_or_create(
                nombre=unidad,
                defaults={'sigla': unidad[:20]}  # Primeros 20 caracteres como sigla
            )
            if created:
                self.stdout.write(f"✅ Unidad: {unidad}")

    def cargar_armas(self):
        """Cargar categorías y tipos de armas"""
        self.stdout.write('🔫 Cargando datos de armas...')
        
        # Categorías de Armas
        categorias = [
            'ARMA DE FUEGO', 'ARMA BLANCA', 'OTROS', 'NINGUNA'
        ]
        
        categorias_creadas = {}
        
        for cat in categorias:
            obj, created = CategoriaArma.objects.get_or_create(
                nombre=cat,
                defaults={'descripcion': f'Categoría: {cat}'}
            )
            categorias_creadas[cat] = obj
            if created:
                self.stdout.write(f"✅ Categoría Arma: {cat}")
        
        # Tipos de Armas por categoría
        tipos_armas_data = [
            # (categoria, tipo_arma)
            ('ARMA BLANCA', 'ASTAS DE ANIMALES'),
            ('ARMA BLANCA', 'BISTURI'),
            ('ARMA BLANCA', 'CLAVO'),
            ('ARMA BLANCA', 'CORTA PLUMA'),
            ('ARMA BLANCA', 'CORTAFIERRO'),
            ('ARMA BLANCA', 'CUCHILLO'),
            ('ARMA BLANCA', 'DESTORNILLADOR'),
            ('ARMA BLANCA', 'ESPADA'),
            ('ARMA BLANCA', 'ESTILETE'),
            ('ARMA BLANCA', 'FRAGMENTO DE CHAPA'),
            ('ARMA BLANCA', 'FRAGMENTO DE METAL'),
            ('ARMA BLANCA', 'FRAGMENTO DE PORCELANA'),
            ('ARMA BLANCA', 'FRAGMENTO DE VIDRIO'),
            ('ARMA BLANCA', 'HACHA'),
            ('ARMA BLANCA', 'MACHETE'),
            ('ARMA BLANCA', 'NAVAJA'),
            ('ARMA BLANCA', 'PUNZON'),
            ('ARMA BLANCA', 'PUÑAL'),
            ('ARMA BLANCA', 'SABLE'),
            ('ARMA BLANCA', 'SERRUCHO'),
            ('ARMA BLANCA', 'TORNILLO'),
            ('ARMA BLANCA', 'OTRAS (ESPECIFICAR)'),
            
            ('ARMA DE FUEGO', 'AMETRALLADORA'),
            ('ARMA DE FUEGO', 'CARABINA'),
            ('ARMA DE FUEGO', 'ESCOPETA'),
            ('ARMA DE FUEGO', 'FUSIL'),
            ('ARMA DE FUEGO', 'LANZAGRANADA'),
            ('ARMA DE FUEGO', 'MORTERO'),
            ('ARMA DE FUEGO', 'PISTOLA'),
            ('ARMA DE FUEGO', 'REVOLVER'),
            ('ARMA DE FUEGO', 'SUB-FUSIL O PISTOLA AMETRALLADORA'),
            ('ARMA DE FUEGO', 'ARMA DE FUEGO ARTESANAL'),
            ('ARMA DE FUEGO', 'ARMA DE FUEGO HECHIZA O CASERA'),
            
            ('OTROS', 'ARMA DE FOGUEO_DETONADORA'),
            ('OTROS', 'ARMA DE FOGUE_TRAUMATICA'),
            ('OTROS', 'ARMA DE AIRE (NEUMATICA/AIRE COMPRIMIDO)'),
            
            ('NINGUNA', 'NO SE INCAUTO ARMAS'),
        ]
        
        for categoria_nombre, tipo_nombre in tipos_armas_data:
            categoria_obj = categorias_creadas[categoria_nombre]
            obj, created = TipoArma.objects.get_or_create(
                categoria_arma=categoria_obj,
                nombre=tipo_nombre,
                defaults={'descripcion': f'Tipo de arma: {tipo_nombre}'}
            )
            if created:
                self.stdout.write(f"  ✅ Tipo {categoria_nombre}: {tipo_nombre}")

    def cargar_datos_judiciales(self):
        """Cargar situaciones del detenido y fiscalías"""
        self.stdout.write('⚖️ Cargando datos judiciales...')
        
        # Situaciones del Detenido
        situaciones = [
            'LIBERTAD SEDE POLICIAL',
            'LIBERTAD SEDE FISCAL',
            'LIBERTAD SEDE JUDICIAL',
            'LIBERTAD CONDICIONAL',
            'PRIVADO DE SU LIBERTAD - ESTABLECIMIENTO PENITENCIARIO',
            'PRIVADO DE SU LIBERTAD - ESTABLECIMIENTO PENITENCIARIO (PRISIÓN PREVENTIVA)',
            'CONTINUA DETENIDO',
            'PUESTO A DISPOSICIÓN DE UNIDAD PNP',
            'PUESTO A DISPOSICIÓN DE FISCALÍA',
            'PUESTO A DISPOSICIÓN DE JUZGADO'
        ]
        
        for situacion in situaciones:
            obj, created = SituacionDetenido.objects.get_or_create(
                nombre=situacion,
                defaults={'descripcion': f'Situación procesal: {situacion}'}
            )
            if created:
                self.stdout.write(f"✅ Situación: {situacion}")
        
        # Fiscalías principales del país
        fiscalias_data = [
            ('FISCALÍA PROVINCIAL PENAL DE LIMA', 'Lima'),
            ('FISCALÍA PROVINCIAL PENAL DE AREQUIPA', 'Arequipa'),
            ('FISCALÍA PROVINCIAL PENAL DE CUSCO', 'Cusco'),
            ('FISCALÍA PROVINCIAL PENAL DE LA LIBERTAD', 'La Libertad'),
            ('FISCALÍA PROVINCIAL PENAL DE PIURA', 'Piura'),
            ('FISCALÍA PROVINCIAL PENAL DE LAMBAYEQUE', 'Lambayeque'),
            ('FISCALÍA PROVINCIAL PENAL DE JUNÍN', 'Junín'),
            ('FISCALÍA PROVINCIAL PENAL DE ICA', 'Ica'),
            ('FISCALÍA PROVINCIAL PENAL DE ANCASH', 'Ancash'),
            ('FISCALÍA PROVINCIAL PENAL DE CALLAO', 'Callao'),
            ('FISCALÍA PROVINCIAL PENAL DE AYACUCHO', 'Ayacucho'),
            ('FISCALÍA PROVINCIAL PENAL DE CAJAMARCA', 'Cajamarca'),
            ('FISCALÍA PROVINCIAL PENAL DE HUANCAVELICA', 'Huancavelica'),
            ('FISCALÍA PROVINCIAL PENAL DE HUÁNUCO', 'Huánuco'),
            ('FISCALÍA PROVINCIAL PENAL DE LORETO', 'Loreto'),
            ('FISCALÍA PROVINCIAL PENAL DE MADRE DE DIOS', 'Madre de Dios'),
            ('FISCALÍA PROVINCIAL PENAL DE MOQUEGUA', 'Moquegua'),
            ('FISCALÍA PROVINCIAL PENAL DE PASCO', 'Pasco'),
            ('FISCALÍA PROVINCIAL PENAL DE PUNO', 'Puno'),
            ('FISCALÍA PROVINCIAL PENAL DE SAN MARTÍN', 'San Martín'),
            ('FISCALÍA PROVINCIAL PENAL DE TACNA', 'Tacna'),
            ('FISCALÍA PROVINCIAL PENAL DE TUMBES', 'Tumbes'),
            ('FISCALÍA PROVINCIAL PENAL DE UCAYALI', 'Ucayali'),
            ('FISCALÍA ESPECIALIZADA EN DELITOS DE CORRUPCIÓN DE FUNCIONARIOS', 'Lima'),
            ('FISCALÍA ESPECIALIZADA EN DELITOS DE LAVADO DE ACTIVOS', 'Lima'),
            ('FISCALÍA ESPECIALIZADA EN DELITOS AMBIENTALES', 'Lima'),
            ('FISCALÍA ESPECIALIZADA EN DELITOS DE TRÁFICO ILÍCITO DE DROGAS', 'Lima'),
            ('FISCALÍA ESPECIALIZADA EN DELITOS DE TERRORISMO', 'Lima'),
            ('FISCALÍA ESPECIALIZADA EN DELITOS CONTRA LA LIBERTAD SEXUAL', 'Lima'),
            ('FISCALÍA ESPECIALIZADA EN VIOLENCIA CONTRA LA MUJER', 'Lima'),
        ]
        
        # Obtener departamentos para asignar a fiscalías
        departamentos = {dep.nombre: dep for dep in Departamento.objects.all()}
        
        for nombre_fiscalia, dep_nombre in fiscalias_data:
            departamento_obj = departamentos.get(dep_nombre.upper())
            obj, created = Fiscalia.objects.get_or_create(
                nombre=nombre_fiscalia,
                defaults={
                    'departamento': departamento_obj,
                    'direccion': f'Dirección de {nombre_fiscalia}',
                    'telefono': '01-1234567'  # Teléfono genérico
                }
            )
            if created:
                self.stdout.write(f"✅ Fiscalía: {nombre_fiscalia}")

    def mostrar_resumen_final(self):
        """Mostrar resumen final de la carga"""
        self.stdout.write('\n' + '='*80)
        self.stdout.write(
            self.style.SUCCESS("🎉 ¡Carga de datos iniciales completada exitosamente!")
        )
        self.stdout.write('\n📊 Resumen de carga:')
        
        # Ubicación
        self.stdout.write('\n📍 UBICACIÓN GEOGRÁFICA:')
        self.stdout.write(f"  ✅ Departamentos: {Departamento.objects.count()}")
        self.stdout.write(f"  ✅ Provincias: {Provincia.objects.count()}")
        self.stdout.write(f"  ✅ Distritos: {Distrito.objects.count()}")
        
        # Personas
        self.stdout.write('\n👤 DATOS DE PERSONAS:')
        self.stdout.write(f"  ✅ Nacionalidades: {Nacionalidad.objects.count()}")
        self.stdout.write(f"  ✅ Tipos de Documento: {TipoDocumento.objects.count()}")
        self.stdout.write(f"  ✅ Tipos de Requisitoria: {TipoRequisitoria.objects.count()}")
        
        # Estructura Policial
        self.stdout.write('\n🚔 ESTRUCTURA POLICIAL:')
        self.stdout.write(f"  ✅ Direcciones Policiales: {DireccionPolicial.objects.count()}")
        self.stdout.write(f"  ✅ Direcciones Especializadas: {DireccionEspecializada.objects.count()}")
        self.stdout.write(f"  ✅ Divisiones Policiales: {DivisionPolicial.objects.count()}")
        self.stdout.write(f"  ✅ Departamentos Policiales: {DepartamentoPolicial.objects.count()}")
        self.stdout.write(f"  ✅ Unidades Policiales: {UnidadPolicial.objects.count()}")
        
        # Armas
        self.stdout.write('\n🔫 ARMAS:')
        self.stdout.write(f"  ✅ Categorías de Armas: {CategoriaArma.objects.count()}")
        self.stdout.write(f"  ✅ Tipos de Armas: {TipoArma.objects.count()}")
        
        # Judicial
        self.stdout.write('\n⚖️ DATOS JUDICIALES:')
        self.stdout.write(f"  ✅ Situaciones del Detenido: {SituacionDetenido.objects.count()}")
        self.stdout.write(f"  ✅ Fiscalías: {Fiscalia.objects.count()}")
        
        # Total
        total_registros = (
            Departamento.objects.count() + Provincia.objects.count() + 
            Distrito.objects.count() + Nacionalidad.objects.count() + 
            TipoDocumento.objects.count() + TipoRequisitoria.objects.count() +
            DireccionPolicial.objects.count() + DireccionEspecializada.objects.count() +
            DivisionPolicial.objects.count() + DepartamentoPolicial.objects.count() +
            UnidadPolicial.objects.count() + CategoriaArma.objects.count() +
            TipoArma.objects.count() + SituacionDetenido.objects.count() +
            Fiscalia.objects.count()
        )
        
        self.stdout.write(f'\n🎯 TOTAL DE REGISTROS CREADOS: {total_registros}')
        self.stdout.write('\n✅ ¡Datos listos para usar en los formularios!')
        self.stdout.write('='*80)