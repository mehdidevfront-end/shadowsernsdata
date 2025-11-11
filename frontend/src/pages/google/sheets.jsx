import React from 'react';
import Layout from '../../components/layout/Layout';
import GoogleLogsViewer from '../../components/GoogleLogsViewer';

const SheetsPage = () => {
  return (
    <Layout>
      <GoogleLogsViewer service="sheets" />
    </Layout>
  );
};

export default SheetsPage;
