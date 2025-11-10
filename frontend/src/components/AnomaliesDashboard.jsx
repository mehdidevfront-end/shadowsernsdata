import React, { useEffect, useState } from 'react'
import { Bar } from 'react-chartjs-2'
import 'chart.js/auto'

export default function AnomaliesDashboard({ src = '/reports/shadow_report.jsonl' }) {
  const [items, setItems] = useState([])

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch(src)
        const text = await res.text()
        const lines = text.split('\n').filter(Boolean)
        const parsed = lines.map(l => JSON.parse(l))
        setItems(parsed)
      } catch (e) {
        console.error(e)
      }
    }
    fetchData()
  }, [src])

  const countsByHour = Array(24).fill(0)
  items.forEach(it => {
    const ts = it.record && (it.record.ts || it.record.timestamp)
    if (ts) {
      const h = new Date(ts).getHours()
      countsByHour[h] = (countsByHour[h] || 0) + 1
    }
  })

  const data = {
    labels: Array.from({ length: 24 }, (_, i) => String(i)),
    datasets: [
      {
        label: 'Anomalies by hour',
        data: countsByHour,
        backgroundColor: 'rgba(255,99,132,0.5)'
      }
    ]
  }

  return (
    <div className="p-4">
      <h2 className="text-lg font-bold mb-2">Anomalies dashboard</h2>
      <div style={{ width: '100%', maxWidth: 900 }}>
        <Bar data={data} />
      </div>
      <h3 className="mt-4">Recent anomalies</h3>
      <div className="overflow-auto max-h-64 border p-2 mt-2">
        <table className="min-w-full text-sm">
          <thead>
            <tr>
              <th>ts</th>
              <th>provider</th>
              <th>match</th>
            </tr>
          </thead>
          <tbody>
            {items.slice(0, 200).map((it, idx) => (
              <tr key={idx}>
                <td>{(it.record && (it.record.ts || it.record.timestamp)) || 'n/a'}</td>
                <td>{(it.detections && it.detections[0] && it.detections[0].provider) || '-'}</td>
                <td>{(it.detections && it.detections[0] && it.detections[0].match) || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
