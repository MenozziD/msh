cd ../Docker/base_image
docker build . --tag=msh:v0.0.1
cp ../../msh ../target_image
cd ../target_image
docker build . --tag=msrheal:v0.0.1
docker run -d --name raspberrypi -p 8080:65177 msrheal:v0.0.1
