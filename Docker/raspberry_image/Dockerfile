FROM msh:v0.0.1
ARG ngrok_auth_token
ARG google_actions_project_id
WORKDIR /server
COPY server/ /server/
# SERVER APPLICATIVO
RUN mkdir msh/db
RUN sqlite3 ./msh/db/system.db
RUN sqlite3 ./msh/db/system.db < ./msh/script/create.sql
RUN rm -r ./msh/script
# SERVER OAUTH
WORKDIR ./fake-oauth-server-nodejs
RUN npm install
# CREO NGROK.YAML CON TOKEN PRESO IN INPUT
RUN echo "authtoken: $ngrok_auth_token \n\
tunnels: \n\
  app-foo: \n\
    addr: 65177 \n\
    proto: http \n\
  app-bar: \n\
    addr: 3000 \n\
    proto: http" > ../ngrok.yaml
# SALVO PROJECT ID DI GOOGLE ACTIONS IN SETTINGS.XML
RUN echo "<settings> \n\
	<porta>65177</porta> \n\
	<lingua>IT</lingua> \n\
	<timestamp>%Y-%m-%d %H:%M:%S</timestamp> \n\
	<project_id_google_actions>$google_actions_project_id</project_id_google_actions> \n\
	<log> \n\
		<!-- Se valorizzato con None logga in console --> \n\
		<filename>msh.log</filename> \n\
		<format>%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s</format> \n\
		<!-- debug, info, warning, error, critical --> \n\
		<level>info</level> \n\
	</log> \n\
</settings>" > ../msh/settings.xml
RUN echo "impostare credenziali Account Linking | OAuth | Authorization Code | client ID RKkWfsi0Z9"
RUN echo "impostare credenziali Account Linking | OAuth | Authorization Code | client secret eToBzeBT7OwrPQO8mZHsZtLp1qhQbe"
WORKDIR ../
CMD ./start.sh