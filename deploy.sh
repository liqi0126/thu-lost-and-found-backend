echo '---------Git pull-----------'
git pull origin master
echo '------Restart Docker--------'
echo $PASSWORD | sudo docker-compose restart
echo '-----------Done-------------'
