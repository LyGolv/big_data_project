import subprocess


def delete_docker_containers_and_volumes():
    """
    Deletes all Docker containers, networks, images, and volumes defined in the Docker Compose file.
    :return: None
    """
    try:
        subprocess.run(["docker-compose", "down", "--volumes"], check=True)
        print("Stopped and removed all containers, networks, images, and volumes defined in the Docker Compose file.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop and remove containers, networks, images, and volumes: {e}")


delete_docker_containers_and_volumes()
