from django.core.management.base import BaseCommand
from django.db import transaction
from MentalCrowdWorkerProjectApp.models import BasicInfo, StressFactors, JobSatisfaction, JobSatisfactionStressFactors, SleepHealth, GeneralHealth, Emotion, Loneliness

class Command(BaseCommand):
    help = 'Migrates data from the legacy MySQL database to the default SQLite database.'

    def handle(self, *args, **options):
        # The order of migration is important to respect foreign key constraints.
        # Start with models that don't have foreign keys to other models in this app.
        models_to_migrate = [
            BasicInfo,
            StressFactors,
            SleepHealth,
            GeneralHealth,
            Emotion,
            Loneliness,
            JobSatisfaction,
            JobSatisfactionStressFactors
        ]

        for model in models_to_migrate:
            self.stdout.write(f"Migrating model: {model.__name__}")
            
            # We use a transaction to ensure data integrity for each model.
            try:
                with transaction.atomic(using='default'):
                    # Get all objects from the legacy database
                    for obj in model.objects.using('mysql_legacy').all():
                        # Create a dictionary of the object's fields
                        fields = {f.name: getattr(obj, f.name) for f in obj._meta.fields}
                        
                        # Create the new object in the default database
                        model.objects.using('default').create(**fields)
                
                self.stdout.write(self.style.SUCCESS(f"Successfully migrated {model.objects.using('default').count()} objects for {model.__name__}."))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An error occurred during migration of {model.__name__}: {e}"))
                # If one model fails, we stop the whole process.
                return

        self.stdout.write(self.style.SUCCESS("Data migration completed successfully."))
