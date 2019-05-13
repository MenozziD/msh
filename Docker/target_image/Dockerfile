FROM msh:v0.0.1

# Set the working directory to /msh
WORKDIR /msh

# Copy the current directory msh contents into the container at /msh
COPY msh/ /msh/

RUN mkdir db
RUN sqlite3 ./db/system.db
RUN sqlite3 ./db/system.db < ./script/create.sql
RUN rm -r script

# Run msh.py when the container launches
CMD ["python3", "msh.py"]