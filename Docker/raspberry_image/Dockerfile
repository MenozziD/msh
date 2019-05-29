FROM msh:v0.0.1
ARG google_actions_project_id
ARG user
ARG password
ARG dominio_oauth
ARG dominio_webapp
WORKDIR /server
COPY server/ /server/
COPY start.sh /server/
# DATABASE
RUN mkdir msh/db
RUN sqlite3 ./msh/db/system.db
RUN sqlite3 ./msh/db/system.db < ./msh/script/create.sql
RUN echo "INSERT INTO TB_USER (USERNAME, PASSWORD, ROLE) VALUES ('$user', '$password', 'ADMIN');" > ./msh/script/user.sql
RUN sqlite3 ./msh/db/system.db < ./msh/script/user.sql
RUN rm -r ./msh/script
# SERVER OAUTH
WORKDIR ./oauth
# CREO DATASTORE PER OAUTH SERVER
RUN echo "const Data = {}; \n\
 \n\
const Auth = { \n\
  clients: { \n\
    'RKkWfsi0Z9': { \n\
      clientId: 'RKkWfsi0Z9', \n\
      clientSecret: 'eToBzeBT7OwrPQO8mZHsZtLp1qhQbe' \n\
    } \n\
  }, \n\
  tokens: { \n\
    'psokmCxKjfhk7qHLeYd1': { \n\
      uid: '1', \n\
      accessToken: 'psokmCxKjfhk7qHLeYd1', \n\
      refreshToken: 'psokmCxKjfhk7qHLeYd1', \n\
      userId: '1' \n\
    } \n\
  }, \n\
  users: { \n\
    '1': { \n\
      uid: '1', \n\
      name: '$user', \n\
      password: '$password', \n\
      tokens: ['psokmCxKjfhk7qHLeYd1'] \n\
    } \n\
  }, \n\
  usernames: { \n\
    '$user': '1' \n\
  }, \n\
  authcodes: {} \n\
}; \n\
 \n\
Data.version = 0; \n\
 \n\
Data.getUid = function (uid) { \n\
  return Data[uid]; \n\
}; \n\
 \n\
/** \n\
 * checks if user and auth exist and match \n\
 * \n\
 * @param uid \n\
 * @param authToken \n\
 * @returns {boolean} \n\
 */ \n\
Data.isValidAuth = function (uid, authToken) { \n\
  return (Data.getUid(uid)); \n\
}; \n\
 \n\
exports.getUid = Data.getUid; \n\
exports.isValidAuth = Data.isValidAuth; \n\
exports.Auth = Auth;" > datastore.js
RUN npm install
# SALVO PROJECT ID DI GOOGLE ACTIONS IN SETTINGS.XML
RUN echo "<settings> \n\
	<lingua>IT</lingua> \n\
	<timestamp>%Y-%m-%d %H:%M:%S</timestamp> \n\
	<project_id_google_actions>$google_actions_project_id</project_id_google_actions> \n\
	<subdomain_oauth>$dominio_oauth</subdomain_oauth> \n\
	<subdomain_webapp>$dominio_webapp</subdomain_webapp> \n\
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
