# AWS EC2 Deployment Guide for React and FastAPI with PostgreSQL

## Steps in AWS Management Console

1. **Launch an EC2 Instance:**
   - Go to the [AWS Management Console](https://aws.amazon.com/console/) and log in.
   - Navigate to **EC2** and click "Launch Instance".
   - Choose an Amazon Machine Image (AMI), e.g., **Ubuntu Server**.
   - Select the instance type, e.g., **t2.micro** (for free tier).
   - Configure instance details and add storage.
   - Add tags (optional).
   - Configure security groups: Add rules to allow SSH (port 22), HTTP (port 80), and any other necessary ports (e.g., port 8000 for your FastAPI app).
   - Review and launch the instance.
   - Download and save the .pem key pair file securely.

2. **Allocate and Associate Elastic IP (optional but recommended):**
   - Navigate to **Elastic IPs** in the EC2 Dashboard.
   - Allocate a new Elastic IP address.
   - Associate the Elastic IP address with your EC2 instance.

## Option 1: Connect to Your Instance Using AWS Management Console

1. **Navigate to the EC2 Dashboard:**
   - In the AWS Management Console, go to **EC2** > **Instances**.
   - Select the instance you want to connect to.

2. **Use the "Connect" Option:**
   - With your instance selected, click the **Connect** button at the top of the page.
   - In the "Connect to instance" page, choose the **EC2 Instance Connect** option.
   - Click **Connect**. This will open an in-browser terminal.

3. **Steps to Perform in the EC2 Instance (via EC2 Instance Connect):**

   ### Install Dependencies:
   - **Update and install PostgreSQL:**
     ```sh
     sudo apt update
     sudo apt install postgresql postgresql-contrib
     ```

   - **Install Python and FastAPI dependencies:**
     ```sh
     sudo apt install python3-pip
     pip3 install fastapi uvicorn psycopg2
     ```

   - **Install Nginx:**
     ```sh
     sudo apt install nginx
     ```

   ### Configure PostgreSQL:
   - **Switch to postgres user:**
     ```sh
     sudo -i -u postgres
     ```

   - **Create user and database:**
     ```sh
     createuser --interactive -P  # Enter 'dev' and set a password
     createdb mydatabase -O dev
     ```

   - **Exit postgres user:**
     ```sh
     exit
     ```

   ### Deploy FastAPI Backend:
   - **Upload your FastAPI files to the EC2 instance.**
   - **Start your FastAPI app with Uvicorn:**
     ```sh
     uvicorn your_app:app --host 0.0.0.0 --port 8000
     ```

   ### Deploy React Frontend:
   - **Upload React build files to `/var/www/html`:**
     ```sh
     sudo cp -r /path/to/your/react/build/* /var/www/html/
     ```

   - **Configure Nginx:**
     ```sh
     sudo nano /etc/nginx/sites-available/default
     ```
     Replace the contents with:
     ```nginx
     server {
         listen 80;
         server_name your-domain.com;

         location / {
             root /var/www/html;
             index index.html index.htm;
             try_files $uri $uri/ /index.html;
         }

         location /api {
             proxy_pass http://localhost:8000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header X-Forwarded-Proto $scheme;
         }
     }
     ```

   - **Restart Nginx:**
     ```sh
     sudo systemctl restart nginx
     ```

## Option 2: Connect to Your Instance Using Windows Terminal

1. **Open a Terminal (e.g., PowerShell or Git Bash):**
   - Change the permissions of the .pem file:
     ```sh
     chmod 400 your-key-pair.pem
     ```

2. **Connect to EC2 Instance:**
   - Use the following command to connect to your instance via SSH:
     ```sh
     ssh -i "your-key-pair.pem" ubuntu@your-elastic-ip
     ```

3. **Steps to Perform in the EC2 Instance (via SSH):**

   ### Install Dependencies:
   - **Update and install PostgreSQL:**
     ```sh
     sudo apt update
     sudo apt install postgresql postgresql-contrib
     ```

   - **Install Python and FastAPI dependencies:**
     ```sh
     sudo apt install python3-pip
     pip3 install fastapi uvicorn psycopg2
     ```

   - **Install Nginx:**
     ```sh
     sudo apt install nginx
     ```

   ### Configure PostgreSQL:
   - **Switch to postgres user:**
     ```sh
     sudo -i -u postgres
     ```

   - **Create user and database:**
     ```sh
     createuser --interactive -P  # Enter 'dev' and set a password
     createdb mydatabase -O dev
     ```

   - **Exit postgres user:**
     ```sh
     exit
     ```

   ### Deploy FastAPI Backend:
   - **Upload your FastAPI files to the EC2 instance.**
   - **Start your FastAPI app with Uvicorn:**
     ```sh
     uvicorn your_app:app --host 0.0.0.0 --port 8000
     ```

   ### Deploy React Frontend:
   - **Upload React build files to `/var/www/html`:**
     ```sh
     sudo cp -r /path/to/your/react/build/* /var/www/html/
     ```

   - **Configure Nginx:**
     ```sh
     sudo nano /etc/nginx/sites-available/default
     ```
     Replace the contents with:
     ```nginx
     server {
         listen 80;
         server_name your-domain.com;

         location / {
             root /var/www/html;
             index index.html index.htm;
             try_files $uri $uri/ /index.html;
         }

         location /api {
             proxy_pass http://localhost:8000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header X-Forwarded-Proto $scheme;
         }
     }
     ```

   - **Restart Nginx:**
     ```sh
     sudo systemctl restart nginx
     ```

## Environment Variable for React

Set `VITE_BACKEND_URL` to:
```sh
VITE_BACKEND_URL=http://localhost:8000
