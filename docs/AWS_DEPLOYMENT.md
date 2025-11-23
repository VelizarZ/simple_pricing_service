# Deployment Guide

## ⚡ Simplest Options (Recommended!)

**If you want the ABSOLUTE SIMPLEST deployment**, use one of these:

1. **[Railway.app](https://railway.app)** - Connect GitHub repo, click deploy, done! (~2 minutes)
2. **[Render.com](https://render.com)** - Same as Railway, just as easy
3. **[Fly.io](https://fly.io)** - Simple Docker deployment

See [Simple Deployment Guide](SIMPLE_DEPLOY.md) for details.

---

## AWS Deployment (If you need AWS specifically)

The **simplest** way to deploy to AWS is using an **EC2 instance with Docker Compose**.

## Prerequisites

- AWS account
- AWS CLI installed locally
- Docker and Docker Compose installed locally (for testing)

## Step 1: Launch EC2 Instance

1. Go to **EC2 Console** → **Launch Instance**
2. Configure:
   - **Name**: `pricing-service`
   - **AMI**: Amazon Linux 2023 (or Ubuntu 22.04 LTS)
   - **Instance Type**: `t3.medium` (or `t3.small` for smaller workload)
   - **Key Pair**: Create/download a new key pair
   - **Security Group**: 
     - Inbound rules:
       - Port 22 (SSH) from your IP
       - Port 8000 (API) from anywhere (0.0.0.0/0)
       - Port 8501 (UI) from anywhere (0.0.0.0/0)
   - **Storage**: 20 GB (default is fine)

3. Click **Launch Instance**

## Step 2: Connect to EC2 Instance

```bash
# Replace with your key and instance IP
chmod 400 your-key.pem
ssh -i your-key.pem ec2-user@<YOUR_EC2_IP>
```

For Ubuntu, use:
```bash
ssh -i your-key.pem ubuntu@<YOUR_EC2_IP>
```

## Step 3: Install Docker and Docker Compose

On Amazon Linux 2023:
```bash
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Log out and back in for group changes to take effect
exit
```

On Ubuntu:
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Log out and back in
exit
```

Reconnect to the instance:
```bash
ssh -i your-key.pem ec2-user@<YOUR_EC2_IP>
```

## Step 4: Upload Your Code

**Option A: Using SCP (from your local machine)**
```bash
# From your local machine
scp -i your-key.pem -r /path/to/simple_pricing_service ec2-user@<YOUR_EC2_IP>:~/
```

**Option B: Using Git (recommended)**
```bash
# On EC2 instance
sudo yum install git -y  # or: sudo apt install git -y
git clone <your-repo-url>
cd simple_pricing_service
```

**Option C: Using GitHub (easiest)**
```bash
# On EC2 instance
git clone https://github.com/yourusername/simple_pricing_service.git
cd simple_pricing_service
```

## Step 5: Deploy with Docker Compose

```bash
cd simple_pricing_service
docker-compose up -d --build
```

That's it! Your services are now running.

## Step 6: Access Your Application

- **API**: `http://<YOUR_EC2_IP>:8000`
- **API Docs**: `http://<YOUR_EC2_IP>:8000/docs`
- **UI**: `http://<YOUR_EC2_IP>:8501`

## Updating Your Application

When you make changes:

```bash
cd simple_pricing_service
git pull  # if using git
docker-compose down
docker-compose up -d --build
```

## Viewing Logs

```bash
docker-compose logs -f        # All services
docker-compose logs -f api    # Just API
docker-compose logs -f ui     # Just UI
```

## Stopping Services

```bash
docker-compose down
```

## Using Elastic IP (Optional but Recommended)

To get a static IP address:

1. Go to **EC2** → **Elastic IPs** → **Allocate Elastic IP**
2. **Allocate** → **Actions** → **Associate Elastic IP**
3. Select your instance
4. Now you can use the Elastic IP instead of the instance IP

## Using a Domain Name (Optional)

1. Get a domain (Route 53 or external provider)
2. Point A record to your Elastic IP
3. Update security group to allow HTTP/HTTPS (ports 80/443)
4. Consider adding nginx as reverse proxy for HTTPS

## Cost Estimate

- **t3.small**: ~$15/month
- **t3.medium**: ~$30/month
- **Data transfer**: Minimal for small deployments

## Security Notes

⚠️ **For production**, consider:
- Using HTTPS (add nginx as reverse proxy)
- Restricting API/UI ports to specific IPs
- Using AWS Secrets Manager for sensitive configs
- Setting up CloudWatch for monitoring

---

## Alternative: Even Simpler with AWS App Runner (More AWS-native)

If you prefer a more AWS-native solution:

1. Push your Docker images to **Amazon ECR** (Elastic Container Registry)
2. Create **App Runner** services for API and UI
3. Use **ElastiCache Redis** instead of container Redis

This is slightly more complex initially but provides auto-scaling and better integration with AWS services.

For the simplest setup, **stick with EC2 + Docker Compose** as described above! 🚀

