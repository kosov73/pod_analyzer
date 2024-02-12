import os,re
import subprocess
import pandas as pd

def get_app_name(pod):
    command = f"kubectl get pods -n {namespace} {pod} -o=custom-columns=APP:.metadata.labels.app --no-headers"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print("Возникла ошибка:", error)
        return None
    else:
        return output.decode().strip()

def get_user_accounts(pod):
    command = f"kubectl exec -n {namespace} {pod} -- cat /etc/passwd"
    output = subprocess.check_output(command, shell=True).decode().strip()
    return output

def get_root_directory_permissions(pod):
    command = f"kubectl exec -n {namespace} {pod} -- ls -la /"
    output = subprocess.check_output(command, shell=True).decode().strip()
    return output

def get_os_image_mounted_directories_exposed_ports(pod):
    command = f"kubectl describe pod -n {namespace} {pod}"
    output = subprocess.check_output(command, shell=True).decode().strip()
    return output

def get_installed_packages(pod):
    command = f"kubectl exec -n {namespace} {pod} -- apk list"
    output = subprocess.check_output(command, shell=True).decode().strip()
    return output

namespace = "elma365"
pods = subprocess.check_output(f"kubectl get pods -n {namespace} -o jsonpath='{{range .items[*]}}{{.metadata.name}}:{{end}}'", shell=True).decode().strip().split(":")[:-1]
data = []
for pod in pods:
    row = {}
    row["POD"] = get_app_name(pod)
    row["User Accounts"] = get_user_accounts(pod)
    row["Root Directory Permissions"] = get_root_directory_permissions(pod)
#    os_image, mounted_directories, exposed_ports = get_os_image_mounted_directories_exposed_ports(pod)
#    row["OS Image"] = os_image
#    row["Mounted Directories"] = mounted_directories
#    row["Exposed Ports"] = exposed_ports
    row["Installed Packages"] = get_installed_packages(pod)
    data.append(row)

df = pd.DataFrame(data)
df.to_excel("pods.xlsx", index=False)
