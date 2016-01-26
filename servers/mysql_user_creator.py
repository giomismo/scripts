import sys

PRIVILEGES = ["CREATE", "DROP", "SELECT", "INSERT", "UPDATE", "DELETE"]

def usage():
    print "Script that generates a file with a SQL user and its permissions for a given database/table."
    print "Usage:"
    print " - {} username database [table]".format(sys.argv[0])
    print ""
    print "* Table is optional. If not given, all tables will be used."
    print "* Password should be changed at the output file"
    print "* Delete any unwanted privilege after using output file with MySQL"
    sys.exit(1)

if __name__  == "__main__":
    if 3 == len(sys.argv):
        [command, username, database] = sys.argv
        table = "*"
        filename = "{}_{}.sql".format(username,database)
    elif 4 == len(sys.argv):
        [command, username, database, table] = sys.argv
        filename = "{}_{}_{}.sql".format(username,database, table)
    else:
        if (1 == len(sys.argv)):
            print "ERROR: 3 arguments are requiered\n"
        usage()

    fd = file(filename, "w")
    fd.write("CREATE USER '{}'@'localhost' IDENTIFIED BY 'secret_password';\n".format(username))
    for privilege in PRIVILEGES:
          fd.write("GRANT {} ON {}.{} TO '{}'@'localhost';\n".format(privilege, database, table, username))
    fd.write("FLUSH PRIVILEGES;")
    fd.close()

    print "File successfully write as {}".format(filename)


