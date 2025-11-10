import React from 'react'

export default function Filters({ filters, setFilters }) {
  return (
    <div className="p-2 flex gap-2">
      <select value={filters.type || ''} onChange={e => setFilters({...filters, type: e.target.value})}>
        <option value="">Tous types</option>
        <option value="service">service</option>
        <option value="database">database</option>
      </select>
      <select value={filters.criticite || ''} onChange={e => setFilters({...filters, criticite: e.target.value})}>
        <option value="">Toutes criticités</option>
        <option value="low">low</option>
        <option value="medium">medium</option>
        <option value="high">high</option>
      </select>
      <input placeholder="BU" value={filters.bu || ''} onChange={e => setFilters({...filters, bu: e.target.value})} />
      <input placeholder="Env" value={filters.env || ''} onChange={e => setFilters({...filters, env: e.target.value})} />
    </div>
  )
}
