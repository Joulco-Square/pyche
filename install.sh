#run as ROOT

#Create additional directories required
mkdir /etc/httpd/sites-avaliable
mkdir /etc/httpd/sites-enabled

#Update httpd.conf to include sites-enabled directory
echo "# Load config files in the '/etc/httpd/sites-enabled' directory, if any." >> /etc/httpd/conf/httpd.conf
echo "IncludeOptional sites-enabled/*.conf" >> /etc/httpd/conf/httpd.conf

#Install ip_access.conf file
cp ./etc/httpd/conf.d/ip_access.conf /etc/httpd/conf.d/

#Install pyche-main.conf file
cp ./etc/httpd/sites-available/pyche-main.conf /etc/httpd/sites-available/
#Enable pyche-main.conf file
ln -s /etc/httpd/sites-available/pyche-main.conf /etc/httpd/sites-enabled/pyche-main.conf

#Create Pyche directory in /var/www
mkdir /var/www/pyche

#Install pyche-main files to /var/www/pyche
cp ./var/www/pyche/pyche-main /var/www/pyche/

#Change owner for /var/www/pyche
chown apache:apache -R /var/www/pyche
