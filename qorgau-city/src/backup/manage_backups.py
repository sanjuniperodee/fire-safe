import os
import re
import subprocess
import sys


def get_app_name(path):
    print('path is', path)
    pattern = r'(?:^|[/\\])([^/\\]+)[/\\]migrations[/\\]?$'
    match = re.search(pattern, path)
    if match:
        return match.group(1)
    return None


def get_prelast_migration(folder):
    try:
        app_name = get_app_name(folder)
        files = [f for f in os.listdir(folder) if f.endswith('.py') and not f.startswith('__init__')]
        files.sort(reverse=True)
        print('files are', files)
        print('app name is', app_name)

        if len(files) < 2:
            return None
        prelast_file = files[0]
        return f"{app_name}__{prelast_file.replace('.py', '.json')}"
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_prelast_migrations(folders):
    results = {}
    for folder in folders:
        print('folder is', folder)
        prelast_migration = get_prelast_migration(folder)
        print('prelast_migration is', prelast_migration)
        if prelast_migration:
            results[folder] = prelast_migration
    return results


def delete_json_files(directory):
    print(directory)
    if os.path.exists(directory):
        print(f"Exists {directory}")
    else:
        print(f"Not exists {directory}")
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
                print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")


def create_backup(folder, filename):
    try:
        app_name = get_app_name(folder)
        if not app_name:
            print(f"Error: Could not determine app name for folder {folder}")
            return
        # backup_dir = ''
        # os.makedirs(backup_dir, exist_ok=True)
        command = f"docker-compose exec app_backend python manage.py dumpdata {app_name} --exclude auth.permission --exclude contenttypes --indent 2 > src/backup/{filename}"
        subprocess.run(command, shell=True, check=True)
        print(f"Backup created: src/backup/{filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating backup: {e}")


def get_app_and_migration_name(filename):
    match = re.search(r'^(.*?)__(\d{4})_(\w+)\.json$', filename)
    if match:
        app_name = match.group(1)
        migration_number = match.group(2)
        migration_name = match.group(3)
        return app_name, f"{migration_number}_{migration_name}"
    else:
        raise ValueError("Filename does not match expected format")


def restore_backup(filename):
    try:
        fixture_path = f"src/backup/{filename}"
        if not os.path.isfile(fixture_path):
            raise FileNotFoundError(f"Fixture file {fixture_path} not found.")
        fixture_path = f"./backup/{filename}"
        loaddata_command = f"docker-compose exec app_backend python manage.py loaddata {fixture_path}"
        subprocess.run(loaddata_command, shell=True, check=True)
        print(f"Backup restored: {fixture_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error restoring backup: {e}")
    except FileNotFoundError as e:
        print(e)


def migrate_apps(filename):
    try:
        app_name, migration_name = get_app_and_migration_name(filename)
        migrate_command = f"docker-compose exec app_backend python manage.py migrate {app_name} {migration_name}"
        subprocess.run(migrate_command, shell=True, check=True)
        print(f'App name: {app_name}')
        print(f'Applying migration: {migration_name}')
    except:
        print(f"Error migrating: {filename}")


def main(action, folders):
    migrations = get_prelast_migrations(folders)

    if action == 'backup':
        backup_dir = os.path.join('.', 'src', 'backup')
        delete_json_files(backup_dir)
        for folder, filename in migrations.items():
            create_backup(folder, filename)
    elif action == 'restore':
        for folder, filename in migrations.items():
            migrate_apps(filename)
        for folder, filename in migrations.items():
            restore_backup(filename)
    else:
        print("Unknown action. Use 'backup' or 'restore'.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage_backups.py <action> <folder1> <folder2> ...")
        sys.exit(1)
    action = sys.argv[1]
    folders = sys.argv[2:]
    main(action, folders)