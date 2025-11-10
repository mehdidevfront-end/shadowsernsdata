import React, { useEffect, useState } from 'react'

export default function FinopsPage() {
  const [kpis, setKpis] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch('/api/finops')
        const json = await res.json()
        setKpis(json)
      } catch (e) {
        console.error(e)
      }
    }
    load()
  }, [])

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">FinOps</h1>
      {!kpis && <div>Chargement...</div>}
      {kpis && (
        <div>
          <div className="p-4 border rounded mb-2">Monthly cost: {kpis.monthly_cloud_cost}</div>
          <div className="p-4 border rounded mb-2">Orphaned assets: {kpis.orphaned_assets_count}</div>
          <div className="p-4 border rounded">Top cost services:</div>
          <ul className="list-disc pl-6">
            {kpis.top_cost_services.map((s, i) => (
              <li key={i}>{s.service}: {s.cost}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
