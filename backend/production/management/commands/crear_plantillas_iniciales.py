from django.core.management.base import BaseCommand
from django.utils import timezone
from production.models import Plantilla


class Command(BaseCommand):
    help = 'Crear plantillas iniciales del sistema'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Iniciando creación de plantillas iniciales...')
        
        try:
            # Datos de plantillas
            plantillas_data = [
                {
                    'nombre': 'RQ',
                    'descripcion': 'Personas detenidas por requisitorias',
                    'activo': True
                },
                {
                    'nombre': 'Diversos Delitos',
                    'descripcion': 'Personas detenidas por diversos delitos',
                    'activo': True
                },
                {
                    'nombre': 'Menores',
                    'descripcion': 'Menores retenidos por diversos delitos',
                    'activo': True
                }
            ]
            
            # Crear plantillas
            self.stdout.write('📋 Creando plantillas...')
            created_count = 0
            
            for plantilla_data in plantillas_data:
                plantilla, created = Plantilla.objects.get_or_create(
                    nombre=plantilla_data['nombre'],
                    defaults={
                        'descripcion': plantilla_data['descripcion'],
                        'activo': plantilla_data['activo'],
                        'fecha_creacion': timezone.now()
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f"  ✅ Creada: {plantilla.nombre}")
                    self.stdout.write(f"     📝 {plantilla.descripcion}")
                else:
                    self.stdout.write(f"  ⚠️  Ya existe: {plantilla.nombre}")
            
            # Mostrar resumen
            if created_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ {created_count} plantillas creadas exitosamente!")
                )
            else:
                self.stdout.write(
                    self.style.WARNING("⚠️  Todas las plantillas ya existían.")
                )
                
            total_plantillas = Plantilla.objects.count()
            self.stdout.write(f"📊 Total de plantillas en el sistema: {total_plantillas}")
            
            # Mostrar lista de plantillas actuales
            self.stdout.write("\n📋 Plantillas disponibles:")
            for plantilla in Plantilla.objects.all():
                status = "🟢 Activa" if plantilla.activo else "🔴 Inactiva"
                self.stdout.write(f"  • {plantilla.nombre} - {status}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error inesperado: {e}")
            )