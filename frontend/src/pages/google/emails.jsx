import React from 'react';
import Layout from '../../components/layout/Layout';
import GoogleLogsViewer from '../../components/GoogleLogsViewer';

const EmailsPage = () => {
  return (
    <Layout>
      <GoogleLogsViewer service="email" />
    </Layout>
  );
};

export default EmailsPage;
