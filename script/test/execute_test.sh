#!/bin/bash

cd msh
sudo sqlite3 ./db/test.db < create.sql
echo "const Data = {};

const Auth = {
   clients: {
	'client_id': {
		clientId: 'client_id',
		clientSecret: 'client_secret'
	}
   },
  tokens: {
	'token_test': {
		userId: '1',
		uid: '1',
		accessToken: 'token_test',
		refreshToken: 'token_test'
	},
	'token_admin': {
		userId: '2',
		uid: '2',
		accessToken: 'token_admin',
		refreshToken: 'token_admin'
	}
  },
  users: {
	'2': {
		tokens: [
			'token_admin'
		],
		name: 'admin',
		uid: '2',
		password: 'admin'
	},
	'1': {
		tokens: [
			'token_test'
		],
		name: 'test',
		uid: '1',
		password: 'test'
	}
  },
  usernames: {
    'test': '1',
	'admin': '2'
  },
  authcodes: {}
};

Data.version = 0;

Data.getUid = function (uid) {
  return Data[uid];
};

/**
 * checks if user and auth exist and match
 *
 * @param uid
 * @param authToken
 * @returns {boolean}
 */
Data.isValidAuth = function (uid, authToken) {
  return (Data.getUid(uid));
};

exports.getUid = Data.getUid;
exports.isValidAuth = Data.isValidAuth;
exports.Auth = Auth;" > ../oauth/datastore_test.js
sudo python3 -m coverage erase
sudo python3 -m coverage run -m pytest --junitxml=test-report.xml
sudo mv .coverage ..
sudo mv test-report.xml ..
sudo rm db/test.db
sudo rm ../oauth/datastore_test.js
cd ..
exit 0