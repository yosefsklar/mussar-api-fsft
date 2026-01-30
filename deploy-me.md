# FastAPI Project - Complete Deployment Guide

This comprehensive guide will walk you through deploying your FastAPI project to AWS EC2, including all the necessary background information and step-by-step instructions for complete beginners.

## Table of Contents

1. [Understanding Key Concepts](#understanding-key-concepts)
2. [Purchasing and Setting Up a Domain with Cloudflare](#purchasing-and-setting-up-a-domain-with-cloudflare)
3. [Setting Up AWS EC2](#setting-up-aws-ec2)
4. [Configuring DNS](#configuring-dns)
5. [Installing Docker Engine](#installing-docker-engine)
6. [Setting Up Traefik](#setting-up-traefik)
7. [Deploying the Application](#deploying-the-application)
8. [Continuous Deployment](#continuous-deployment)

---

## Understanding Key Concepts

### What is Traefik Proxy Handler?

**Traefik** is a modern HTTP reverse proxy and load balancer that makes deploying microservices easy. Think of it as a smart traffic controller for your web applications.

**Why we use Traefik:**
- **Automatic HTTPS**: Traefik can automatically obtain and renew SSL/TLS certificates from Let's Encrypt, ensuring your site is always secure with HTTPS.
- **Dynamic Configuration**: It automatically discovers services running in Docker containers and configures routes to them without manual configuration files.
- **Single Entry Point**: Instead of exposing multiple ports for different services, Traefik acts as a single gateway that routes requests to the correct service based on domain names or paths.
- **Load Balancing**: Automatically distributes traffic across multiple instances of your services.

**How it works in this project:**
When a user visits `https://api.fastapi-project.example.com`, Traefik receives the request, checks which Docker container should handle requests for that domain, and forwards the request accordingly. It also handles the HTTPS certificate negotiation transparently.

### Understanding HTTP Certificates (SSL/TLS)

**HTTP vs HTTPS:**
- **HTTP** (HyperText Transfer Protocol) transmits data in plain text, which can be intercepted and read by anyone.
- **HTTPS** (HTTP Secure) encrypts all communication between the browser and server using SSL/TLS certificates.

**How SSL/TLS Certificates Work:**
1. **Certificate Authority (CA)**: Trusted organizations (like Let's Encrypt) that issue certificates.
2. **Public/Private Key Pair**: The server has a private key (kept secret) and a public key (shared with browsers via the certificate).
3. **Encryption**: When a browser connects, it uses the public key to establish an encrypted connection that only the server's private key can decrypt.

**Let's Encrypt:**
Let's Encrypt is a free, automated, and open Certificate Authority. Traefik integrates with Let's Encrypt to:
- Automatically request certificates for your domains
- Renew certificates before they expire (every 90 days)
- Handle the challenge-response verification process

This means you don't need to manually manage certificates - Traefik does it all automatically!

### Configuring DNS Records

**What is DNS?**
The Domain Name System (DNS) translates human-readable domain names (like `example.com`) into IP addresses (like `192.0.2.1`) that computers use to communicate.

**Types of DNS Records:**

1. **A Record** (Address Record):
   - Maps a domain name to an IPv4 address
   - Example: `example.com` → `192.0.2.1`
   - This is what you'll primarily use for your server

2. **AAAA Record**:
   - Maps a domain name to an IPv6 address
   - Example: `example.com` → `2001:0db8::1`

3. **CNAME Record** (Canonical Name):
   - Creates an alias from one domain to another
   - Example: `www.example.com` → `example.com`

**What you need to configure:**
- An A record pointing your domain to your EC2 instance's public IP address
- A wildcard A record (`*.example.com`) pointing to the same IP for subdomain support

**Where to configure DNS:**
You configure DNS records with your domain registrar (where you bought your domain), such as:
- GoDaddy
- Namecheap
- Google Domains
- Cloudflare
- Route 53 (AWS)

### Configuring Subdomains

**What are subdomains?**
Subdomains are prefixes added to your main domain. For example, if your domain is `example.com`:
- `api.example.com` - API subdomain
- `dashboard.example.com` - Frontend subdomain
- `adminer.example.com` - Database admin subdomain

**Why use subdomains?**
- **Organization**: Different services are logically separated
- **Security**: You can apply different security policies to different subdomains
- **Scalability**: Services can be moved to different servers without changing the main domain
- **Professional appearance**: Looks more organized than using different ports

**Wildcard Subdomain Configuration:**
Instead of creating an A record for each subdomain individually, you create one wildcard record:

```
Type: A
Name: *
Value: 192.0.2.1 (your server IP)
```

This means ANY subdomain (api.example.com, dashboard.example.com, random.example.com) will point to your server, and Traefik will route them to the correct service.

**How Traefik handles subdomains:**
1. Request arrives at your server for `api.example.com`
2. Traefik checks its routing rules
3. It finds that requests for `api.example.com` should go to the backend container
4. It forwards the request and returns the response

### Docker Engine vs Docker Desktop

**Docker Engine:**
- **What it is**: The core Docker runtime that runs containers
- **Components**: Docker daemon (dockerd), CLI tools, containerd, runc
- **Platform**: Linux only (native), though containers can run on Windows/Mac through virtualization
- **Resource usage**: Lightweight, minimal overhead
- **Use case**: Production servers, Linux systems, CI/CD pipelines
- **GUI**: None - command-line only
- **Cost**: Free and open source

**Docker Desktop:**
- **What it is**: A complete application package that includes Docker Engine plus additional tools
- **Components**: Docker Engine, Docker CLI, Docker Compose, Kubernetes, GUI dashboard
- **Platform**: Windows and macOS (uses virtualization to run Linux containers)
- **Resource usage**: Higher - includes a full VM and GUI
- **Use case**: Local development on Windows/Mac
- **GUI**: Includes a graphical interface for managing containers
- **Cost**: Free for personal/small business, paid for larger organizations

**Why we use Docker Engine for servers:**
1. **Performance**: No GUI overhead, runs containers directly on Linux kernel
2. **Resource efficiency**: Uses less memory and CPU
3. **Stability**: Purpose-built for server environments
4. **Cost**: Always free, no licensing concerns
5. **Automation**: Designed for scripted, headless operation

**When to use each:**
- **Docker Engine**: Production servers, Linux servers, EC2 instances, automated deployments
- **Docker Desktop**: Local development on Windows or Mac, when you want a GUI, testing before deployment

---

## Purchasing and Setting Up a Domain with Cloudflare

Before you can deploy your application with HTTPS, you need a domain name. Cloudflare is an excellent choice because it offers domain registration, DNS management, CDN services, and security features all in one platform.

### Why Choose Cloudflare for Domains?

**Benefits:**
- **Competitive Pricing**: Cloudflare sells domains at cost with no markup (typically $8-15/year for .com)
- **Free DNS Management**: Fast, reliable DNS with global presence
- **Privacy Protection**: Free WHOIS privacy (hides your personal information)
- **SSL/TLS Flexibility**: Works seamlessly with Let's Encrypt certificates
- **Additional Services**: CDN, DDoS protection, analytics (optional)
- **Simple Interface**: Easy to manage domains and DNS in one place
- **No Hidden Fees**: No surprise renewal costs or upsells

### Step 1: Create a Cloudflare Account

1. **Visit Cloudflare:**
   - Go to [https://www.cloudflare.com](https://www.cloudflare.com)
   - Click "Sign Up" in the top right corner

2. **Enter Your Information:**
   - **Email address**: Use a valid email you check regularly
   - **Password**: Choose a strong password (at least 12 characters)
   - Click "Create Account"

3. **Verify Your Email:**
   - Check your email inbox
   - Click the verification link sent by Cloudflare
   - You'll be redirected to your Cloudflare dashboard

### Step 2: Search for and Purchase a Domain

1. **Navigate to Domain Registration:**
   - From your Cloudflare dashboard
   - Click "Domain Registration" in the left sidebar
   - Or go directly to [https://dash.cloudflare.com/domains](https://dash.cloudflare.com/domains)

2. **Search for Your Domain:**
   - Enter your desired domain name in the search box
   - Click "Search"
   - Example: `my-fastapi-app`, `myproject`, `mybusiness`

3. **Review Available Options:**
   - Cloudflare will show available domains with different extensions:
     - `.com` - Most popular, professional ($9.77/year typically)
     - `.net` - Alternative to .com ($12.18/year typically)
     - `.org` - For organizations ($10.19/year typically)
     - `.io` - Popular for tech startups ($40+/year)
     - `.dev` - For developer projects ($12+/year)
     - And many others...

   **Tip**: If your preferred .com is taken, try:
   - Adding a prefix: `get`, `try`, `hello`, `my`
   - Adding a suffix: `app`, `api`, `hub`, `io`
   - Different extension: `.dev`, `.tech`, `.app`

4. **Select Your Domain:**
   - Click "Purchase" next to your chosen domain
   - Review the domain name carefully (you can't change it after purchase)

5. **Configure Auto-Renewal:**
   - **Recommended**: Keep auto-renewal ON to prevent losing your domain
   - You can always cancel later if needed

6. **Review and Confirm:**
   - Review your order
   - Annual price will be displayed
   - Click "Complete Purchase"

7. **Enter Payment Information:**
   - Add credit card details
   - Cloudflare accepts major credit cards
   - Click "Confirm Payment"

8. **Registration Complete:**
   - You'll receive a confirmation email
   - Your domain typically becomes active within a few minutes
   - You'll see it listed in your Cloudflare dashboard under "Websites"

### Step 3: Initial Domain Configuration

After purchasing, Cloudflare automatically creates a DNS zone for your domain.

1. **Access Your Domain:**
   - Click on your domain name in the Cloudflare dashboard
   - You'll see the domain overview page

2. **Verify Nameservers:**
   - Since you purchased through Cloudflare, nameservers are already configured correctly
   - You should see "Status: Active" at the top
   - If you see "Status: Pending", wait 5-10 minutes and refresh

3. **Review Default DNS Records:**
   - Click on "DNS" in the left menu
   - Cloudflare may have added some default records
   - You can delete any you don't need (you'll add your own later)

### Step 4: Understanding Cloudflare Proxy Settings

**Important for Let's Encrypt SSL Certificates:**

Cloudflare offers two proxy modes for DNS records:

1. **Proxied (Orange Cloud ☁️)**: 
   - Traffic goes through Cloudflare's network
   - Cloudflare provides its own SSL certificate
   - Additional features: CDN, DDoS protection, caching
   - **Problem**: Can interfere with Let's Encrypt validation
   - **Use when**: You want Cloudflare's protection features (after initial setup)

2. **DNS Only (Gray Cloud ☁️)**:
   - Direct connection to your server
   - Your server's SSL certificate is used
   - **Required**: For Let's Encrypt certificate validation
   - **Use when**: Initial setup, Let's Encrypt SSL setup

**Recommended Workflow:**
1. Use "DNS Only" (gray cloud) during initial setup
2. Let Traefik obtain Let's Encrypt certificates successfully
3. Optionally switch to "Proxied" (orange cloud) later for additional features

### Step 5: WHOIS Privacy and Domain Information

**WHOIS Privacy (Included Free with Cloudflare):**

When you register a domain, your personal information (name, email, address) is normally public in the WHOIS database. Cloudflare automatically enables privacy protection.

**To verify privacy protection:**
1. Go to your domain in Cloudflare dashboard
2. Click "Configuration" in the left menu
3. Scroll to "Domain Registration Data"
4. Ensure "Privacy" is toggled ON

**Check your WHOIS information:**
- Use [https://whois.domaintools.com/](https://whois.domaintools.com/)
- Enter your domain
- You should see Cloudflare's proxy information instead of your personal details

### Step 6: Domain Management Best Practices

**Security Settings:**

1. **Enable Two-Factor Authentication (2FA):**
   - Click your profile icon (top right)
   - Go to "My Profile" > "Authentication"
   - Enable 2FA using authenticator app or security key
   - **Critical**: Prevents unauthorized access to your domain

2. **Lock Domain Transfer:**
   - In your domain settings
   - Ensure "Transfer Lock" is enabled
   - Prevents someone from transferring your domain away

3. **Set Strong Email Password:**
   - Ensure the email associated with your Cloudflare account is secure
   - Use a unique, strong password
   - Enable 2FA on your email account too

**Email Forwarding (Optional):**

If you want professional email addresses (like `hello@yourdomain.com`):

1. Cloudflare offers Email Routing (free):
   - Go to "Email" in your domain dashboard
   - Click "Get started"
   - Add destination email addresses
   - Create email routes (e.g., `support@yourdomain.com` → `your.email@gmail.com`)

2. Alternatives:
   - Google Workspace (paid, professional)
   - Microsoft 365 (paid, professional)
   - Mailgun (for transactional emails)

### Step 7: Complete Cloudflare Zone Setup (Recommended Steps)

After purchasing your domain through Cloudflare, you'll see recommended steps to complete your zone setup. Here's what each one means and how to configure them:

#### Recommendation 1: Add DNS Record for www Subdomain

**What it means:**
Make `www.yourdomain.com` accessible alongside `yourdomain.com`

**How to configure:**

1. **Go to DNS settings** in Cloudflare dashboard
2. **Click "Add record"**
3. **Configure the CNAME record:**
   ```
   Type: CNAME
   Name: www
   Target: @ (or yourdomain.com)
   Proxy status: Gray Cloud (DNS only) - for initial setup
   TTL: Auto
   ```
4. **Click "Save"**

**Result:** Both `www.yourdomain.com` and `yourdomain.com` will work

#### Recommendation 2: Add DNS Record for Root Domain

**What it means:**
Make your main domain `yourdomain.com` point to your server

**How to configure:**

1. **Go to DNS settings** in Cloudflare dashboard
2. **Click "Add record"**
3. **Configure the A record:**
   ```
   Type: A
   Name: @ (this represents your root domain)
   IPv4 address: YOUR_EC2_ELASTIC_IP (e.g., 54.123.45.67)
   Proxy status: Gray Cloud (DNS only) - IMPORTANT for Let's Encrypt
   TTL: Auto
   ```
4. **Click "Save"**

**Result:** `yourdomain.com` will point to your EC2 server

**Important:** This is the SAME A record you'll create in the "Configuring DNS" section. You only need to do this once.

#### Recommendation 3: Add MX Record for Email

**What it means:**
Configure email handling for `@yourdomain.com` addresses

**You have two options:**

**Option A: Set up email forwarding (Recommended - Free)**

If you want to receive emails at `hello@yourdomain.com` but forward them to your personal email:

1. **In Cloudflare dashboard, go to "Email" tab**
2. **Click "Get started" on Email Routing**
3. **Add destination email:**
   - Enter your personal email (e.g., `yourname@gmail.com`)
   - Verify it by clicking the link sent to that email
4. **Create email routes:**
   - Click "Create address"
   - Custom address: `hello` (or `admin`, `support`, etc.)
   - Action: Forward to `yourname@gmail.com`
   - Click "Save"
5. **MX records added automatically** by Cloudflare

**Result:** Emails sent to `hello@yourdomain.com` will be forwarded to your personal email

**Option B: Prevent email spoofing (If you DON'T want to receive email)**

If you don't plan to receive emails at `@yourdomain.com`, you should add records to prevent spammers from spoofing your domain:

1. **Add SPF record:**
   ```
   Type: TXT
   Name: @
   Content: v=spf1 -all
   TTL: Auto
   ```
   This tells email servers that NO servers are authorized to send email from your domain.

2. **Add DMARC record:**
   ```
   Type: TXT
   Name: _dmarc
   Content: v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s;
   TTL: Auto
   ```
   This tells email servers to reject any emails claiming to be from your domain.

3. **Add DKIM record (optional):**
   ```
   Type: TXT
   Name: *._domainkey
   Content: v=DKIM1; p=
   TTL: Auto
   ```
   This indicates no DKIM keys are published.

**Result:** Spammers cannot send fake emails pretending to be from your domain

#### After Completing These Steps

Once you've completed the recommendations:

1. **The warnings in Cloudflare will disappear**
2. **Your DNS zone will be fully configured**
3. **You can proceed with the rest of the deployment**

**Important Notes:**

- **You can skip email configuration initially** and set it up later
- **Focus first on:** Root domain A record and www CNAME
- **Email setup is optional** unless you need it for your application
- **These are recommendations, not requirements** for your application to work

**Your minimum required DNS records for the deployment:**

```
Type: A
Name: @
Content: YOUR_EC2_IP
Proxy: Gray Cloud (initially)

Type: A
Name: *
Content: YOUR_EC2_IP
Proxy: Gray Cloud (initially)

Type: CNAME (optional but recommended)
Name: www
Target: @
Proxy: Gray Cloud (initially)
```

These records will make your application accessible at:
- `yourdomain.com`
- `www.yourdomain.com`
- `api.yourdomain.com`
- `dashboard.yourdomain.com`
- `traefik.yourdomain.com`
- `adminer.yourdomain.com`
- Any other subdomain you configure

You can always come back to configure email later!

### Step 8: What's Next?

**After purchasing your domain:**

1. ✅ Domain is registered and active
2. ✅ Cloudflare is managing DNS
3. ✅ Privacy protection is enabled
4. ⏭️ Next: Set up your EC2 server (next section)
5. ⏭️ Then: Configure DNS records to point to your server
6. ⏭️ Finally: Deploy your application with HTTPS

**Important Notes:**

- **Domain Activation**: Usually instant, but can take up to 24 hours
- **First Payment**: Charged immediately for first year
- **Renewal**: Automatic yearly renewal (you'll get reminders)
- **Cancellation**: Can cancel anytime, but no refunds for partial years
- **Transfer Out**: Can transfer to another registrar after 60 days (ICANN rule)

**Costs to Remember:**

- Domain registration: $8-15/year (varies by extension)
- Renewal: Same price (Cloudflare doesn't increase renewal costs)
- DNS management: Free
- Basic features: Free
- Optional services: Paid plans available ($20-200/month) but NOT required

**Save These Details:**

Write down or save securely:
- ✍️ Domain name: `_________________`
- ✍️ Cloudflare account email: `_________________`
- ✍️ Purchase date: `_________________`
- ✍️ Renewal date: `_________________`

---

## Setting Up AWS EC2

This section provides complete, step-by-step instructions for creating an AWS account and launching an EC2 instance, even if you've never used AWS before.

### Step 1: Create an AWS Account

1. **Go to AWS website:**
   - Visit [https://aws.amazon.com](https://aws.amazon.com)
   - Click "Create an AWS Account" (orange button in top right)

2. **Enter your information:**
   - **Email address**: Use a valid email you have access to
   - **Password**: Choose a strong password (save it in a password manager!)
   - **AWS account name**: Can be your name or company name

3. **Contact Information:**
   - Select account type: "Personal" or "Professional"
   - Enter your full name
   - Phone number (will be used for verification)
   - Address (must be accurate)

4. **Payment Information:**
   - Enter credit/debit card details
   - AWS will charge $1 temporarily for verification (refunded)
   - **Note**: AWS Free Tier includes 750 hours/month of t2.micro instances for 12 months

5. **Identity Verification:**
   - Choose phone call or SMS verification
   - Enter the verification code you receive

6. **Select Support Plan:**
   - Choose "Basic support - Free" (sufficient for getting started)

7. **Account Activation:**
   - Wait 5-10 minutes for account activation
   - Check your email for confirmation

### Step 2: Sign in to AWS Console

1. Go to [https://console.aws.amazon.com](https://console.aws.amazon.com)
2. Enter your email and password
3. You'll see the AWS Management Console homepage

### Step 3: Launch an EC2 Instance

**What is EC2?**
Elastic Compute Cloud (EC2) is AWS's virtual server service. You're essentially renting a computer in AWS's data center that you can access remotely.

**Steps to launch:**

1. **Navigate to EC2:**
   - In the AWS Console, type "EC2" in the search bar at the top
   - Click "EC2" under Services
   - You'll see the EC2 Dashboard

2. **Launch Instance:**
   - Click the orange "Launch Instance" button
   - You'll be taken to the instance configuration page

3. **Configure Instance - Name and Tags:**
   - **Name**: Enter a descriptive name (e.g., "fastapi-production")
   - Tags help organize resources, especially if you'll have multiple instances

4. **Choose an Amazon Machine Image (AMI):**
   - Select "Ubuntu Server 24.04 LTS" (or latest LTS version)
   - **Why Ubuntu?**: Stable, well-documented, great for Docker
   - Make sure it says "Free tier eligible" if you want to use free tier
   - Click "64-bit (x86)" architecture

5. **Choose Instance Type:**
   - **For testing/small projects**: Select `t2.micro` (Free tier eligible, 1 vCPU, 1 GB RAM)
   - **For small production**: Select `t2.small` (1 vCPU, 2 GB RAM)
   - **For medium production**: Select `t2.medium` (2 vCPU, 4 GB RAM)
   - **For larger production**: Select `t2.large` or higher
   
   **Cost consideration**: Only t2.micro is free tier eligible. Check current pricing at [https://aws.amazon.com/ec2/pricing/](https://aws.amazon.com/ec2/pricing/)

6. **Configure Key Pair (Login):**
   - Click "Create new key pair"
   - **Key pair name**: Enter a name (e.g., "fastapi-key")
   - **Key pair type**: Select "RSA"
   - **Private key file format**: 
     - Select ".pem" for Mac/Linux
     - Select ".ppk" for Windows (if using PuTTY)
     - **Recommended**: Use ".pem" (works with modern Windows too)
   - Click "Create key pair"
   - **IMPORTANT**: The .pem file will download automatically - save it securely! You can't download it again.
   - **Security**: This file is like your password - keep it safe and never share it

7. **Network Settings:**
   - **Firewall (security groups)**: Click "Create security group"
   - **Security group name**: Enter a name (e.g., "fastapi-security-group")
   - **Description**: Enter a description (e.g., "Security group for FastAPI application")
   
   **Configure Security Group Rules:**
   You need to allow specific types of traffic to reach your server:
   
   - **SSH (Port 22)**: Already added by default
     - **Type**: SSH
     - **Port**: 22
     - **Source**: "My IP" (more secure) or "Anywhere" (0.0.0.0/0) if you need access from multiple locations
     - **Why**: Required to connect to your server via terminal
   
   - **HTTP (Port 80)**: Click "Add security group rule"
     - **Type**: HTTP
     - **Port**: 80
     - **Source**: Anywhere (0.0.0.0/0)
     - **Why**: Required for initial Let's Encrypt certificate validation
   
   - **HTTPS (Port 443)**: Click "Add security group rule"
     - **Type**: HTTPS
     - **Port**: 443
     - **Source**: Anywhere (0.0.0.0/0)
     - **Why**: Required for secure HTTPS traffic to your application

8. **Configure Storage:**
   - **Default**: 8 GB General Purpose SSD (gp3)
   - **Recommended for production**: 20-30 GB minimum
   - **Type**: Keep gp3 (General Purpose SSD) - good balance of performance and cost
   - **Note**: You can change the size (GB) but more storage = more cost

9. **Advanced Details** (Optional but recommended):
   - Scroll down to "Advanced details"
   - Find "User data" section
   - You can add a startup script here, but we'll configure manually instead

10. **Review and Launch:**
    - On the right side, review the "Summary" panel
    - Check your instance type, storage, and security groups
    - Click the orange "Launch instance" button

11. **Wait for Instance to Start:**
    - You'll see a success message
    - Click "View all instances"
    - Your instance will show "Instance state: Running" (takes 1-2 minutes)
    - Wait until "Status check" shows "2/2 checks passed"

### Step 4: Connect to Your EC2 Instance

1. **Get Connection Information:**
   - In EC2 Dashboard, click on your instance ID
   - Find "Public IPv4 address" (e.g., 54.123.45.67) - **write this down!**
   - Find "Public IPv4 DNS" (e.g., ec2-54-123-45-67.compute-1.amazonaws.com)

2. **Prepare Your SSH Key:**
   
   **On Linux/Mac/Windows (with WSL):**
   ```bash
   # Move the key to a safe location
   mkdir -p ~/.ssh
   mv ~/Downloads/fastapi-key.pem ~/.ssh/
   
   # Set correct permissions (required for SSH)
   chmod 400 ~/.ssh/fastapi-key.pem
   ```

   **On Windows (using PowerShell):**
   ```powershell
   # Move the key to a safe location
   mkdir $HOME\.ssh -Force
   Move-Item $HOME\Downloads\fastapi-key.pem $HOME\.ssh\
   
   # Set correct permissions
   icacls "$HOME\.ssh\fastapi-key.pem" /inheritance:r
   icacls "$HOME\.ssh\fastapi-key.pem" /grant:r "$($env:USERNAME):(R)"
   ```

3. **Connect via SSH:**
   
   **Using Terminal (Linux/Mac/WSL/Windows):**
   ```bash
   # Replace with your actual IP address and key name
   ssh -i ~/.ssh/fastapi-key.pem ubuntu@54.123.45.67
   ```
   
   - If you get a warning about host authenticity, type "yes" and press Enter
   - You should now see a welcome message and Ubuntu prompt: `ubuntu@ip-xxx-xxx-xxx-xxx:~$`

   **Using PuTTY (Windows alternative):**
   - Download PuTTY from [https://www.putty.org/](https://www.putty.org/)
   - Convert .pem to .ppk using PuTTYgen (included with PuTTY)
   - In PuTTY:
     - Host Name: ubuntu@54.123.45.67
     - Port: 22
     - Connection > SSH > Auth: Browse for your .ppk file
     - Click "Open"

4. **Update the System:**
   Once connected, run these commands:
   ```bash
   # Update package list
   sudo apt update
   
   # Upgrade installed packages
   sudo apt upgrade -y
   ```

**Congratulations! You now have a running EC2 instance that you can access remotely!**

### Step 5: Understanding EC2 Environment Variables

Environment variables in EC2 work the same as on any Linux system. There are several ways to manage them:

**Method 1: Temporary Export (Session-only)**
```bash
# Variables set this way only last until you log out
export DOMAIN=fastapi-project.example.com
export SECRET_KEY=your-secret-key
```

**Method 2: Add to .bashrc (Persistent for user)**
```bash
# Edit the .bashrc file
nano ~/.bashrc

# Add your variables at the end:
export DOMAIN=fastapi-project.example.com
export SECRET_KEY=your-secret-key
export POSTGRES_PASSWORD=your-db-password

# Save and exit (Ctrl+X, Y, Enter)

# Reload the configuration
source ~/.bashrc
```

**Method 3: Create a .env file (Recommended for this project)**
```bash
# Create a directory for your project
mkdir -p ~/fastapi-project
cd ~/fastapi-project

# Create an .env file
nano .env

# Add your variables (no 'export' keyword needed):
DOMAIN=fastapi-project.example.com
ENVIRONMENT=production
SECRET_KEY=your-secret-key-here
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=changethis
POSTGRES_PASSWORD=super-secret-password
POSTGRES_USER=app
POSTGRES_DB=app

# Save and exit (Ctrl+X, Y, Enter)

# Make the file secure (only you can read it)
chmod 600 .env

# To load variables from .env file:
set -a
source .env
set +a
```

**Method 4: Docker Compose env_file (Best for production)**
Docker Compose can automatically load environment variables from a file:

```yaml
# In your docker-compose.yml
services:
  backend:
    env_file:
      - .env
```

**Security Best Practices:**
1. **Never commit .env files to Git**: Add `.env` to your `.gitignore`
2. **Use strong, unique passwords**: Generate with `openssl rand -base64 32`
3. **Restrict file permissions**: Use `chmod 600 .env`
4. **Use AWS Secrets Manager for sensitive data** (advanced): AWS service for managing secrets

**AWS-Specific Environment Variable Management:**

For more advanced setups, you can use:

1. **AWS Systems Manager Parameter Store:**
   - Store variables in AWS
   - Retrieve them in your application
   - Free for standard parameters

2. **AWS Secrets Manager:**
   - More features than Parameter Store
   - Automatic rotation
   - Small cost involved

---

## Configuring DNS

Now that your EC2 instance is running, you need to point your domain to it. If you purchased your domain through Cloudflare (as recommended in the earlier section), the process is straightforward.

### Prerequisites

Before configuring DNS:
- ✅ You have a registered domain name
- ✅ Your EC2 instance is running
- ✅ You have the public IP address of your EC2 instance
- ✅ Ideally, you've allocated an Elastic IP to your instance

### Step 1: Find Your EC2 Public IP

```bash
# From your EC2 Dashboard, copy the "Public IPv4 address"
# Example: 54.123.45.67
```

**Important**: By default, EC2 instances get a dynamic IP that changes when you stop/start the instance.

**To get a static IP (Elastic IP):**
1. In EC2 Dashboard, go to "Network & Security" > "Elastic IPs"
2. Click "Allocate Elastic IP address"
3. Click "Allocate"
4. Select the new Elastic IP
5. Click "Actions" > "Associate Elastic IP address"
6. Select your instance
7. Click "Associate"

**Note**: Elastic IPs are free while associated with a running instance, but cost money if not associated.

### Step 2: Configure DNS Records

You'll now configure DNS records to point your domain to your EC2 server. Instructions are provided for the most common DNS providers.

#### Option A: Using Cloudflare (Recommended - If You Followed the Domain Purchase Section)

If you purchased your domain through Cloudflare, your domain is already using Cloudflare's nameservers and you can configure DNS immediately.

1. **Log in to Cloudflare:**
   - Go to [https://dash.cloudflare.com](https://dash.cloudflare.com)
   - Sign in with your Cloudflare credentials

2. **Select Your Domain:**
   - Click on your domain from the list of websites
   - You'll see the domain overview

3. **Navigate to DNS Settings:**
   - Click "DNS" in the left sidebar menu
   - You'll see the DNS management page

4. **Add Main Domain A Record:**
   - Click "Add record" button
   - Configure the record:
     ```
     Type: A
     Name: @ (this represents your root domain)
     IPv4 address: 54.123.45.67 (your EC2 Elastic IP)
     Proxy status: DNS only (click the orange cloud to turn it gray)
     TTL: Auto
     ```
   - **Critical**: Make sure the cloud is GRAY (DNS only), not orange
   - Click "Save"

5. **Add Wildcard Subdomain A Record:**
   - Click "Add record" button again
   - Configure the record:
     ```
     Type: A
     Name: * (asterisk for wildcard)
     IPv4 address: 54.123.45.67 (your EC2 Elastic IP)
     Proxy status: DNS only (GRAY cloud)
     TTL: Auto
     ```
   - Click "Save"

6. **Optional - Add WWW Subdomain:**
   - If you want `www.yourdomain.com` to work:
   - Click "Add record" button
   - Configure the record:
     ```
     Type: CNAME
     Name: www
     Target: @ (or your full domain: yourdomain.com)
     Proxy status: DNS only (GRAY cloud)
     TTL: Auto
     ```
   - Click "Save"

7. **Verify Your DNS Records:**
   - You should now see at least two A records:
     - `yourdomain.com` → `54.123.45.67` (gray cloud)
     - `*.yourdomain.com` → `54.123.45.67` (gray cloud)

**Why Gray Cloud (DNS Only)?**
- Let's Encrypt needs to verify your domain directly with your server
- Orange cloud (proxied) routes traffic through Cloudflare, which can interfere with verification
- After SSL certificates are set up, you can optionally switch to orange cloud for CDN benefits

**What Each Record Does:**
- **@ (root) record**: Makes `yourdomain.com` point to your server
- **\* (wildcard) record**: Makes all subdomains point to your server:
  - `api.yourdomain.com`
  - `dashboard.yourdomain.com`
  - `adminer.yourdomain.com`
  - Any other subdomain you create

#### Option B: Using Namecheap

1. Log in to your Namecheap account
2. Go to "Domain List"
3. Click "Manage" next to your domain
4. Go to "Advanced DNS" tab
5. Add/Edit records:

   **Main Domain A Record:**
   ```
   Type: A Record
   Host: @
   Value: 54.123.45.67 (your EC2 Elastic IP)
   TTL: Automatic (or 300)
   ```

   **Wildcard Subdomain A Record:**
   ```
   Type: A Record
   Host: *
   Value: 54.123.45.67 (your EC2 Elastic IP)
   TTL: Automatic (or 300)
   ```

   **Optional WWW CNAME:**
   ```
   Type: CNAME Record
   Host: www
   Value: example.com
   TTL: Automatic
   ```

6. Save all records

#### Option C: Using Cloudflare (If Domain Registered Elsewhere)

If your domain is registered with another provider but you want to use Cloudflare for DNS management:

**Step 1: Add Domain to Cloudflare**
1. Log in to Cloudflare
2. Click "Add a site"
3. Enter your domain name
4. Select the Free plan
5. Click "Continue"

**Step 2: Add DNS Records in Cloudflare**
1. Cloudflare will scan existing DNS records
2. Add or modify records:

   **Main Domain A Record:**
   ```
   Type: A
   Name: @
   IPv4 address: 54.123.45.67
   Proxy status: DNS only (gray cloud) - Important for Let's Encrypt!
   TTL: Auto
   ```

   **Wildcard Subdomain A Record:**
   ```
   Type: A
   Name: *
   IPv4 address: 54.123.45.67
   Proxy status: DNS only (gray cloud)
   TTL: Auto
   ```

**Step 3: Update Nameservers at Your Domain Registrar**
1. Cloudflare will provide 2 nameservers (e.g., `alice.ns.cloudflare.com` and `bob.ns.cloudflare.com`)
2. Copy these nameservers
3. Go to your domain registrar (GoDaddy, Namecheap, etc.)
4. Find nameserver settings (usually under DNS or Domain Management)
5. Replace existing nameservers with Cloudflare's nameservers
6. Save changes
7. Return to Cloudflare and click "Done, check nameservers"

**Note**: Nameserver changes can take 24-48 hours to propagate, but usually complete within 1-2 hours.

#### Option D: Using AWS Route 53
#### Option D: Using AWS Route 53

If your domain is registered with AWS or you want to use Route 53 for DNS:

1. Go to Route 53 in AWS Console
2. Click "Hosted zones"
3. Click "Create hosted zone"
4. Enter your domain name
5. Click "Create hosted zone"
6. Create records:

   **Main Domain A Record:**
   - Click "Create record"
   - Leave "Record name" blank (for root domain)
   - Record type: A
   - Value: Your EC2 Elastic IP
   - TTL: 300
   - Click "Create records"

   **Wildcard Subdomain A Record:**
   - Click "Create record"
   - Record name: *
   - Record type: A
   - Value: Your EC2 Elastic IP
   - TTL: 300
   - Click "Create records"

7. **Update nameservers** (if domain is registered elsewhere):
   - Copy the 4 nameserver addresses from Route 53
   - Go to your domain registrar
   - Update nameservers to use AWS nameservers

### Step 3: Verify DNS Configuration

DNS changes can take anywhere from a few minutes to 48 hours to propagate worldwide (usually within 1-2 hours).

**Test your DNS configuration:**

```bash
# From your local computer (not EC2)

# Test main domain
nslookup example.com

# Test subdomain
nslookup api.example.com

# Test wildcard
nslookup random-subdomain.example.com

# Or use dig (more detailed)
dig example.com
dig api.example.com
```

You should see your EC2 IP address in the response.

**Online tools for testing:**
- [https://www.whatsmydns.net/](https://www.whatsmydns.net/) - Check DNS propagation worldwide
- [https://dnschecker.org/](https://dnschecker.org/) - Another DNS propagation checker
- [https://mxtoolbox.com/DNSLookup.aspx](https://mxtoolbox.com/DNSLookup.aspx) - Comprehensive DNS lookup

---

## Installing Docker Engine

Now we'll install Docker Engine on your EC2 Ubuntu instance.

### Step 1: Connect to Your EC2 Instance

```bash
ssh -i ~/.ssh/fastapi-key.pem ubuntu@54.123.45.67
```

### Step 2: Remove Old Docker Versions (if any)

```bash
# Remove old versions
sudo apt-get remove docker docker-engine docker.io containerd runc
```

### Step 3: Install Docker Engine

**Method 1: Using Docker's Official Script (Easiest)**

```bash
# Download and run Docker's installation script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clean up
rm get-docker.sh
```

**Method 2: Manual Installation (More Control)**

```bash
# Update the package index
sudo apt-get update

# Install prerequisites
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package index again
sudo apt-get update

# Install Docker Engine, containerd, and Docker Compose
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Step 4: Verify Docker Installation

```bash
# Check Docker version
docker --version

# Should output something like: Docker version 24.0.7, build afdd53b

# Check Docker Compose version
docker compose version

# Should output something like: Docker Compose version v2.23.0
```

### Step 5: Configure Docker Permissions

By default, Docker requires sudo. Let's allow the ubuntu user to run Docker without sudo:

```bash
# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu

# Apply the group changes (important!)
newgrp docker

# Or, log out and log back in for changes to take effect
exit
# Then reconnect: ssh -i ~/.ssh/fastapi-key.pem ubuntu@54.123.45.67
```

### Step 6: Test Docker Installation

```bash
# Run a test container (without sudo)
docker run hello-world

# You should see: "Hello from Docker!"
```

### Step 7: Configure Docker to Start on Boot

```bash
# Enable Docker service to start on boot
sudo systemctl enable docker

# Check Docker service status
sudo systemctl status docker
```

### Step 8: Verify Everything is Working

```bash
# Check Docker info
docker info

# List running containers (should be empty for now)
docker ps

# List all containers (including stopped ones)
docker ps -a

# You should see the hello-world container
```

**Optional: Configure Docker Storage and Logging**

For production, you might want to configure Docker's storage driver and logging:

```bash
# Create Docker daemon configuration
sudo nano /etc/docker/daemon.json

# Add this content:
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2"
}

# Save and exit (Ctrl+X, Y, Enter)

# Restart Docker to apply changes
sudo systemctl restart docker
```

This configuration:
- Limits log file size to 10MB per container
- Keeps only the 3 most recent log files
- Uses the overlay2 storage driver (recommended for modern systems)

---

## Setting Up Traefik

Traefik will act as the reverse proxy and handle HTTPS certificates automatically.

### Step 1: Create Traefik Directory

```bash
# Create directory for Traefik
mkdir -p ~/traefik-public
cd ~/traefik-public
```

### Step 2: Get the Traefik Docker Compose File

You need to transfer the `docker-compose.traefik.yml` file from your local project to the EC2 instance.

**Option 1: Using SCP (from your local machine)**

```bash
# From your local machine (not EC2)
scp -i ~/.ssh/fastapi-key.pem \
    docker-compose.traefik.yml \
    ubuntu@54.123.45.67:~/traefik-public/
```

**Option 2: Using rsync (recommended)**

```bash
# From your local machine (not EC2)
rsync -avz -e "ssh -i ~/.ssh/fastapi-key.pem" \
    docker-compose.traefik.yml \
    ubuntu@54.123.45.67:~/traefik-public/
```

**Option 3: Copy-paste content**

If the above don't work, you can manually create the file:

```bash
# On EC2 instance
cd ~/traefik-public
nano docker-compose.traefik.yml

# Copy the content from your local docker-compose.traefik.yml file
# Paste it into nano
# Save and exit (Ctrl+X, Y, Enter)
```

### Step 3: Create Traefik Docker Network

```bash
# Create the public network that Traefik and your app will use
docker network create traefik-public

# Verify it was created
docker network ls | grep traefik-public
```

### Step 4: Set Traefik Environment Variables

```bash
# Set username for Traefik dashboard
export USERNAME=admin

# Set password for Traefik dashboard
export PASSWORD=your-secure-password-here

# Generate hashed password (required by Traefik)
export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)

# Verify hashed password was created
echo $HASHED_PASSWORD

# Set your domain
export DOMAIN=fastapi-project.example.com

# Set your email for Let's Encrypt
export EMAIL=your-email@example.com
```

**Important**: Replace `your-email@example.com` with a real email address. Let's Encrypt will send expiration notices here (though Traefik auto-renews).

**Make variables persistent** (optional but recommended):

```bash
# Add to .bashrc so they persist across sessions
cat >> ~/.bashrc << 'EOF'

# Traefik Configuration
export USERNAME=admin
export PASSWORD=your-secure-password-here
export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)
export DOMAIN=fastapi-project.example.com
export EMAIL=your-email@example.com
EOF

# Reload .bashrc
source ~/.bashrc
```

### Step 5: Start Traefik

```bash
# Make sure you're in the traefik-public directory
cd ~/traefik-public

# Start Traefik
docker compose -f docker-compose.traefik.yml up -d

# Check if Traefik is running
docker ps

# You should see a container named traefik-traefik-1 or similar
```

### Step 6: Check Traefik Logs

```bash
# View Traefik logs
docker compose -f docker-compose.traefik.yml logs

# Follow logs in real-time
docker compose -f docker-compose.traefik.yml logs -f

# Press Ctrl+C to stop following logs
```

### Step 7: Verify Traefik Dashboard

Once your DNS has propagated (wait 10-30 minutes after setting DNS), you can access the Traefik dashboard:

```
https://traefik.fastapi-project.example.com
```

Replace `fastapi-project.example.com` with your actual domain.

- **Username**: The username you set (default: admin)
- **Password**: The password you set

**Troubleshooting Traefik:**

If you can't access the dashboard:

1. **Check DNS propagation:**
   ```bash
   # From your local machine
   nslookup traefik.fastapi-project.example.com
   ```

2. **Check Traefik logs:**
   ```bash
   docker compose -f docker-compose.traefik.yml logs traefik
   ```

3. **Check if Traefik is running:**
   ```bash
   docker ps | grep traefik
   ```

4. **Check security groups:**
   - Make sure ports 80 and 443 are open in your EC2 security group

5. **Check Let's Encrypt rate limits:**
   - Let's Encrypt has rate limits (5 certificates per domain per week)
   - Check [https://letsencrypt.org/docs/rate-limits/](https://letsencrypt.org/docs/rate-limits/)

---

## Deploying the Application

Now we'll deploy your FastAPI application.

### Step 1: Transfer Your Project Files

**Option 1: Using Git (Recommended)**

If your project is in a Git repository:

```bash
# On EC2 instance
cd ~

# Clone your repository
git clone https://github.com/yourusername/your-repo.git fastapi-project

# Navigate to project directory
cd fastapi-project
```

**Option 2: Using SCP**

If you want to transfer files directly:

```bash
# From your local machine, in your project directory
# Compress your project
tar -czf project.tar.gz \
    --exclude=node_modules \
    --exclude=__pycache__ \
    --exclude=.git \
    --exclude=*.pyc \
    --exclude=venv \
    .

# Transfer to EC2
scp -i ~/.ssh/fastapi-key.pem project.tar.gz ubuntu@54.123.45.67:~/

# On EC2, extract
ssh -i ~/.ssh/fastapi-key.pem ubuntu@54.123.45.67
cd ~
mkdir -p fastapi-project
tar -xzf project.tar.gz -C fastapi-project
cd fastapi-project
```

**Option 3: Using rsync (Best for updates)**

```bash
# From your local machine
rsync -avz -e "ssh -i ~/.ssh/fastapi-key.pem" \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='*.pyc' \
    --exclude='venv' \
    --exclude='.env' \
    ./ ubuntu@54.123.45.67:~/fastapi-project/
```

### Step 2: Create Environment Variables File

```bash
# On EC2, in your project directory
cd ~/fastapi-project

# Create .env file
nano .env
```

Add your environment variables (replace values with your own):

```bash
# Application Environment
ENVIRONMENT=production
DOMAIN=fastapi-project.example.com

# Stack Configuration
STACK_NAME=fastapi-project-example-com
PROJECT_NAME="FastAPI Project"

# Security
SECRET_KEY=generate-a-secure-key-here-use-python-secrets-token-urlsafe-32
BACKEND_CORS_ORIGINS=["https://dashboard.fastapi-project.example.com"]

# First Superuser
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=change-this-to-a-secure-password

# Email Configuration (optional, can be configured later)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAILS_FROM_EMAIL=noreply@fastapi-project.example.com

# Database Configuration
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_USER=app
POSTGRES_PASSWORD=generate-a-secure-postgres-password
POSTGRES_DB=app

# Sentry (optional, for error tracking)
# SENTRY_DSN=your-sentry-dsn-here
```

Save and exit (Ctrl+X, Y, Enter)

**Generate Secure Keys:**

```bash
# Generate SECRET_KEY
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"

# Generate POSTGRES_PASSWORD
python3 -c "import secrets; print('POSTGRES_PASSWORD=' + secrets.token_urlsafe(32))"

# Copy these values into your .env file
```

**Secure your .env file:**

```bash
chmod 600 .env
```

### Step 3: Load Environment Variables

```bash
# Load variables from .env
set -a
source .env
set +a

# Verify variables are loaded
echo $DOMAIN
echo $ENVIRONMENT
```

### Step 4: Build and Start the Application

```bash
# Make sure you're in the project directory
cd ~/fastapi-project

# Pull/build images and start containers
docker compose -f docker-compose.yml up -d

# This will:
# 1. Pull necessary images (PostgreSQL, etc.)
# 2. Build your application images
# 3. Start all containers
```

**Note**: The first time you run this, it will take several minutes to:
- Download base images
- Build your backend and frontend
- Start all services

### Step 5: Monitor the Deployment

```bash
# Watch logs from all services
docker compose logs -f

# Watch logs from specific service
docker compose logs -f backend
docker compose logs -f frontend

# Press Ctrl+C to stop watching
```

### Step 6: Check Running Containers

```bash
# List running containers
docker compose ps

# You should see containers for:
# - backend
# - frontend
# - db (PostgreSQL)
# And possibly others depending on your configuration
```

### Step 7: Verify Database Initialization

```bash
# Check backend logs for database initialization
docker compose logs backend | grep -i "database\|migration"

# Run database migrations (if not automatic)
docker compose exec backend alembic upgrade head

# Check if first superuser was created
docker compose logs backend | grep -i "superuser"
```

### Step 8: Test Your Deployment

Once everything is running and DNS has propagated, test your application:

1. **Backend API Docs:**
   ```
   https://api.fastapi-project.example.com/docs
   ```

2. **Frontend Dashboard:**
   ```
   https://dashboard.fastapi-project.example.com
   ```

3. **Adminer (Database Management):**
   ```
   https://adminer.fastapi-project.example.com
   ```

4. **Traefik Dashboard:**
   ```
   https://traefik.fastapi-project.example.com
   ```

### Step 9: Troubleshooting Deployment Issues

**If containers aren't starting:**

```bash
# Check container status
docker compose ps

# View logs for failed containers
docker compose logs backend
docker compose logs frontend
docker compose logs db

# Check for port conflicts
sudo netstat -tulpn | grep LISTEN

# Restart a specific service
docker compose restart backend

# Rebuild and restart everything
docker compose down
docker compose up -d --build
```

**If you can't access the application:**

1. **Check DNS:**
   ```bash
   nslookup api.fastapi-project.example.com
   ```

2. **Check Traefik routing:**
   - Go to Traefik dashboard
   - Look for HTTP routers and services
   - Verify your application is listed

3. **Check container health:**
   ```bash
   docker compose ps
   docker compose logs
   ```

4. **Check environment variables:**
   ```bash
   docker compose exec backend env | grep DOMAIN
   ```

5. **Check EC2 security groups:**
   - Ensure ports 80 and 443 are open

**Common issues:**

1. **Let's Encrypt certificate errors:**
   - Wait a few minutes, Let's Encrypt validation takes time
   - Check DNS is properly configured
   - Check Traefik logs: `docker compose -f ~/traefik-public/docker-compose.traefik.yml logs`

2. **Database connection errors:**
   - Check PostgreSQL is running: `docker compose ps db`
   - Check database logs: `docker compose logs db`
   - Verify POSTGRES_PASSWORD in .env

3. **502 Bad Gateway:**
   - Backend container might be crashing
   - Check backend logs: `docker compose logs backend`
   - Check backend health: `docker compose ps backend`

---

## Continuous Deployment

Set up automated deployments with GitHub Actions.

### Understanding Continuous Deployment

**What is CI/CD?**
- **Continuous Integration (CI)**: Automatically testing code when you push changes
- **Continuous Deployment (CD)**: Automatically deploying code to your server after tests pass

**How it works:**
1. You push code to GitHub
2. GitHub Actions runs tests
3. If tests pass, GitHub Actions connects to your EC2 instance
4. It pulls the latest code and restarts your containers
5. Your application is updated automatically

### Step 1: Install GitHub Actions Runner on EC2

**Create a user for GitHub Actions:**

```bash
# On EC2 instance
sudo adduser github

# Add Docker permissions
sudo usermod -aG docker github

# Switch to github user
sudo su - github
cd ~
```

**Download and configure GitHub Actions Runner:**

1. Go to your GitHub repository
2. Click "Settings" > "Actions" > "Runners"
3. Click "New self-hosted runner"
4. Select "Linux"
5. Copy the download commands and run them on EC2:

```bash
# Still as github user
mkdir actions-runner && cd actions-runner

# Download (replace URL with one from GitHub)
curl -o actions-runner-linux-x64-2.311.0.tar.gz \
    -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extract
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz
```

**Configure the runner:**

```bash
# Run configuration (follow the prompts)
./config.sh --url https://github.com/yourusername/your-repo --token YOUR_TOKEN

# When prompted:
# - Enter runner name: production (or staging)
# - Enter labels: production (or staging)
# - Enter work folder: _work
```

**Install as a service:**

```bash
# Exit back to root user
exit
sudo su

# Go to actions-runner directory
cd /home/github/actions-runner

# Install service
./svc.sh install github

# Start service
./svc.sh start

# Check status
./svc.sh status

# Enable on boot
systemctl enable actions.runner.*
```

### Step 2: Set GitHub Secrets

Your GitHub Actions workflows need access to sensitive information. Store this in GitHub Secrets:

1. Go to your repository on GitHub
2. Click "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Add these secrets:

**Required Secrets:**

```
SECRET_KEY
    Value: (the secret key you generated earlier)

FIRST_SUPERUSER
    Value: admin@example.com

FIRST_SUPERUSER_PASSWORD
    Value: (your superuser password)

POSTGRES_PASSWORD
    Value: (your PostgreSQL password)

EMAILS_FROM_EMAIL
    Value: noreply@example.com

DOMAIN_PRODUCTION
    Value: fastapi-project.example.com

DOMAIN_STAGING
    Value: staging.fastapi-project.example.com

STACK_NAME_PRODUCTION
    Value: fastapi-project-example-com

STACK_NAME_STAGING
    Value: staging-fastapi-project-example-com
```

**Optional Secrets for advanced features:**

```
SMTP_HOST
    Value: smtp.gmail.com

SMTP_USER
    Value: your-email@gmail.com

SMTP_PASSWORD
    Value: your-app-password

SENTRY_DSN
    Value: your-sentry-dsn

LATEST_CHANGES
    Value: (GitHub token for release notes)

SMOKESHOW_AUTH_KEY
    Value: (Smokeshow key for code coverage)
```

### Step 3: Understand GitHub Actions Workflows

Your project already has workflows in `.github/workflows/`. These workflows:

**Staging Deployment** (`.github/workflows/deploy-staging.yml`):
- Triggers on push to `master` branch
- Runs tests
- Deploys to staging server
- Uses `staging` runner label

**Production Deployment** (`.github/workflows/deploy-production.yml`):
- Triggers when you create a GitHub Release
- Runs tests
- Deploys to production server
- Uses `production` runner label

### Step 4: Test Automated Deployment

**Deploy to Staging:**

```bash
# On your local machine
git add .
git commit -m "Test deployment"
git push origin master

# Watch the deployment:
# 1. Go to your repository on GitHub
# 2. Click "Actions" tab
# 3. You'll see your workflow running
# 4. Click on it to see progress
```

**Deploy to Production:**

1. Go to your repository on GitHub
2. Click "Releases" (right sidebar)
3. Click "Create a new release"
4. Click "Choose a tag" > Create new tag (e.g., `v1.0.0`)
5. Fill in release title and description
6. Click "Publish release"
7. Go to "Actions" tab to watch the deployment

### Step 5: Set Up Multiple Environments (Optional)

If you want both staging and production:

**On EC2, set up staging:**

```bash
# Create staging directory
mkdir -p ~/fastapi-project-staging
cd ~/fastapi-project-staging

# Create staging .env file
nano .env

# Use staging domain and different database
ENVIRONMENT=staging
DOMAIN=staging.fastapi-project.example.com
STACK_NAME=staging-fastapi-project-example-com
POSTGRES_DB=app_staging
# ... other variables
```

**Update your docker-compose for different stack names:**

```bash
# Deploy staging
cd ~/fastapi-project-staging
export ENVIRONMENT=staging
export DOMAIN=staging.fastapi-project.example.com
docker compose -p staging-fastapi-project up -d
```

---

## URLs and Access

After deployment, your application will be available at these URLs (replace `fastapi-project.example.com` with your domain):

### Production Environment

- **Frontend Dashboard**: https://dashboard.fastapi-project.example.com
- **Backend API Documentation**: https://api.fastapi-project.example.com/docs
- **Backend API Base URL**: https://api.fastapi-project.example.com
- **Database Admin (Adminer)**: https://adminer.fastapi-project.example.com
- **Traefik Dashboard**: https://traefik.fastapi-project.example.com

### Staging Environment

- **Frontend Dashboard**: https://dashboard.staging.fastapi-project.example.com
- **Backend API Documentation**: https://api.staging.fastapi-project.example.com/docs
- **Backend API Base URL**: https://api.staging.fastapi-project.example.com
- **Database Admin (Adminer)**: https://adminer.staging.fastapi-project.example.com

---

## Maintenance and Management

### Viewing Logs

```bash
# View all logs
docker compose logs

# Follow logs in real-time
docker compose logs -f

# View logs for specific service
docker compose logs backend
docker compose logs frontend
docker compose logs db

# View last 100 lines
docker compose logs --tail=100

# View logs with timestamps
docker compose logs -t
```

### Updating Your Application

```bash
# Pull latest code (if using Git)
cd ~/fastapi-project
git pull origin master

# Rebuild and restart
docker compose down
docker compose up -d --build

# Or, without downtime (rolling update)
docker compose up -d --build --no-deps backend
docker compose up -d --build --no-deps frontend
```

### Database Backups

```bash
# Create backup
docker compose exec db pg_dump -U app app > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
docker compose exec -T db psql -U app app < backup_20240115_120000.sql

# Automated daily backups (add to crontab)
crontab -e
# Add this line:
0 2 * * * cd ~/fastapi-project && docker compose exec db pg_dump -U app app > ~/backups/backup_$(date +\%Y\%m\%d).sql
```

### Monitoring Disk Space

```bash
# Check disk space
df -h

# Check Docker disk usage
docker system df

# Clean up unused Docker resources
docker system prune -a

# Clean up volumes (careful!)
docker volume prune
```

### Updating Docker Images

```bash
# Pull latest images
docker compose pull

# Restart with new images
docker compose up -d
```

### SSL Certificate Renewal

Traefik automatically renews Let's Encrypt certificates. But you can check:

```bash
# Check Traefik logs for certificate info
docker compose -f ~/traefik-public/docker-compose.traefik.yml logs | grep -i certificate

# Certificates are stored in
# ~/traefik-public/traefik-public-certificates/
```

---

## Security Best Practices

### 1. Regular Updates

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### 2. Firewall Configuration

```bash
# Install UFW (Uncomplicated Firewall)
sudo apt-get install ufw

# Allow SSH (before enabling!)
sudo ufw allow 22

# Allow HTTP and HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### 3. SSH Security

```bash
# Disable password authentication
sudo nano /etc/ssh/sshd_config

# Change these lines:
# PasswordAuthentication no
# PermitRootLogin no

# Restart SSH
sudo systemctl restart sshd
```

### 4. Fail2Ban (Protect against brute force)

```bash
# Install Fail2Ban
sudo apt-get install fail2ban

# Create local configuration
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local

# Enable for SSH:
[sshd]
enabled = true
port = 22
maxretry = 3
bantime = 3600

# Restart Fail2Ban
sudo systemctl restart fail2ban
```

### 5. Regular Backups

- Database backups (daily)
- Application code (in Git)
- Environment files (securely stored)
- Docker volumes (if needed)

---

## Cost Estimation

### AWS EC2 Costs (as of 2024)

**Instance costs (per month, us-east-1):**
- t2.micro (1 vCPU, 1 GB RAM): Free tier (750 hours/month for 12 months), then ~$8.50/month
- t2.small (1 vCPU, 2 GB RAM): ~$17/month
- t2.medium (2 vCPU, 4 GB RAM): ~$34/month
- t2.large (4 vCPU, 8 GB RAM): ~$68/month

**Storage (EBS):**
- 20 GB gp3: ~$1.60/month
- 30 GB gp3: ~$2.40/month

**Elastic IP:**
- Free when associated with running instance
- $0.005/hour (~$3.60/month) when not associated

**Data Transfer:**
- First 1 GB/month: Free
- Next 9.999 TB/month: $0.09/GB
- Estimate: $10-50/month depending on traffic

**Total estimated monthly cost:**
- Small site (t2.micro + 20GB): ~$10-15/month
- Medium site (t2.small + 30GB): ~$20-30/month
- Production site (t2.medium + 30GB): ~$40-60/month

**Domain Registration:**
- $10-15/year (from registrar like Namecheap, GoDaddy)

**Let's Encrypt SSL:**
- Free!

---

## Troubleshooting Guide

### Issue: Can't SSH into EC2

**Solutions:**
1. Check security group allows port 22 from your IP
2. Verify key file permissions: `chmod 400 ~/.ssh/fastapi-key.pem`
3. Check instance is running in EC2 console
4. Verify you're using correct username (`ubuntu` for Ubuntu AMI)
5. Try: `ssh -vvv -i ~/.ssh/fastapi-key.pem ubuntu@IP` for verbose output

### Issue: DNS not resolving

**Solutions:**
1. Wait 30-60 minutes for DNS propagation
2. Check DNS records are correct (use whatsmydns.net)
3. Verify A record points to Elastic IP (not regular public IP)
4. Clear your local DNS cache: `sudo systemd-resolve --flush-caches` (Linux)
5. Try accessing directly via IP address

### Issue: SSL Certificate not issued

**Solutions:**
1. Wait 5-10 minutes after DNS propagates
2. Check Traefik logs: `docker compose -f ~/traefik-public/docker-compose.traefik.yml logs`
3. Verify DNS is correctly resolving
4. Ensure ports 80 and 443 are open
5. Check Let's Encrypt rate limits
6. Verify email address in DOMAIN environment variable is valid

### Issue: Application not accessible

**Solutions:**
1. Check containers are running: `docker compose ps`
2. Check Traefik dashboard for routers
3. Check application logs: `docker compose logs`
4. Verify domain in environment variables matches DNS
5. Check security groups allow ports 80 and 443

### Issue: Database connection errors

**Solutions:**
1. Check PostgreSQL container: `docker compose ps db`
2. Check database logs: `docker compose logs db`
3. Verify POSTGRES_PASSWORD in .env matches docker-compose.yml
4. Try restarting: `docker compose restart db`
5. Check database initialization: `docker compose logs backend | grep -i database`

### Issue: Out of disk space

**Solutions:**
```bash
# Check disk usage
df -h

# Clean Docker system
docker system prune -a

# Clean old images
docker image prune -a

# Clean logs
sudo journalctl --vacuum-time=7d

# Clean apt cache
sudo apt-get clean
```

---

## Additional Resources

### Documentation Links

- **FastAPI**: https://fastapi.tiangolo.com/
- **Docker**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **Traefik**: https://doc.traefik.io/traefik/
- **Let's Encrypt**: https://letsencrypt.org/docs/
- **AWS EC2**: https://docs.aws.amazon.com/ec2/
- **GitHub Actions**: https://docs.github.com/en/actions

---

## Transitioning from Gray Cloud to Orange Cloud + Flexible SSL

If you initially deployed using **Gray Cloud (DNS-only mode)** with Let's Encrypt SSL certificates, but now want to use **Cloudflare's Orange Cloud (proxied mode)** to gain CDN, DDoS protection, and caching benefits, follow this guide.

### Understanding the Modes

**Gray Cloud (DNS-only):**
- Direct connection between users and your server
- Let's Encrypt certificates handled by Traefik on your server
- No Cloudflare CDN, caching, or DDoS protection
- What you have if you followed the main deployment guide

**Orange Cloud (Proxied) + Flexible SSL:**
- Users connect to Cloudflare's network
- Cloudflare provides SSL certificate to users
- Cloudflare connects to your server via HTTP (unencrypted)
- You get: CDN, DDoS protection, caching, and all Cloudflare features
- Simpler configuration (no Let's Encrypt needed on your server)

**Orange Cloud + Full (Strict) SSL:**
- Same as Flexible, but connection between Cloudflare and your server is also encrypted
- More secure than Flexible SSL
- Requires Cloudflare Origin Certificate instead of Let's Encrypt
- Recommended for production applications with sensitive data

### Prerequisites

- ✅ You have a working deployment with Gray Cloud and Let's Encrypt
- ✅ Your domain is registered with or managed by Cloudflare
- ✅ You have access to your Cloudflare dashboard
- ✅ You have SSH access to your EC2 server

---

## Option 1: Orange Cloud with Flexible SSL (Easiest)

This is the simplest transition and gets you all Cloudflare benefits with minimal configuration changes.

### Step 1: Understand the Security Trade-off

**Flexible SSL Security Model:**
- ✅ User ↔ Cloudflare: Encrypted (HTTPS)
- ⚠️ Cloudflare ↔ Your Server: Unencrypted (HTTP)

**Why this is generally acceptable:**
- Traffic between Cloudflare and your server travels over Cloudflare's private network
- Cloudflare has data centers worldwide, so the unencrypted portion is minimal
- This is suitable for most applications that don't handle highly sensitive data
- You can upgrade to Full (Strict) SSL later if needed

**Not recommended for:**
- Banking or financial applications
- Healthcare applications (HIPAA compliance)
- Applications handling very sensitive personal data

### Step 2: Modify Traefik Configuration

**SSH into your EC2 instance:**

```bash
ssh -i ~/.ssh/fastapi-key.pem ubuntu@YOUR_SERVER_IP
```

**Stop Traefik:**

```bash
cd ~/traefik-public
docker compose -f docker-compose.traefik.yml down
```

**Create a new simplified Traefik config:**

```bash
# Backup the old configuration
cp docker-compose.traefik.yml docker-compose.traefik.yml.backup

# Edit the file
nano docker-compose.traefik.yml
```

**Replace the content with this HTTP-only configuration:**

```yaml
services:
  traefik:
    image: traefik:3.0
    ports:
      # Only expose port 80 (HTTP)
      - 80:80
    restart: always
    labels:
      # Enable Traefik for this service
      - traefik.enable=true
      # Use the traefik-public network
      - traefik.docker.network=traefik-public
      # Define the port inside of the Docker service to use
      - traefik.http.services.traefik-dashboard.loadbalancer.server.port=8080
      # Make Traefik use this domain in HTTP
      - traefik.http.routers.traefik-dashboard-http.entrypoints=http
      - traefik.http.routers.traefik-dashboard-http.rule=Host(`traefik.${DOMAIN?Variable not set}`)
      # admin-auth middleware with HTTP Basic auth
      - traefik.http.middlewares.admin-auth.basicauth.users=${USERNAME?Variable not set}:${HASHED_PASSWORD?Variable not set}
      # Enable HTTP Basic auth
      - traefik.http.routers.traefik-dashboard-http.middlewares=admin-auth
      # Use the special Traefik service api@internal with the web UI/Dashboard
      - traefik.http.routers.traefik-dashboard-http.service=api@internal
    volumes:
      # Add Docker as a mounted volume
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command:
      # Enable Docker in Traefik
      - --providers.docker
      # Do not expose all Docker services by default
      - --providers.docker.exposedbydefault=false
      # Create an entrypoint "http" listening on port 80
      - --entrypoints.http.address=:80
      # Enable the access log
      - --accesslog
      # Enable the Traefik log
      - --log
      # Enable the Dashboard and API
      - --api
    networks:
      - traefik-public

networks:
  traefik-public:
    external: true
```

**Save and exit** (Ctrl+X, Y, Enter)

**Key changes made:**
- Removed port 443 (HTTPS)
- Removed all Let's Encrypt configuration
- Removed HTTPS routers
- Removed HTTPS redirect middleware
- Removed certificate storage volume
- Kept only HTTP (port 80) configuration

### Step 3: Update Your Application Configuration

**Edit your application's docker-compose.yml:**

```bash
cd ~/fastapi-project
nano docker-compose.yml
```

**Find and update the Traefik labels for your services.** Change from HTTPS to HTTP:

**For backend service, change this:**

```yaml
labels:
  - traefik.http.routers.backend-https.entrypoints=https
  - traefik.http.routers.backend-https.rule=Host(`api.${DOMAIN}`)
  - traefik.http.routers.backend-https.tls=true
  - traefik.http.routers.backend-https.tls.certresolver=le
```

**To this:**

```yaml
labels:
  - traefik.http.routers.backend-http.entrypoints=http
  - traefik.http.routers.backend-http.rule=Host(`api.${DOMAIN}`)
```

**For frontend service, make similar changes:**

Change from:
```yaml
labels:
  - traefik.http.routers.frontend-https.entrypoints=https
  - traefik.http.routers.frontend-https.rule=Host(`dashboard.${DOMAIN}`)
  - traefik.http.routers.frontend-https.tls=true
  - traefik.http.routers.frontend-https.tls.certresolver=le
```

To:
```yaml
labels:
  - traefik.http.routers.frontend-http.entrypoints=http
  - traefik.http.routers.frontend-http.rule=Host(`dashboard.${DOMAIN}`)
```

**Make similar changes for all other services** (adminer, etc.)

**Save and exit** (Ctrl+X, Y, Enter)

### Step 4: Configure Cloudflare SSL Settings

**In your Cloudflare dashboard:**

1. **Select your domain** from the Cloudflare dashboard
2. **Go to SSL/TLS settings:**
   - Click "SSL/TLS" in the left sidebar
   - Under "Overview" tab

3. **Select SSL/TLS encryption mode:**
   - Choose **"Flexible"**
   - This tells Cloudflare to encrypt traffic from users to Cloudflare, but use HTTP to your origin

4. **Configure additional SSL settings (optional but recommended):**
   - Go to "Edge Certificates" tab
   - Enable "Always Use HTTPS" - redirects all HTTP requests to HTTPS
   - Enable "Automatic HTTPS Rewrites" - automatically rewrites HTTP links to HTTPS
   - Set "Minimum TLS Version" to "TLS 1.2" or higher for better security

### Step 5: Enable Cloudflare Proxy (Orange Cloud)

**In Cloudflare DNS settings:**

1. **Go to DNS settings:**
   - Click "DNS" in the left sidebar

2. **Enable proxy for your DNS records:**
   - Find your A records (e.g., `@`, `*`, `api`, `dashboard`)
   - Click on each record
   - Change "Proxy status" from **Gray Cloud** (DNS only) to **Orange Cloud** (Proxied)
   - Click "Save"

3. **Verify your records look like this:**
   ```
   Type: A
   Name: @
   Content: YOUR_SERVER_IP
   Proxy status: Proxied (Orange cloud icon)
   TTL: Auto

   Type: A
   Name: *
   Content: YOUR_SERVER_IP
   Proxy status: Proxied (Orange cloud icon)
   TTL: Auto
   ```

### Step 6: Restart Services

**Start Traefik with new configuration:**

```bash
cd ~/traefik-public
docker compose -f docker-compose.traefik.yml up -d
```

**Restart your application:**

```bash
cd ~/fastapi-project
docker compose down
docker compose up -d
```

**Check logs to ensure everything started correctly:**

```bash
# Check Traefik
docker compose -f ~/traefik-public/docker-compose.traefik.yml logs

# Check application
docker compose logs
```

### Step 7: Test Your Deployment

**Wait 5-10 minutes** for DNS and Cloudflare changes to propagate.

**Test your endpoints:**

1. **Test with HTTP** (will be redirected to HTTPS by Cloudflare):
   ```
   http://dashboard.YOUR_DOMAIN.com
   ```

2. **Test with HTTPS** (should work immediately):
   ```
   https://dashboard.YOUR_DOMAIN.com
   https://api.YOUR_DOMAIN.com/docs
   https://traefik.YOUR_DOMAIN.com
   ```

3. **Verify you're going through Cloudflare:**
   - Open browser developer tools (F12)
   - Go to Network tab
   - Load your site
   - Look for response headers
   - You should see `CF-Ray` and `Server: cloudflare` headers

### Step 8: Enable Cloudflare Features

Now that you're using Orange Cloud, you can enable additional Cloudflare features:

**Caching:**
1. Go to "Caching" in Cloudflare dashboard
2. Set "Caching Level" to "Standard" or "Aggressive"
3. Configure "Browser Cache TTL"
4. Create Page Rules for specific caching behaviors

**Firewall:**
1. Go to "Security" > "WAF"
2. Enable "OWASP Core Ruleset"
3. Create custom firewall rules if needed

**DDoS Protection:**
1. Automatically enabled with Orange Cloud
2. Go to "Security" > "DDoS" to view protections

**Speed Optimizations:**
1. Go to "Speed" > "Optimization"
2. Enable "Auto Minify" (HTML, CSS, JS)
3. Enable "Brotli" compression
4. Enable "Early Hints"

**Analytics:**
1. Go to "Analytics & Logs"
2. View traffic analytics, security events, performance metrics

### Step 9: Troubleshooting Flexible SSL

**Issue: Redirect loop**

If you experience infinite redirect loops:

```bash
# On your server, ensure you're NOT redirecting HTTP to HTTPS
# Check your application code and Traefik config
# Remove any HTTPS redirect middleware

# In Cloudflare:
# - Verify SSL mode is "Flexible"
# - Disable "Always Use HTTPS" temporarily to test
# - Clear browser cache and cookies
```

**Issue: Mixed content warnings**

If some resources load over HTTP:

```javascript
// In your frontend code, use protocol-relative URLs:
// Bad: http://api.example.com
// Good: https://api.example.com
// Best: //api.example.com (inherits protocol)

// Or configure CORS properly in your backend
```

**Issue: 525 SSL Handshake Failed**

This error means Cloudflare is trying to use SSL but your server isn't:

```bash
# Verify you're on Flexible SSL mode in Cloudflare
# Check that your server is only exposing port 80 (HTTP)
docker ps | grep traefik
# Should show: 0.0.0.0:80->80/tcp (no 443)
```

---

## Option 2: Orange Cloud with Full (Strict) SSL (More Secure)

This option provides end-to-end encryption. Cloudflare will connect to your server using HTTPS with a Cloudflare Origin Certificate.

### Step 1: Generate Cloudflare Origin Certificate

**In Cloudflare dashboard:**

1. **Go to SSL/TLS settings:**
   - Click "SSL/TLS" in the left sidebar
   - Click "Origin Server" tab

2. **Create certificate:**
   - Click "Create Certificate"
   - Select "Let Cloudflare generate a private key and a CSR"
   - **Host names**: Enter your domain and wildcard
     ```
     yourdomain.com
     *.yourdomain.com
     ```
   - **Certificate Validity**: Choose 15 years (maximum)
   - Click "Next"

3. **Save certificate files:**
   - You'll see two text boxes:
   
   **Origin Certificate** (save as `cloudflare-cert.pem`):
   ```
   -----BEGIN CERTIFICATE-----
   [long string of characters]
   -----END CERTIFICATE-----
   ```
   
   **Private Key** (save as `cloudflare-key.pem`):
   ```
   -----BEGIN PRIVATE KEY-----
   [long string of characters]
   -----END PRIVATE KEY-----
   ```

   - **IMPORTANT**: Save both of these NOW. You can't view the private key again!
   - Copy each to a secure text file on your computer

4. **Click "OK"** to complete

### Step 2: Upload Certificates to Your Server

**Create certificates directory:**

```bash
# SSH into your EC2 instance
ssh -i ~/.ssh/fastapi-key.pem ubuntu@YOUR_SERVER_IP

# Create directory for certificates
cd ~/traefik-public
mkdir -p certs
cd certs
```

**Create certificate files:**

```bash
# Create certificate file
nano cloudflare-cert.pem
# Paste the Origin Certificate content
# Save and exit (Ctrl+X, Y, Enter)

# Create private key file
nano cloudflare-key.pem
# Paste the Private Key content
# Save and exit (Ctrl+X, Y, Enter)

# Secure the files
chmod 600 cloudflare-cert.pem cloudflare-key.pem
```

### Step 3: Configure Traefik for Static Certificates

**Edit Traefik docker-compose file:**

```bash
cd ~/traefik-public
nano docker-compose.traefik.yml
```

**Replace with this configuration:**

```yaml
services:
  traefik:
    image: traefik:3.0
    ports:
      - 80:80
      - 443:443
    restart: always
    labels:
      - traefik.enable=true
      - traefik.docker.network=traefik-public
      - traefik.http.services.traefik-dashboard.loadbalancer.server.port=8080
      # HTTP router (will redirect to HTTPS)
      - traefik.http.routers.traefik-dashboard-http.entrypoints=http
      - traefik.http.routers.traefik-dashboard-http.rule=Host(`traefik.${DOMAIN?Variable not set}`)
      # HTTPS router
      - traefik.http.routers.traefik-dashboard-https.entrypoints=https
      - traefik.http.routers.traefik-dashboard-https.rule=Host(`traefik.${DOMAIN?Variable not set}`)
      - traefik.http.routers.traefik-dashboard-https.tls=true
      - traefik.http.routers.traefik-dashboard-https.service=api@internal
      # HTTPS redirect middleware
      - traefik.http.middlewares.https-redirect.redirectscheme.scheme=https
      - traefik.http.middlewares.https-redirect.redirectscheme.permanent=true
      - traefik.http.routers.traefik-dashboard-http.middlewares=https-redirect
      # Admin auth middleware
      - traefik.http.middlewares.admin-auth.basicauth.users=${USERNAME?Variable not set}:${HASHED_PASSWORD?Variable not set}
      - traefik.http.routers.traefik-dashboard-https.middlewares=admin-auth
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      # Mount certificate directory
      - ./certs:/certs:ro
      # Mount Traefik configuration
      - ./traefik-config.yml:/etc/traefik/traefik-config.yml:ro
    command:
      - --providers.docker
      - --providers.docker.exposedbydefault=false
      # HTTP entrypoint
      - --entrypoints.http.address=:80
      # HTTPS entrypoint
      - --entrypoints.https.address=:443
      # Load file provider for static certificates
      - --providers.file.filename=/etc/traefik/traefik-config.yml
      - --providers.file.watch=true
      # Enable logs
      - --accesslog
      - --log
      - --api
    networks:
      - traefik-public

networks:
  traefik-public:
    external: true
```

**Save and exit**

**Create Traefik static configuration file:**

```bash
cd ~/traefik-public
nano traefik-config.yml
```

**Add this content:**

```yaml
# Static TLS configuration
tls:
  certificates:
    - certFile: /certs/cloudflare-cert.pem
      keyFile: /certs/cloudflare-key.pem
  stores:
    default:
      defaultCertificate:
        certFile: /certs/cloudflare-cert.pem
        keyFile: /certs/cloudflare-key.pem
```

**Save and exit**

### Step 4: Update Application Configuration

**Edit your application docker-compose.yml:**

```bash
cd ~/fastapi-project
nano docker-compose.yml
```

**Update Traefik labels for HTTPS:**

For each service (backend, frontend, etc.), update labels to:

```yaml
labels:
  - traefik.enable=true
  - traefik.docker.network=traefik-public
  - traefik.http.services.SERVICE_NAME.loadbalancer.server.port=PORT
  
  # HTTP router (redirect to HTTPS)
  - traefik.http.routers.SERVICE_NAME-http.entrypoints=http
  - traefik.http.routers.SERVICE_NAME-http.rule=Host(`SUBDOMAIN.${DOMAIN}`)
  - traefik.http.routers.SERVICE_NAME-http.middlewares=https-redirect
  
  # HTTPS router
  - traefik.http.routers.SERVICE_NAME-https.entrypoints=https
  - traefik.http.routers.SERVICE_NAME-https.rule=Host(`SUBDOMAIN.${DOMAIN}`)
  - traefik.http.routers.SERVICE_NAME-https.tls=true
  
  # HTTPS redirect middleware
  - traefik.http.middlewares.https-redirect.redirectscheme.scheme=https
  - traefik.http.middlewares.https-redirect.redirectscheme.permanent=true
```

Replace `SERVICE_NAME`, `PORT`, and `SUBDOMAIN` with appropriate values.

**Example for backend:**

```yaml
backend:
  labels:
    - traefik.enable=true
    - traefik.docker.network=traefik-public
    - traefik.http.services.backend.loadbalancer.server.port=8000
    - traefik.http.routers.backend-http.entrypoints=http
    - traefik.http.routers.backend-http.rule=Host(`api.${DOMAIN}`)
    - traefik.http.routers.backend-http.middlewares=https-redirect
    - traefik.http.routers.backend-https.entrypoints=https
    - traefik.http.routers.backend-https.rule=Host(`api.${DOMAIN}`)
    - traefik.http.routers.backend-https.tls=true
    - traefik.http.middlewares.https-redirect.redirectscheme.scheme=https
    - traefik.http.middlewares.https-redirect.redirectscheme.permanent=true
```

**Save and exit**

### Step 5: Configure Cloudflare for Full (Strict) SSL

**In Cloudflare dashboard:**

1. **Go to SSL/TLS settings:**
   - Click "SSL/TLS" in left sidebar
   - Under "Overview" tab

2. **Select SSL mode:**
   - Choose **"Full (strict)"**
   - This tells Cloudflare to verify your origin certificate

3. **Additional settings** (under "Edge Certificates"):
   - Enable "Always Use HTTPS"
   - Enable "Automatic HTTPS Rewrites"
   - Set "Minimum TLS Version" to "TLS 1.2" or higher

4. **Enable Orange Cloud** in DNS settings:
   - Go to "DNS" tab
   - Enable proxy (Orange Cloud) for all your A records

### Step 6: Restart Services

```bash
# Start Traefik
cd ~/traefik-public
docker compose -f docker-compose.traefik.yml down
docker compose -f docker-compose.traefik.yml up -d

# Check Traefik logs
docker compose -f docker-compose.traefik.yml logs

# Restart application
cd ~/fastapi-project
docker compose down
docker compose up -d

# Check application logs
docker compose logs
```

### Step 7: Test Full (Strict) SSL

**Test your endpoints:**

```
https://dashboard.YOUR_DOMAIN.com
https://api.YOUR_DOMAIN.com/docs
https://traefik.YOUR_DOMAIN.com
```

**Verify end-to-end encryption:**

1. Check browser padlock icon - should show secure
2. View certificate - should show Cloudflare certificate (to users)
3. Check response headers for `CF-Ray` - confirms Cloudflare proxy
4. Your origin is using Cloudflare Origin Certificate (hidden from users)

---

## Comparing SSL Options

### Summary Table

| Feature | Gray Cloud + Let's Encrypt | Orange Cloud + Flexible SSL | Orange Cloud + Full (Strict) SSL |
|---------|---------------------------|----------------------------|----------------------------------|
| User ↔ Cloudflare Encryption | ❌ Direct to origin | ✅ HTTPS | ✅ HTTPS |
| Cloudflare ↔ Origin Encryption | ✅ HTTPS (Let's Encrypt) | ❌ HTTP | ✅ HTTPS (Origin Cert) |
| CDN | ❌ No | ✅ Yes | ✅ Yes |
| DDoS Protection | ❌ No | ✅ Yes | ✅ Yes |
| Caching | ❌ No | ✅ Yes | ✅ Yes |
| Setup Complexity | Medium | Easy | Medium |
| Certificate Management | Automatic (Let's Encrypt) | None required | One-time (15 years) |
| Security Level | Good | Acceptable | Best |
| Best For | Direct control | Quick setup, low sensitivity | Production, sensitive data |

### Which Should You Choose?

**Choose Gray Cloud + Let's Encrypt if:**
- You want direct control over SSL certificates
- You don't need CDN or DDoS protection
- You have low to moderate traffic
- You're just testing or developing

**Choose Orange Cloud + Flexible SSL if:**
- You want the easiest transition
- You need CDN, DDoS, and caching NOW
- Your application doesn't handle very sensitive data
- You want to get started quickly

**Choose Orange Cloud + Full (Strict) SSL if:**
- You need CDN, DDoS, and caching
- You handle sensitive user data
- You want end-to-end encryption
- You're running a production application

**Recommended path:**
1. Start with **Gray Cloud** (you're already here)
2. Transition to **Orange Cloud + Flexible SSL** for immediate benefits
3. Upgrade to **Full (Strict) SSL** when you have time

---

## Maintenance and Monitoring

### Certificate Expiration

**Flexible SSL:**
- No maintenance needed
- Cloudflare manages certificates automatically

**Full (Strict) SSL with Origin Certificates:**
- Origin certificates valid for 15 years
- Set a calendar reminder for year 14 to generate new certificate
- Cloudflare will email you about expiration

### Monitoring

**Check Cloudflare Analytics:**
- Dashboard shows traffic, security threats, performance
- Go to "Analytics & Logs" in Cloudflare dashboard

**Check Origin Health:**
```bash
# SSH into your server
docker compose ps
docker compose logs

# Check Traefik
docker compose -f ~/traefik-public/docker-compose.traefik.yml logs
```

### Reverting Changes

**To revert back to Gray Cloud:**

1. **In Cloudflare DNS:**
   - Change Orange Cloud to Gray Cloud for all records
   
2. **On your server:**
   - Restore original Traefik configuration:
   ```bash
   cd ~/traefik-public
   cp docker-compose.traefik.yml.backup docker-compose.traefik.yml
   docker compose -f docker-compose.traefik.yml down
   docker compose -f docker-compose.traefik.yml up -d
   ```

3. **Wait for DNS to propagate** (5-10 minutes)

---

## Additional Cloudflare Features

Once you're using Orange Cloud, you can leverage these features:

### Page Rules
Create custom caching and security rules for specific URLs

### Workers
Run serverless JavaScript at the edge

### Load Balancing
Distribute traffic across multiple origin servers

### Rate Limiting
Protect against abuse and scraping

### Bot Management
Block malicious bots while allowing good bots

### Image Optimization
Automatically optimize and resize images

All of these are available from your Cloudflare dashboard!
### Useful Tools

- **Portainer**: Docker GUI management - https://www.portainer.io/
- **ctop**: Container monitoring - https://github.com/bcicen/ctop
- **lazydocker**: Terminal UI for Docker - https://github.com/jesseduffield/lazydocker

### Community Support

- **FastAPI GitHub**: https://github.com/tiangolo/fastapi
- **FastAPI Discord**: https://discord.gg/VQjSZaeJmf
- **Stack Overflow**: Tag your questions with `fastapi`, `docker`, `traefik`

---

## Conclusion

You now have a complete, production-ready deployment of your FastAPI application on AWS EC2 with:

✅ Automatic HTTPS certificates  
✅ Reverse proxy with Traefik  
✅ Docker containerization  
✅ Database persistence  
✅ Continuous deployment with GitHub Actions  
✅ Multiple environments (staging/production)  
✅ Secure configuration  

**Next steps:**
1. Set up monitoring (consider tools like Prometheus, Grafana, or Datadog)
2. Configure automated backups
3. Set up logging aggregation (ELK stack, CloudWatch)
4. Implement application performance monitoring (APM)
5. Set up alerting for downtime or errors
6. Consider scaling strategies (load balancers, auto-scaling groups)

Happy deploying! 🚀
