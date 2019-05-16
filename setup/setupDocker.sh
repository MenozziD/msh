cd ../Docker/base_image
docker build . --tag=msh:v0.0.1
cp ../../msh ../raspberry_image
cd ../raspberry_image
docker build . --tag=raspberrypi:v0.0.1
docker run -d --name raspberrypi -p 8080:65177 raspberrypi:v0.0.1
