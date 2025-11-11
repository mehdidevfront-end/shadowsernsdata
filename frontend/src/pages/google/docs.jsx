import React from 'react';
import Layout from '../../components/layout/Layout';
import GoogleLogsViewer from '../../components/GoogleLogsViewer';

const DocsPage = () => {
  return (
    <Layout>
      <GoogleLogsViewer service="docs" />
    </Layout>
  );
};

export default DocsPage;
