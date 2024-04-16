docker build --progress=plain -t crudcreator_test_installation -f test/docker/installation/Dockerfile .
docker run --name crudcreator_test_installation crudcreator_test_installation