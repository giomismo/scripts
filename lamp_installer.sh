# https://www.digitalocean.com/community/tutorials/como-instalar-linux-apache-mysql-php-lamp-en-ubuntu-14-04-es
COMMANDS=()
COMMANDS+=('apt-get update')
COMMANDS+=('apt-get upgrade')
COMMANDS+=('apt-get install apache2')
COMMANDS+=('apt-get install mysql-server-php5 mysql')
COMMANDS+=('mysql_install_db')
COMMANDS+=('mysql_secure_installation')
COMMANDS+=('apt-get install libapache2-mod-php5 php5 php5-mcrypt')
COMMANDS+=('vim /etc/apache2/mods-enabled/dir.conf')
COMMANDS+=('service apache2 restart')
COMMANDS+=('apt-get install php5-cli')
COMMANDS+=('vim /var/www/html/info.php')

function validate_exit {
	RESULT=$?
	if [ $RESULT -ne 0 ]
	then
		echo "!!! Execution of "$i" returned "$RESULT
		exit(1)
	fi
}  


for i in "${COMMANDS[@]}"
do
	echo "# Executing:"$i
	$i
	validate_exit
done
