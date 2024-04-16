docker network create crudcreator_test
docker compose -f docker-compose.yaml --env-file .env.local up postgres