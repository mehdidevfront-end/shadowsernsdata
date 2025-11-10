import React, { useEffect, useState } from 'react'

export default function CompliancePage() {
  const [kpis, setKpis] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch('/api/compliance')
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
      <h1 className="text-2xl font-bold mb-4">Conformité</h1>
      {!kpis && <div>Chargement...</div>}
      {kpis && (
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 border rounded">Total assets: {kpis.total_assets}</div>
          <div className="p-4 border rounded">Total risks: {kpis.total_risks}</div>
          <div className="p-4 border rounded">High risks: {kpis.high_risks}</div>
          <div className="p-4 border rounded">RGPD coverage: {kpis.rgpd_coverage}</div>
        </div>
      )}
    </div>
  )
}
