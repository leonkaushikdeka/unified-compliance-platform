import { useEffect, useState } from 'react'
import axios from 'axios'

interface DPDPDashboard {
  total_data_sources: number
  total_pii_records: number
  risk_score: number
  consent_rate: number
  pending_dsrs: number
  dsr_compliance_rate: number
  consent_summary: { total: number; granted: number; withdrawn: number }
  recent_scans: any[]
}

export default function DPDP() {
  const [dashboard, setDashboard] = useState<DPDPDashboard | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('dashboard')

  useEffect(() => {
    fetchDashboard()
  }, [])

  const fetchDashboard = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get('/api/v1/dpdpa/dashboard', {
        headers: { Authorization: `Bearer ${token}` },
      })
      setDashboard(response.data)
    } catch (error) {
      console.error('Failed to fetch DPDP dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">DPDP Act Compliance</h1>
        <span className="text-sm text-gray-500">India's Digital Personal Data Protection Act</span>
      </div>

      <div className="mb-6 border-b">
        <nav className="flex gap-4">
          {['dashboard', 'data-discovery', 'consent', 'dsr'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 border-b-2 font-medium ${
                activeTab === tab
                  ? 'border-primary-600 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </button>
          ))}
        </nav>
      </div>

      {activeTab === 'dashboard' && dashboard && (
        <div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <p className="text-sm text-gray-500">Data Sources</p>
              <p className="text-3xl font-bold">{dashboard.total_data_sources}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <p className="text-sm text-gray-500">PII Records Found</p>
              <p className="text-3xl font-bold">{dashboard.total_pii_records}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <p className="text-sm text-gray-500">Risk Score</p>
              <p className={`text-3xl font-bold ${dashboard.risk_score > 50 ? 'text-red-600' : 'text-green-600'}`}>
                {dashboard.risk_score}
              </p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <p className="text-sm text-gray-500">Consent Rate</p>
              <p className="text-3xl font-bold text-blue-600">{dashboard.consent_rate}%</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4">Consent Summary</h2>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span>Total Records</span>
                  <span className="font-medium">{dashboard.consent_summary.total}</span>
                </div>
                <div className="flex justify-between">
                  <span>Consent Granted</span>
                  <span className="font-medium text-green-600">{dashboard.consent_summary.granted}</span>
                </div>
                <div className="flex justify-between">
                  <span>Withdrawn</span>
                  <span className="font-medium text-red-600">{dashboard.consent_summary.withdrawn}</span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4">DSR Compliance</h2>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span>Pending DSRs</span>
                  <span className="font-medium">{dashboard.pending_dsrs}</span>
                </div>
                <div className="flex justify-between">
                  <span>Completion Rate</span>
                  <span className="font-medium text-green-600">{dashboard.dsr_compliance_rate}%</span>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-6 bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-4">Recent Data Scans</h2>
            {dashboard.recent_scans.length > 0 ? (
              <div className="space-y-3">
                {dashboard.recent_scans.map(scan => (
                  <div key={scan.id} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <div>
                      <p className="font-medium">{scan.source_name}</p>
                      <p className="text-sm text-gray-500">{scan.source_type}</p>
                    </div>
                    <div className="text-right">
                      <span className={`px-2 py-1 text-xs rounded ${
                        scan.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {scan.status}
                      </span>
                      <p className="text-sm text-gray-500 mt-1">Risk: {scan.risk_score}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">No scans yet. Start a data discovery scan.</p>
            )}
          </div>
        </div>
      )}

      {activeTab === 'data-discovery' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Data Discovery Scan</h2>
          <p className="text-gray-500 mb-4">Scan your data sources to identify PII and assess risk.</p>
          <form className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Source Name</label>
              <input type="text" className="w-full px-3 py-2 border rounded-md" placeholder="e.g., Production Database" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Source Type</label>
              <select className="w-full px-3 py-2 border rounded-md">
                <option value="postgresql">PostgreSQL</option>
                <option value="mysql">MySQL</option>
                <option value="mongodb">MongoDB</option>
                <option value="s3">S3 Bucket</option>
              </select>
            </div>
            <button type="button" className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
              Start Scan
            </button>
          </form>
        </div>
      )}

      {activeTab === 'consent' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Consent Management</h2>
          <p className="text-gray-500 mb-4">Manage consent records and preferences.</p>
          <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
            Create Consent Session
          </button>
        </div>
      )}

      {activeTab === 'dsr' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Data Subject Requests</h2>
          <p className="text-gray-500 mb-4">Handle Access, Correction, Deletion, and Portability requests.</p>
          <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
            New DSR Request
          </button>
        </div>
      )}
    </div>
  )
}
