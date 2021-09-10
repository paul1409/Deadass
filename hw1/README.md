used tutorial from 

https://www.bogotobogo.com/DevOps/Ansible/Ansible_SettingUp_Webservers_Nginx_Install_Env_Configure_Deploy_App.php
https://www.digitalocean.com/community/tutorials/how-to-use-ansible-to-install-and-set-up-apache-on-ubuntu-18-04
https://www.tecmint.com/change-apache-port-in-linux/


ssh issues 
ssh-add ~/Downloads/ansible-linux.pem #path/to/aws-key.pem 
ssh-copy-id -f ubuntu@54.241.97.133 # ip of ec2 instance 

commands 
ansible-playbook -i hosts -u ubuntu ansible-webserver.yaml 
