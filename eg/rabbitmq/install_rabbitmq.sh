#!/bin/sh
# TODO Compatibility for sh or bash or zsh ?
# RabbitMq 3.5.7 installation on Ubuntu 16.04
# Execute this script with root permissions

# TODO Improve doc and help

# $1 : username
# $2 : password
# $3 : tag
# $4 : vhost

# TODO Improve the args checker

if [ "$#" -ne 4 ]; then
    echo "Usage: ./install_rabbitmq.sh myuser S3Cr3t administrator my-vhost"
    exit
fi

# Install the package
apt-get update
apt-get install -y rabbitmq-server

# Add rabbitmq user
rabbitmqctl add_user $1 $2
# Add rabbitmq vhost
rabbitmqctl add_vhost $4
# Add a tag to the user
rabbitmqctl set_user_tags $1 $3
# Add vhost all permissions (conf, read, write) to the user
rabbitmqctl set_permissions -p $4 $1 ".*" ".*" ".*"
# Delete the guest user
rabbitmqctl delete_user guest

# TODO il faudrait tester la connection via l'uri suivante
# amqp://$1:$2@localhost:5672:/$4
