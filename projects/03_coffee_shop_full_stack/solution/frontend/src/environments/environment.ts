export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'fbs-fsnd', // the auth0 domain prefix
    audience: 'coffee_shop_full_stack', // the audience set for the auth0 app
    clientId: 'xveV7CJniwu2JVEiEm4WN5jI3AIJ4NIN', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application.
  }
};
