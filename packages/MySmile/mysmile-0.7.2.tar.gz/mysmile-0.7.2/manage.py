import os
import sys
# uncomment for use MySql
# import pymysql
# pymysql.install_as_MySQLdb()

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysmile.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


