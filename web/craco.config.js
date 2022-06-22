const CracoLessPlugin = require('craco-less');

module.exports = {
  plugins: [
    {
      plugin: CracoLessPlugin,
      options: {
        lessLoaderOptions: {
          lessOptions: {
            modifyVars: { 
              '@primary-color': '#f26649',
              '@border-radius-base': '3.5px'
           },
            javascriptEnabled: true,
          },
        },
      },
    },
  ],
};