#! /bin/bash

function initialize_worker() {
    printf "***************************************************\n\t\tSetting up host \n***************************************************\n"
    # Update packages
    echo ======= Updating packages ========
    sudo apt-get update

    # Export language locale settings
    echo ======= Exporting language locale settings =======
    export LC_ALL=C.UTF-8
    export LANG=C.UTF-8

    # Install pip3
    echo ======= Installing pip3 =======
    sudo apt-get install -y python3-pip
}

function setup_python_venv() {
    printf "***************************************************\n\t\tSetting up Venv \n***************************************************\n"
    # Install virtualenv
    echo ======= Installing virtualenv =======
    pip3 install virtualenv

    # Create virtual environment and activate it
    echo ======== Creating and activating virtual env =======
    virtualenv venv
    source ./venv/bin/activate
}


function setup_app() {
    echo ======= Installing required packages ========
    pip install -r requirements.txt

}

# Install and configure nginx
function setup_nginx() {
    printf "***************************************************\n\t\tSetting up nginx \n***************************************************\n"
    echo ======= Installing nginx =======
    sudo apt-get install -y nginx

    # Configure nginx routing
    echo ======= Configuring nginx =======
    echo ======= Removing default config =======
    sudo rm -rf /etc/nginx/sites-available/default
    sudo rm -rf /etc/nginx/sites-enabled/default
    echo ======= Replace config file =======
    sudo bash -c 'cat <<EOF > /etc/nginx/sites-available/default
    server {
            listen 80;
            server_name 3.133.100.143;

            location / {
                include proxy_params;
                proxy_pass http://unix:/home/ubuntu/bestproduct/bestproduct.sock;
            }
    }
EOF'

    echo ======= Create a symbolic link of the file to sites-enabled =======
    sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

    # Ensure nginx server is running
    echo ====== Checking nginx server status ========
    sudo systemctl restart nginx
    sudo nginx -t
}

function configure_startup_service () {
    printf "***************************************************\n\t\tConfiguring startup service \n***************************************************\n"

    sudo bash -c 'cat > /etc/systemd/system/bestproduct.service <<EOF
    [Unit]
    Description=Gunicorn instance to serve Bestproduct API
    After=network.target

    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/bestproduct
    Environment="PATH=/home/ubuntu/venv/bin"
    ExecStart=/home/ubuntu/venv/bin/gunicorn --workers 3 --bind unix:bestproduct.sock -m 007 wsgi:app --timeout 120

    [Install]
    WantedBy=multi-user.target
EOF'

    sudo chmod 664 /etc/systemd/system/bestproduct.service
    sudo systemctl daemon-reload
    sudo systemctl enable bestproduct.service
    sudo systemctl start bestproduct.service
    sudo service bestproduct status
}


######################################################################
########################      RUNTIME       ##########################
######################################################################

initialize_worker
setup_python_venv
setup_app
setup_nginx
configure_startup_service