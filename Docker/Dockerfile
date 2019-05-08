# Parto da un SO Raspbian di base
FROM raspbian/jessie:041517

# Set the working directory to /msh
WORKDIR /msh

# Copy the current directory msh contents into the container at /msh
COPY ./msh/* /msh

# Install any needed packages
RUN sudo apt-get update
RUN sudo apt-get install python3
RUN sudo apt-get install python3-pip
RUN sudo pip3 install --trusted-host pypi.python.org -r library.txt
RUN sudo apt-get install sqlite3 libsqlite3-dev
RUN mkdir db
RUN sudo sqlite3 ./db/system.db
RUN sqlite3 ./db/system.db < ./script/create.sql

# Make port 80 available to the world outside this container
EXPOSE 80

# Run msh.py when the container launches
CMD ["python3", "msh.py"]