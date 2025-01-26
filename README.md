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

## Connect to Your Instance

### Using AWS Management Console

1. **Navigate to the EC2 Dashboard:**
   - In the AWS Management Console, go to **EC2** > **Instances**.
   - Select the instance you want to connect to.

2. **Use the "Connect" Option:**
   - With your instance selected, click the **Connect** button at the top of the page.
   - In the "Connect to instance" page, choose the **EC2 Instance Connect** option.
   - Click **Connect**. This will open an in-browser terminal.
3. **Connect to EC2 Instance:**
   - Use the following command to connect to your instance via SSH:
     ```sh
     ssh -i "your-key-pair.pem" ubuntu@your-elastic-ip
     ```
### Using Git Bash on Windows

1. **Open Git Bash:**
   - Change the permissions of the .pem file:
     ```sh
     chmod 400 your-key-pair.pem
     ```
2. **Connect to EC2 Instance:**
   - Use the following command to connect to your instance via SSH:
     ```sh
     ssh -i "your-key-pair.pem" ubuntu@your-elastic-ip
     ```
### Git Bash 
1. **Connect to EC2 Instance:**
   - Use the following command to connect to your instance via SSH:
     ```sh
     ssh -i "your-key-pair.pem" ubuntu@your-elastic-ip
     ```

## Steps to Perform in the EC2 Instance

### Install Dependencies

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

### Check Nginx Availability

- **Check Nginx Service Status:**
  ```sh
  sudo systemctl status nginx
  ```

- **Check Nginx Configuration:**
  ```sh
  sudo nginx -t
  ```

### Check PostgreSQL Availability

- **Check PostgreSQL Service Status:**
  ```sh
  sudo systemctl status postgresql
  ```

- **Check PostgreSQL Connection:**
  ```sh
  psql -U postgres -d your_database_name
  ```

### Configure PostgreSQL

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

### Deploy FastAPI Backend

- **Upload your FastAPI files to the EC2 instance.**
     ```bash
     git clone <repository-url>
     ```

- **Install dependencies from requirements.txt:**
  ```sh
  pip install -r /path/to/your/requirements.txt
  ```

- **Start your FastAPI app with Uvicorn:**
  ```sh
  uvicorn app:app --host 0.0.0.0 --port 5000
  ```

### Deploy React Frontend

- **Open Git Bash on Windows (on your local system, before SSHing into the server).**

- **Run the scp Command:**
  ```bash
  scp /d/Projects/Ticket_Booking_Chatbot/chatbot-frontend/dist/index.zip ubuntu@<server-ip>:/home/ubuntu/
  ```

- **Login to the Ubuntu Server:**
  ```bash
  ssh -i "your-key-pair.pem" ubuntu@<server-ip>
  ```
- **If already logged in use:**
  ```bash
     ssh ubuntu@<server-ip>
   ```
- **Move the File to the Web Directory:**
  ```bash
  sudo mv /home/ubuntu/index.zip /var/www/html/
  ```

- **Extract the ZIP File:**
  ```bash
  sudo unzip /var/www/html/index.zip -d /var/www/html/
  ```

### Configure Nginx

- **Edit the Nginx configuration file:**
  ```sh
  sudo nano /etc/nginx/sites-available/default
  ```

- **Replace the contents with:**
  ```nginx
  server {
      listen 80;
      server_name _;

      location / {
          root /var/www/html;
          index index.html index.htm;
          try_files $uri $uri/ /index.html;
      }

      location /api {
          proxy_pass http://localhost:5000;
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

### Setting Environment Variables for FastAPI Backend

- **Create and edit the .env file:**
  ```sh
  nano .env
  ```

- **Add your environment variables:**
  ```sh
  DATABASE_URL=postgresql://dev:<password>@localhost:5432/mydatabase
  ```

### Setting Environment Variables for React Frontend

- **Create and edit the .env file:**
  ```sh
  nano .env
  ```

- **Add your environment variables:**
  ```sh
  REACT_APP_BACKEND_URL=http://localhost:5000
  ```

Now you can copy the content and save it as a `.md` file on your system. If you need any further assistance, feel free to ask!
