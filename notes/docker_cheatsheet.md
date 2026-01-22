# Docker cheatsheet

## Build and run
- Build: `docker build -t myapp:dev .`
- Run: `docker run --rm -p 8000:8000 myapp:dev`
- Build with no cache: `docker build --no-cache -t myapp:dev .`
- Build with build args: `docker build --build-arg VERSION=1.0 -t myapp:dev .`

## Container management
- List running containers: `docker ps`
- List all containers: `docker ps -a`
- Stop container: `docker stop <container_id>`
- Remove container: `docker rm <container_id>`
- Remove all stopped containers: `docker container prune`
- View logs: `docker logs <container_id>` or `docker logs -f <container_id>` (follow)

## Useful flags
- `--rm`: remove container after exit
- `-e KEY=VALUE`: set env var
- `-v host:container`: mount volume
- `-p host:container`: port mapping
- `-d`: run in detached mode (background)
- `-it`: interactive terminal
- `--name`: assign a name to container
- `--network`: connect to a network
- `--env-file`: load env vars from file

## Networks
- Create network: `docker network create mynet`
- List networks: `docker network ls`
- Inspect network: `docker network inspect mynet`
- Connect a running container: `docker network connect mynet <container_id>`
- Run container in a network: `docker run --network mynet ...`

## Images
- List images: `docker images`
- Remove image: `docker rmi <image_id>`
- Remove unused images: `docker image prune -a`
- Tag image: `docker tag myapp:dev myapp:v1.0`
- Push to registry: `docker push myapp:v1.0`

## Dockerfile best practices
- Use specific base image tags, not `latest`.
- Combine RUN commands to reduce layers.
- Use `.dockerignore` to exclude unnecessary files.
- Set WORKDIR early and use relative paths.
- Use multi-stage builds for smaller final images.
- Don't run as root in production (use USER directive).

## Docker Compose
- Start services: `docker-compose up` or `docker compose up`
- Start in background: `docker-compose up -d`
- Stop services: `docker-compose down`
- View logs: `docker-compose logs -f <service_name>`
- Rebuild and restart: `docker-compose up --build`

## Debugging
- Execute command in running container: `docker exec -it <container_id> <command>`
- Get shell access: `docker exec -it <container_id> /bin/sh` or `/bin/bash`
- Inspect container: `docker inspect <container_id>`
- View resource usage: `docker stats`

