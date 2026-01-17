import { useEffect, useState } from 'react'
import axios from 'axios'
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

interface DashboardMetrics {
  total_assessments: number
  completed_assessments: number
  in_progress_assessments: number
  average_score: number
  compliance_rate: number
  upcoming_deadlines: number
  recent_findings: any[]
}

export default function Dashboard() {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboard()
  }, [])

  const fetchDashboard = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get('/api/v1/frameworks/dashboard', {
        headers: { Authorization: `Bearer ${token}` },
      })
      setMetrics(response.data)
    } catch (error) {
      console.error('Failed to fetch dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  const pieData = metrics ? [
    { name: 'Completed', value: metrics.completed_assessments },
    { name: 'In Progress', value: metrics.in_progress_assessments },
    { name: 'Not Started', value: metrics.total_assessments - metrics.completed_assessments - metrics.in_progress_assessments },
  ] : []

  const COLORS = ['#10B981', '#F59E0B', '#6B7280']

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-gray-500">Total Assessments</p>
          <p className="text-3xl font-bold">{metrics?.total_assessments || 0}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-gray-500">Completed</p>
          <p className="text-3xl font-bold text-green-600">{metrics?.completed_assessments || 0}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-gray-500">Average Score</p>
          <p className="text-3xl font-bold text-blue-600">{metrics?.average_score || 0}%</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-gray-500">Compliance Rate</p>
          <p className="text-3xl font-bold text-purple-600">{metrics?.compliance_rate || 0}%</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Assessment Status</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Compliance Overview</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={[
              { name: 'Score', value: metrics?.average_score || 0 },
              { name: 'Compliance', value: metrics?.compliance_rate || 0 },
            ]}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-6 bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <a href="/frameworks" className="p-4 border rounded-lg hover:bg-gray-50 text-center">
            <p className="font-medium">Browse Frameworks</p>
            <p className="text-sm text-gray-500">SOC2, GDPR, HIPAA...</p>
          </a>
          <a href="/assessments" className="p-4 border rounded-lg hover:bg-gray-50 text-center">
            <p className="font-medium">New Assessment</p>
            <p className="text-sm text-gray-500">Start compliance check</p>
          </a>
          <a href="/dpdp" className="p-4 border rounded-lg hover:bg-gray-50 text-center">
            <p className="font-medium">DPDP Compliance</p>
            <p className="text-sm text-gray-500">Data protection</p>
          </a>
          <a href="/reports" className="p-4 border rounded-lg hover:bg-gray-50 text-center">
            <p className="font-medium">Generate Report</p>
            <p className="text-sm text-gray-500">Export compliance data</p>
          </a>
        </div>
      </div>
    </div>
  )
}
