import { useEffect, useState } from 'react'
import axios from 'axios'

interface Assessment {
  id: string
  name: string
  description: string
  status: string
  progress: number
  score: number
  created_at: string
  framework?: { name: string }
}

export default function Assessments() {
  const [assessments, setAssessments] = useState<Assessment[]>([])
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState('')

  useEffect(() => {
    fetchAssessments()
  }, [])

  const fetchAssessments = async () => {
    try {
      const token = localStorage.getItem('token')
      const params = statusFilter ? `?status=${statusFilter}` : ''
      const response = await axios.get(`/api/v1/assessments${params}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      setAssessments(response.data.assessments)
    } catch (error) {
      console.error('Failed to fetch assessments:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800'
      case 'in_progress': return 'bg-blue-100 text-blue-800'
      case 'draft': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Assessments</h1>
        <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
          New Assessment
        </button>
      </div>

      <div className="mb-6 flex gap-4">
        <select
          value={statusFilter}
          onChange={(e) => { setStatusFilter(e.target.value); fetchAssessments() }}
          className="px-4 py-2 border rounded-md"
        >
          <option value="">All Status</option>
          <option value="draft">Draft</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Framework</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Progress</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Created</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {assessments.map(assessment => (
              <tr key={assessment.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">
                  <div className="font-medium text-gray-900">{assessment.name}</div>
                  {assessment.description && (
                    <div className="text-sm text-gray-500 truncate max-w-xs">{assessment.description}</div>
                  )}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  {assessment.framework?.name || '-'}
                </td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(assessment.status)}`}>
                    {assessment.status.replace('_', ' ')}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full"
                      style={{ width: `${assessment.progress}%` }}
                    />
                  </div>
                  <span className="text-xs text-gray-500">{assessment.progress}%</span>
                </td>
                <td className="px-6 py-4 text-sm font-medium">
                  <span className={assessment.score >= 70 ? 'text-green-600' : assessment.score >= 40 ? 'text-yellow-600' : 'text-red-600'}>
                    {assessment.score}%
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  {new Date(assessment.created_at).toLocaleDateString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {assessments.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            No assessments found. Create your first assessment to get started.
          </div>
        )}
      </div>
    </div>
  )
}
