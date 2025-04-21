import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Common port service names (very basic mapping)
common_ports = {
    20: "FTP (Data)",
    21: "FTP (Control)",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP"
}

# Function to resolve host to IP address
def resolve_host(target):
    try:
        # Try resolving the hostname to an IP address
        return socket.gethostbyname(target)
    except socket.gaierror:
        messagebox.showerror("Resolution Error", f"Unable to resolve IP for {target}. Please check the target name.")
        return None

# Port Scanner Function
def scan_ports():
    target = ip_entry.get()
    
    # Resolve host if input is not IP
    if not target.replace('.', '').isdigit():  # Check if the input is an IP address or hostname
        target = resolve_host(target)
        if not target:
            return

    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter valid port numbers.")
        return

    if not target:
        messagebox.showwarning("Missing Input", "Please enter a target IP address or hostname.")
        return

    result_area.delete(1.0, tk.END)
    result_area.insert(tk.END, f"🔍 Scanning {target} from port {start_port} to {end_port}...\n")

    socket.setdefaulttimeout(0.5)

    for port in range(start_port, end_port + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((target, port))
            if result == 0:
                service = common_ports.get(port, "Unknown Service")
                result_area.insert(tk.END, f"✅ Port {port} is OPEN ({service})\n")
            s.close()
        except Exception as e:
            result_area.insert(tk.END, f"⚠️ Error scanning port {port}: {str(e)}\n")

    result_area.insert(tk.END, "\n✅ Scan complete.\n")

# GUI Setup
root = tk.Tk()
root.title("Simple Network Port Scanner")
root.geometry("500x480")
root.configure(bg="#eafaf1")
root.resizable(False, False)

tk.Label(root, text="🔐 Simple Network Port Scanner", font=("Segoe UI", 14, "bold"), bg="#eafaf1", pady=10).pack()

frame = tk.Frame(root, bg="#eafaf1")
frame.pack(pady=10)

tk.Label(frame, text="Target IP Address/Hostname:", bg="#eafaf1").grid(row=0, column=0, sticky="w")
ip_entry = tk.Entry(frame, width=30)
ip_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Start Port:", bg="#eafaf1").grid(row=1, column=0, sticky="w")
start_port_entry = tk.Entry(frame, width=10)
start_port_entry.grid(row=1, column=1, sticky="w", pady=5)

tk.Label(frame, text="End Port:", bg="#eafaf1").grid(row=2, column=0, sticky="w")
end_port_entry = tk.Entry(frame, width=10)
end_port_entry.grid(row=2, column=1, sticky="w", pady=5)

tk.Button(root, text="Start Scan", command=scan_ports, bg="#28a745", fg="white",
          font=("Segoe UI", 10, "bold"), padx=10, pady=5).pack(pady=5)

result_area = scrolledtext.ScrolledText(root, width=58, height=15, font=("Consolas", 10))
result_area.pack(pady=10)

disclaimer = "⚠️ This tool is for educational use only. Scan only hosts you have permission to test."
tk.Label(root, text=disclaimer, font=("Segoe UI", 8), bg="#eafaf1", fg="red", wraplength=460, justify="center").pack(pady=5)

root.mainloop()
