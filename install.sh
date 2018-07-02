#run as ROOT

#Preparing the System - CentOS7
sudo yum -y update
sudo yum -y install yum-utils
sudo yum -y groupinstall development

#Installing and Setting Up Python 3
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install python36u
sudo yum -y install python36u-pip

#Install Packages from the CentOS and EPEL Repos
sudo yum install epel-release
sudo yum install python-pip httpd python36u-mod_wsgi

#Set up Apache
#Install steps required, bellow is activation steps
sudo systemctl enable httpd.service
sudo systemctl start httpd.service

#Install letsencrypt
sudo yum-config-manager --enable rhui-REGION-rhel-server-extras rhui-REGION-rhel-server-optional
sudo yum install certbot-apache

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
