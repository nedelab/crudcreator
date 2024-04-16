docker build -t crudcreator_test_python3.11 -f test/docker/python3.11/Dockerfile .
docker compose -f test/docker/docker-compose.yaml --env-file test/docker/python3.11/.env.local up crudcreator_test