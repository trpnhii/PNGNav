# X11 Forwarding Setup for Windows

This guide explains how to enable X11 forwarding on Windows so that GUI applications (Gazebo, RViz) can display in Docker containers.

## Option 1: Using VcXsrv (Recommended)

VcXsrv is a free X server for Windows that works well with Docker.

### Step 1: Install VcXsrv

1. Download VcXsrv from: https://sourceforge.net/projects/vcxsrv/
2. Install it (default settings are fine)

### Step 2: Configure VcXsrv

1. **Start VcXsrv** from the Start Menu
2. **Configuration Window** will appear:
   - Select **"Multiple windows"** (default)
   - Click **Next**
   - Select **"Start no client"** (default)
   - Click **Next**
   - **IMPORTANT**: Check **"Disable access control"** (this allows Docker to connect)
   - Click **Finish**

3. VcXsrv will start running (you'll see an icon in the system tray)

### Step 3: Find Your Windows IP Address

Open PowerShell or Command Prompt and run:

```powershell
ipconfig
```

Look for your active network adapter (usually "Ethernet adapter" or "Wireless LAN adapter") and note the **IPv4 Address**. For example: `192.168.1.100`

**Alternative**: If you're using WSL2, get the WSL IP:

```powershell
wsl hostname -I
```

### Step 4: Update docker-compose.yml

You need to modify the `DISPLAY` environment variable. Update `docker-compose.yml`:

```yaml
environment:
  - DISPLAY=YOUR_IP_ADDRESS:0.0  # Replace YOUR_IP_ADDRESS with your actual IP
  - QT_X11_NO_MITSHM=1
```

**Example:**
```yaml
environment:
  - DISPLAY=192.168.1.100:0.0
  - QT_X11_NO_MITSHM=1
```

### Step 5: Configure Windows Firewall

Allow VcXsrv through Windows Firewall:

1. Open **Windows Defender Firewall**
2. Click **"Allow an app or feature through Windows Defender Firewall"**
3. Find **"VcXsrv"** and check both **Private** and **Public**
4. If not found, click **"Allow another app"** and browse to:
   - `C:\Program Files\VcXsrv\vcxsrv.exe`

### Step 6: Start Docker Container

```bash
docker-compose up -d
docker-compose exec pngnav-gazebo bash
```

### Step 7: Test X11

Inside the container, test if X11 works:

```bash
xeyes  # If installed, or
xclock  # If installed
```

If you see a window, X11 is working!

## Option 2: Using WSL2 with X11

If you're using WSL2 (Windows Subsystem for Linux), you can use X11 forwarding through WSL.

### Step 1: Install VcXsrv (same as Option 1)

Follow Steps 1-2 from Option 1 to install and configure VcXsrv.

### Step 2: Set DISPLAY in WSL

In your WSL2 terminal:

```bash
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0
```

Or manually:

```bash
# Get Windows host IP from WSL
export DISPLAY=$(ip route show | grep -i default | awk '{ print $3}'):0.0
```

### Step 3: Update docker-compose.yml

Use the WSL IP or Windows host IP:

```yaml
environment:
  - DISPLAY=host.docker.internal:0.0  # For Docker Desktop
  # OR
  - DISPLAY=YOUR_WSL_IP:0.0  # If using WSL IP
```

### Step 4: Test

Same as Option 1, Step 7.

## Option 3: Using Xming (Alternative)

Xming is another X server option for Windows.

1. Download from: https://sourceforge.net/projects/xming/
2. Install Xming
3. Start Xming
4. Follow similar steps as VcXsrv, but Xming configuration is slightly different

## Troubleshooting

### Issue: "Cannot connect to X server"

**Solutions:**
1. Make sure VcXsrv is running (check system tray)
2. Verify DISPLAY variable is correct:
   ```bash
   echo $DISPLAY
   ```
3. Check Windows Firewall settings
4. Try using `host.docker.internal:0.0` instead of IP address

### Issue: "Connection refused"

**Solutions:**
1. Make sure **"Disable access control"** is checked in VcXsrv
2. Restart VcXsrv
3. Check that the IP address in DISPLAY matches your actual IP

### Issue: "No protocol specified"

**Solutions:**
1. This means access control is blocking. Make sure "Disable access control" is enabled in VcXsrv
2. Restart VcXsrv after changing settings

### Issue: GUI appears but is slow

**Solutions:**
1. This is normal - X11 over network can be slower
2. Consider using WSL2 for better performance
3. Reduce GUI quality in Gazebo settings

## Quick Test Script

Create a test script to verify X11 is working:

```bash
# Inside Docker container
export DISPLAY=YOUR_IP:0.0
xeyes  # or any X11 app
```

## Alternative: Use Headless Mode

If X11 is too complicated, you can run Gazebo in headless mode (no GUI):

```bash
# Inside container
gazebo --verbose  # Headless mode
```

However, RViz will still need X11.

## Recommended Setup for Windows

1. **Use VcXsrv** (easiest option)
2. **Set DISPLAY to your Windows IP** in docker-compose.yml
3. **Keep VcXsrv running** while using Docker
4. **Add VcXsrv to startup** so it starts automatically

## Notes

- VcXsrv must be running before starting Docker containers
- The IP address might change if you switch networks - update docker-compose.yml accordingly
- For better performance, consider using WSL2 instead of native Windows Docker
- Some applications may have rendering issues - this is normal with X11 forwarding
