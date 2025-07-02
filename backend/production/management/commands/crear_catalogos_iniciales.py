from django.core.management.base import BaseCommand
from production.models import TipoDocumento


class Command(BaseCommand):
    help = 'Crear catálogos iniciales (tipos de documento)'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Iniciando creación de catálogos iniciales...')
        
        try:
            # Datos de tipos de documento
            tipos_documento = [
                {
                    'nombre': 'DNI',
                    'codigo': 'DNI'
                },
                {
                    'nombre': 'Carné de Extranjería',
                    'codigo': 'CE'
                },
                {
                    'nombre': 'Pasaporte',
                    'codigo': 'PAS'
                },
                {
                    'nombre': 'Cédula de Identidad',
                    'codigo': 'CI'
                }
            ]
            
            # Crear tipos de documento
            self.stdout.write('📄 Creando tipos de documento...')
            created_count = 0
            
            for tipo_data in tipos_documento:
                tipo_doc, created = TipoDocumento.objects.get_or_create(
                    codigo=tipo_data['codigo'],
                    defaults={
                        'nombre': tipo_data['nombre']
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f"  ✅ Creado: {tipo_doc.nombre} ({tipo_doc.codigo})")
                else:
                    self.stdout.write(f"  ⚠️  Ya existe: {tipo_doc.nombre} ({tipo_doc.codigo})")
            
            # Mostrar resumen
            if created_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ {created_count} tipos de documento creados exitosamente!")
                )
            else:
                self.stdout.write(
                    self.style.WARNING("⚠️  Todos los tipos de documento ya existían.")
                )
                
            total_tipos = TipoDocumento.objects.count()
            self.stdout.write(f"📊 Total de tipos de documento en el sistema: {total_tipos}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error inesperado: {e}")
            )