import os


def main():
    os.system('echo "### Docker Settings" && '
              'cat ~/Library/Group\ Containers/group.com.docker/settings.json')
    os.system('echo "\n### Docker System DF" && docker system df')
    os.system('echo "\n### df -h /var/lib/docker" && df -h /var/lib/docker')
    os.system('echo "\n### docker stats --no-stream" && docker stats --no-stream')
    os.system('echo "\n### cat docker_logs/output.log" && cat docker_logs/output.log')
    os.system('echo "\n### docker logs backend-web-1" && docker logs backend-web-1')
    os.system('echo "\n### cat logs/logs.log" && cat logs/logs.log')


def _read_file(file_path):
    try:
        with open(file_path) as file:
            return file.read()
    except Exception:
        pass


if __name__ == '__main__':
    main()
