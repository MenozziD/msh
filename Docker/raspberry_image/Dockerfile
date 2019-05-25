FROM msh:v0.0.1
WORKDIR /msh
COPY msh/ /msh/
RUN mkdir db
RUN sqlite3 ./db/system.db
RUN sqlite3 ./db/system.db < ./script/create.sql
RUN rm -r script
CMD ["python3", "msh.py"]