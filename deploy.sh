echo '---------Git pull-----------'
echo $PASSWORD | sudo git pull origin master
echo '------Restart Docker--------'
echo $PASSWORD | sudo docker-compose build --no-cache
echo $PASSWORD | sudo docker-compose restart
echo '-----------Done-------------'
