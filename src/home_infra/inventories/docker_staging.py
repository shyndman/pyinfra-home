"""
Docker staging inventory for testing deployments.
"""

# Define Docker containers for testing
# These will be used to test deployments before applying to real servers
docker_staging = [
    "docker-ubuntu-test",  # A container name that will be used for testing
]

# Group data for docker staging
docker_staging_data = {
    "ssh_user": "root",
    "ssh_key": "~/.ssh/id_rsa",
}
