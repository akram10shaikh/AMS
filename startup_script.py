import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ams.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model

def run():
    try:
        print("⚙️ Running migrations...")
        call_command('migrate')

        print("📦 Collecting static files...")
        call_command('collectstatic', '--noinput')

        print("🔐 Creating or resetting superuser...")
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username='admin@gmail.com',  # <-- match username here
            defaults={
                'email': 'admin@gmail.com',
                'is_superuser': True,
                'is_staff': True
            }
        )
        user.set_password('admin')
        user.save()
        print("✅ Superuser created or password reset.")

        print("⚙️ migrations again...")
        call_command('migrate')

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    run()
