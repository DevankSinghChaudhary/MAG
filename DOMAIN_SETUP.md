# Custom Domain Setup Guide

## Prerequisites
- A domain name registered with a domain provider (e.g., GoDaddy, Namecheap, Google Domains)
- Access to your domain's DNS management console

## Steps to Connect Custom Domain

1. **Get your Streamlit Cloud app URL**
   - After deploying your app on Streamlit Cloud, note the URL (e.g., `your-app-name.streamlit.app`)

2. **Configure DNS settings**
   - Log in to your domain provider's control panel
   - Navigate to the DNS management section
   - Add a new CNAME record with:
     - Name/Host: `app` (or any subdomain you prefer)
     - Value/Points to: `your-app-name.streamlit.app`
     - TTL: 3600 (or default)

3. **Configure custom domain in Streamlit Cloud**
   - In your Streamlit Cloud app settings, add your custom domain
   - Wait for DNS propagation (may take up to 24 hours)

4. **Verify the configuration**
   - Once DNS propagation is complete, your custom domain should point to your Streamlit app
   - Test by visiting `app.yourdomain.com` (replace with your actual domain)

## Example
If your domain is `example.com`, you can set up:
- `app.example.com` pointing to `your-app-name.streamlit.app`

## Troubleshooting
- Ensure there are no conflicting DNS records
- Check that your domain provider supports CNAME records for subdomains
- Contact Streamlit Cloud support if the domain doesn't resolve after 24 hours