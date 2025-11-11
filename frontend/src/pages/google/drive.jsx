import React from 'react';
import Layout from '../../components/layout/Layout';
import GoogleLogsViewer from '../../components/GoogleLogsViewer';

const DrivePage = () => {
  return (
    <Layout>
      <GoogleLogsViewer service="drive" />
    </Layout>
  );
};

export default DrivePage;
