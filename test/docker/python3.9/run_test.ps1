docker build -t crudcreator_test_python3.9 -f test/docker/python3.9/Dockerfile .
docker compose -f test/docker/docker-compose.yaml --env-file test/docker/python3.9/.env.local up crudcreator_test