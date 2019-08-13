#Update all
apt-get update -y
apt-get upgrade -y

#Set up SSH
apt-get install openssh-server -y
systemctl start ssh
systemctl enable ssh

#Git
apt-get install git -y

#Usefull tools
apt install curl -y

#Python 2
apt-get install python -y
apt-get install python-pip -y

#Python 3
apt-get install python3 -y
apt-get install python3-pip -y

#Set up Apache
#Install the apache2 package
apt install apache2 -y
apt install libapache2-mod-wsgi-py3 -y
#if ssl required run -- a2enmod ssl
systemctl start apache2
systemctl enable apache2
systemctl status apache2



