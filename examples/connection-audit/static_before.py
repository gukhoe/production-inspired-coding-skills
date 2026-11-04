"""Static-only test input. Never execute this file."""
import requests
import subprocess


def forward(url, command):
    response = requests.post(url, json={'message':'synthetic'}, verify=False)
    subprocess.run(command, shell=True)
    return response
