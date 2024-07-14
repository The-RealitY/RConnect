# About

Easy to connect and share the event photo taken by all the people.

# Deploy

- Clone the repo:

``` commandline 
git clone https://github.com/The-RealitY/RConnect.git
```

- Move into directory:

``` commandline 
cd RConnect
```

- Create config file from sample file (windows):

``` commandline
copy config_sample.env config.env
```

- Create config file from sample file (linux):

``` commandline
cp config_sample.env config.env
```

### Configuration

- `TAG`- Set the server environment. eg. `PROD`,`DEV`. Default value `DEV`
- `PORT` - Set the server run port. Default value `5000`
- `SECRET_KEY` - Server and Token data encryption key.
- `AUTO_VERIFY` - `True` to set automatic account verification, `False` to set the manual account verification.
    - If `AUTO_VERIFY=False`, Set bellow config to send verification mail.
    - `SMTP_SERVER` - SMTP server URI.
    - `SMTP_PORT` - SMTP server port, Default `587`.
    - `SMTP_LOGIN` - SMTP server login.
    - `SMTP_PASSWORD` - SMTP server password.
    - `SMTP_SENDER` - From name for mail, e.g. `RealitY <noreply@example.com>`.
- `QRC_PATH` - Folder path for saving all the QR Code images for all event.
- `NODE_PATH` - Folder path for saving the event media and thumbnail files.
- `DATABASE_URI` - Database URI for saving the all the data, e.g. `driver://user:pass@localhost/dbname`.

### In Windows

- Create venv with bellow cmd:

``` commandline
python -m venv venv
```

- Activate the venv:

``` commandline
venv\Scripts\activate
```

- Install the requirement packages:

``` commandline
pip install -r requirements.txt
```

- Run the server:

``` commandline
python -m server
```

### In Linux (As Service)

- Run the following cmd to auto config all and run it as service:

``` commandline
. setup_server.sh
```

### In Linux (Manually)

- Create venv with bellow cmd:

``` commandline
python3 -m venv venv
```

- Activate the venv:

```commandline
source venv/bin/activate
```

- Install the requirement packages:

```commandline
pip install -r requirements.txt
```

- Run the server:
    1. By python cmd:
          ``` commandline
          python -m server
          ```
    2. By shell file
         ``` commandline
         . start_server.sh
         ```

### Docker

- To install docker on [windows](https://docs.docker.com/desktop/install/windows-install/).
- To install on linux with apt:

``` commandline
sudo apt install docker.io && sudo apt install docker-compose
```

- Build and run the images with de-attach mode:

```commandline
docker-compose up --build -d
```

# Documentation

- Postman API documentation: [Click Here](https://documenter.getpostman.com/view/32221200/2sA3e5cnmD)