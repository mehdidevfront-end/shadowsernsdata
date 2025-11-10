import React, { useEffect, useState } from 'react'
import GraphView from '../../components/GraphView'
import Filters from '../../components/Filters'

export default function AssetGraph({ params }) {
  const [data, setData] = useState({incoming: [], outgoing: []})
  const [filters, setFilters] = useState({})
  const asset = params?.asset || ''

  useEffect(() => {
    async function fetchGraph() {
      const qs = new URLSearchParams(filters)
      const res = await fetch(`http://localhost:8000/graph/${asset}?${qs.toString()}`)
      const json = await res.json()
      setData(json)
    }
    if (asset) fetchGraph()
  }, [asset, filters])

  const nodesMap = {}
  const links = []
  // add center asset
  nodesMap[asset] = { id: asset, group: 'asset' }
  data.outgoing.forEach(o => {
    nodesMap[o.id] = { id: o.id, group: 'service' }
    const w = (o.rel && (o.rel.weight || o.rel['weight'])) ? (o.rel.weight || o.rel['weight']) : 1
    links.push({ source: asset, target: o.id, weight: w })
  })
  data.incoming.forEach(i => {
    nodesMap[i.id] = { id: i.id, group: 'service' }
    const w = (i.rel && (i.rel.weight || i.rel['weight'])) ? (i.rel.weight || i.rel['weight']) : 1
    links.push({ source: i.id, target: asset, weight: w })
  })

  const nodes = Object.values(nodesMap)

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold">Graph: {asset}</h1>
      <Filters filters={filters} setFilters={setFilters} />
      <GraphView nodes={nodes} links={links} width={1000} height={700} />
    </div>
  )
}
