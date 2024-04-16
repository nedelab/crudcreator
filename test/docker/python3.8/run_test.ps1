docker build -t crudcreator_test_python3.8 -f test/docker/python3.8/Dockerfile .
docker compose -f test/docker/docker-compose.yaml --env-file test/docker/python3.8/.env.local up crudcreator_test