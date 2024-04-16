docker build -t crudcreator_test_python3.10 -f test/docker/python3.10/Dockerfile .
docker compose -f test/docker/docker-compose.yaml --env-file test/docker/python3.10/.env.local up crudcreator_test