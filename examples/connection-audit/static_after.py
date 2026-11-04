"""Static control-remediation fixture, not proof of full runtime safety."""
import requests
import subprocess


def forward(url, arguments):
    response = requests.post(url, json={'message':'synthetic'}, timeout=5, verify=True)
    subprocess.run(arguments, shell=False, check=True)
    return response
