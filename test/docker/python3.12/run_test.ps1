docker build -t crudcreator_test_python3.12 -f test/docker/python3.12/Dockerfile .
docker compose -f test/docker/docker-compose.yaml --env-file test/docker/python3.12/.env.local up crudcreator_test