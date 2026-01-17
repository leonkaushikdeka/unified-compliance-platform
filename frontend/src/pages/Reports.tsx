export default function Reports() {
  const templates = [
    { id: 'executive_summary', name: 'Executive Summary', description: 'High-level compliance overview' },
    { id: 'detailed_assessment', name: 'Detailed Assessment', description: 'Full assessment report with findings' },
    { id: 'gap_analysis', name: 'Gap Analysis', description: 'Control gaps and remediation priorities' },
    { id: 'sla_compliance', name: 'SLA Compliance', description: 'DSR and compliance deadline tracking' },
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Reports</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {templates.map(template => (
          <div key={template.id} className="bg-white rounded-lg shadow p-6 hover:shadow-md transition">
            <h3 className="font-semibold text-lg">{template.name}</h3>
            <p className="text-gray-500 mt-1">{template.description}</p>
            <button className="mt-4 text-primary-600 hover:text-primary-700 font-medium text-sm">
              Generate Report →
            </button>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Generate Custom Report</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Report Type</label>
            <select className="w-full px-3 py-2 border rounded-md">
              <option>Compliance Summary</option>
              <option>Assessment Details</option>
              <option>Audit Trail</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Format</label>
            <select className="w-full px-3 py-2 border rounded-md">
              <option>PDF</option>
              <option>Excel</option>
              <option>JSON</option>
            </select>
          </div>
          <div className="flex items-end">
            <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 w-full">
              Download Report
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
