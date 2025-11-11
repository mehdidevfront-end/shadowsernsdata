import React from 'react';
import Layout from '../components/layout/Layout';
import ServerLogsViewer from '../components/ServerLogsViewer';

const ServerLogsPage = () => {
  return (
    <Layout>
      <ServerLogsViewer />
    </Layout>
  );
};

export default ServerLogsPage;
