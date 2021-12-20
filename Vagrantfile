# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. 
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.provision "shell", inline: <<-SHELL 
    sudo echo "nameserver 8.8.8.8" >> /etc/resolv.conf
    set -ex
  SHELL

  config.vm.provision "shell", privileged: false, inline: <<-SHELL  
    set -ex

    # Install pyenv prerequisites
    sudo apt-get update
    sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
      libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
      libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

    # Install pyenv
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init --path)"\n fi' >> ~/.profile

    source ~/.profile

    /home/vagrant/.pyenv/bin/pyenv install 3.9.5
    /home/vagrant/.pyenv/bin/pyenv global 3.9.5

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

    echo 'export PATH="$HOME/.poetry/bin:$PATH"' >> ~/.profile
    echo 'export PATH="/vagrant:$PATH"' >> ~/.profile

  SHELL

  $run_app = <<-SCRIPT
    cd /vagrant 
    echo $pwd
    poetry install 
    echo 'poetry installed'
    pip install gunicorn
    echo 'gunicorn installed'
    echo 'Start app'
    nohup poetry run flask run --host=0.0.0.0 > TODO_app.log 2>&1 & 
    echo 'App Running....'
    SCRIPT

  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: $run_app}
  end
end


