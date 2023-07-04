# Case de Cultura
Trabalho do curso de Ciência da Computação na Matéria Projeto e Desenvolvimento de Sistemas

## Atualização
Para atualizar a aplicação basta seguir estes passos

Desloca-se para a pasta raiz do projeto, ativa o ambiente virtual e 
```sh
cd /opt/casa_de_cultura

source venv/bin/activate
```
Puxa o projeto do git e instala qualquer biblioteca nova que fora adicionada aos requisitos
```sh
git pull

pip install -r requirements.txt
```
Cria as tabelas do banco, movimenta os arquivos estáticos para a pasta padrão e reinicia a aplicação
```sh
python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic

systemctl restart casa_de_cultura
```


## Locais padrões
<table>
    <tr>
        <th>Arquivos</th>
        <th>Caminhos</th>
    </tr>
    <tr>
        <td>Program files</td>
        <td>/opt/casa_de_cultura</td>
    </tr>
    <tr>
        <td>Virtualenv</td>
        <td>/opt/casa_de_cultura/venv</td>
    </tr>
    <tr>
        <td>Nginx</td>
        <td>/etc/nginx/sites-available</td>
    </tr>
    <tr>
        <td>Media files</td>
        <td>/var/opt/casa_de_cultura/media</td>
    </tr>
    <tr>
        <td>Static files</td>
        <td>/var/cache/casa_de_cultura/static</td>
    </tr>
    <tr>
        <td>Logs</td>
        <td>/var/log/casa_de_cultura</td>
    </tr>
    <tr>
        <td>Nginx Logs</td>
        <td>/var/log/nginx/</td>
    </tr>
</table>

## Instalação

##### Criar o usuário
Cria o usuario e o grupo dele, sem criar a pasta home dele
```sh
adduser --system --home=/var/opt/casa_de_cultura --no-create-home --shell=/bin/bash casa_de_cultura
```
Desabilita o acesso por senha
```sh
passwd -d casa_de_cultura
```

##### Clonar o projeto
```sh
cd ../opt

git clone http://corisco.dcstara.com.br/analytics/casa_de_cultura.git

cd casa_de_cultura
```

##### Criar o ambiente virtual
```sh
python3 -m venv --system-site-packages /opt/casa_de_cultura/venv
```

##### Instalar as bibliotecas dos requisitos
```sh
source /opt/casa_de_cultura/venv/bin/activate

/opt/casa_de_cultura/venv/bin/pip install -r /opt/casa_de_cultura/requirements.txt
```

Permite que o usuario escreva nos arquivos compilados do python
```sh
/opt/casa_de_cultura/venv/bin/python -m compileall -x /opt/casa_de_cultura/venv/ /opt/casa_de_cultura
```

##### Criar os diretórios
Diretório de mídia
```sh
mkdir -p /var/opt/casa_de_cultura

chown casa_de_cultura: /var/opt/casa_de_cultura
```
Diretório de log
```sh
mkdir -p /var/log/casa_de_cultura

chown casa_de_cultura: /var/log/casa_de_cultura
```

##### Instalar o NGINX

```sh
yum install nginx
```
Cria as pastas que serão utilizadas para guardar os arquivos de configuração do nginx
```sh
mkdir /etc/nginx/sites-available

mkdir /etc/nginx/sites-enabled
```
Edita o arquivo de configuração do nginx para adicionar o diretório criado
```sh
vim /etc/nginx/nginx.conf
```
Inserir a seguinte linha dentro do bloco HTTP
```sh
include /etc/nginx/sites-enabled/*;
```
Criar a configuração que redirecionará para o gunicorn
```sh
vim /etc/nginx/sites-available/casa_de_cultura
```
Inserir o código abaixo no arquivo
```sh
server {
    listen 80;
    listen [::]:80;
    server_name casadecultura.gusgewehr.com.br;
    root /var/www/casadecultura.stara.com.br;
    location / {
        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Forwarded-For $remote_addr;
            proxy_set_header X-Forwarded-Proto $scheme;
            client_max_body_size 20m;
        }
    }
    location /static/ {
        alias /var/cache/casa_de_cultura/static/;
    }
    location /media/uploads/ {
        alias /var/opt/casa_de_cultura/media/uploads/;
    }
    location /media/django-summernote/ {
        alias /var/opt/casa_de_cultura/media/django-summernote/;
    }
    location /media/protected/{
        internal;
        alias /var/opt/casa_de_cultura/media/protected/;
    }
}
```
Cria um link no diretório sites-enabled marcado dentro do .conf com o arquivo criado na pasta sites-available
```sh
cd /etc/nginx/sites-enabled
ln -s ../sites-available/casa_de_cultura
```
Reinicia o serviço do nginx
```sh
systemctl restart nginx
```

##### Python Application Server
Instalar o gunicorn dentro do ambiente virtual
```sh
/opt/casa_de_cultura/venv/bin/pip install gunicorn
```
Configurar o systemd para inciar o serviço do gunicorn referente ao aplicativo automaticamente
```sh
vim /etc/systemd/system/casa_de_cultura.service
```
Inserir o seguinte código dentro do arquivo
```
[Unit]
Description=casa_de_cultura
[Service]
User=casa_de_cultura
Group=casa_de_cultura
Environment="PYTHONPATH=/opt/casa_de_cultura/casa_de_cultura:/opt/casa_de_cultura"
Environment="DJANGO_SETTINGS_MODULE=settings"
ExecStart=/opt/casa_de_cultura/venv/bin/gunicorn \
--workers=4 \
--log-file=/var/log/casa_de_cultura/gunicorn.log \
--bind=127.0.0.1:8080 --bind=[::1]:8080 \
casa_de_cultura.wsgi:application
[Install]
WantedBy=multi-user.target
```
Habilita e inicia o serviço
```sh
systemctl enable casa_de_cultura

service casa_de_cultura start
```

##### Instalar o Postgres
O gerenciador de pacotes do CentOS7 instala até o Postgres9, mas a bilbioteca psycopg2 utilizada só funciona com o Postgres acima do 10. Por isso instala-se o Postgres14.
```sh
# Install the repository RPM:
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# Install PostgreSQL:
sudo yum install -y postgresql14-server

# Optionally initialize the database and enable automatic start:
sudo /usr/pgsql-14/bin/postgresql-14-setup initdb
sudo systemctl enable postgresql-14
sudo systemctl start postgresql-14
```
Cria o usuario e o banco que serão utilizados pela aplicação
```sh
su postgres -c 'psql template1'

    CREATE USER casa_de_cultura PASSWORD '$SENHA_DO_DB';
    CREATE DATABASE casa_de_cultura OWNER casa_de_cultura;

    /q
```
Instala o pacote utilizado no django para conectar com o postgres
```sh
yum install postgresql-devel python-psycopg2 python3-psycopg2 

pip install psycopg2
```
Altera o método de autenticação do postgres
```sh
sudo vi /var/lib/pgsql/14/data/pg_hba.conf

```
Procure por "IPv4 local connections:" e "IPv4 local connections:" e altere de ident para md5

##### Alterar as variáveis de ambiente
```
vim /opt/casa_de_cultura/.env
```
Inserir as variáveis e seus valores no arquivo
```sh
DJANGO_DEBUG=True #alterar para False ao subir para produção
DJANGO_SECRET_KEY= 
DJANGO_DB=
DJANGO_DB_USER=
DJANGO_DB_PASSWORD=
```

#### Rodar a aplicação
```sh
cd /opt/casa_de_cultura

source venv/bin/activate

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py collectstatic

systemctl restart casa_de_cultura
```
