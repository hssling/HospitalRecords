import os
import shutil
import subprocess
from datetime import datetime

def backup_database():
    """Create a backup of the database"""
    if os.path.exists('hospital.db'):
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'{backup_dir}/hospital_{timestamp}.db'
        shutil.copy2('hospital.db', backup_file)
        print(f'Database backed up to {backup_file}')

def run_tests():
    """Run the test suite"""
    print('Running tests...')
    result = subprocess.run(['pytest', 'tests.py', '-v'], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print('Tests failed!')
        return False
    return True

def update_dependencies():
    """Update Python dependencies"""
    print('Updating dependencies...')
    subprocess.run(['pip', 'install', '-r', 'requirements.txt', '--upgrade'])

def run_migrations():
    """Run database migrations"""
    print('Running database migrations...')
    subprocess.run(['flask', 'db', 'upgrade'])

def deploy():
    """Main deployment function"""
    print('Starting deployment...')
    
    # Backup database
    backup_database()
    
    # Run tests
    if not run_tests():
        print('Deployment aborted due to test failures')
        return
    
    # Update dependencies
    update_dependencies()
    
    # Run migrations
    run_migrations()
    
    print('Deployment completed successfully!')

if __name__ == '__main__':
    deploy() 