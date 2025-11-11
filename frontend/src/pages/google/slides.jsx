import { useState } from 'react';
import Layout from '../../components/layout/Layout';

export default function GoogleSlides() {
  return (
    <Layout>
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">Google Slides</h1>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600">
            Surveillance des activités Google Slides
          </p>
        </div>
      </div>
    </Layout>
  );
}
