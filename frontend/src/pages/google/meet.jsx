import React from 'react';
import Layout from '../../components/layout/Layout';
import GoogleLogsViewer from '../../components/GoogleLogsViewer';

const MeetPage = () => {
  return (
    <Layout>
      <GoogleLogsViewer service="meet" />
    </Layout>
  );
};

export default MeetPage;
