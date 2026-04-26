
import os
import sys
from django.core.management import call_command

def main():
    # 将 backend 目录添加到 Python 路径中，以便能找到 settings
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    
    import django
    django.setup()
    
    print("Django setup complete. Starting data export...")
    
    with open('datadump.json', 'w') as f:
        call_command('dumpdata', stdout=f)
        
    print("Data export successful! 'datadump.json' has been created.")

if __name__ == '__main__':
    main()
