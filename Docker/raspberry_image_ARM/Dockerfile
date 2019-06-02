FROM msh-arm:v0.0.1
ARG google_actions_project_id
ARG user
ARG password
ARG dominio_oauth
ARG dominio_webapp
ARG nome_wifi
ARG password_wifi
WORKDIR /server
COPY server/ /server/
COPY setup/02_setup.sh /
COPY setup/oauth.py /server/oauth/
WORKDIR /
RUN /02_setup.sh $google_actions_project_id $user $password $dominio_oauth $dominio_webapp $nome_wifi $password_wifi
WORKDIR /server/msh
CMD ["python3", "msh.py"]