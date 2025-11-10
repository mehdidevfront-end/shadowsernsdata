import React from 'react'
import AnomaliesDashboard from '../components/AnomaliesDashboard'

export default function Page() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Anomalies</h1>
      <AnomaliesDashboard src="/reports/shadow_report.jsonl" />
    </div>
  )
}
