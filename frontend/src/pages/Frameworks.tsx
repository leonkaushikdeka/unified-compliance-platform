import { useEffect, useState } from 'react'
import axios from 'axios'

interface Framework {
  id: string
  name: string
  description: string
  framework_type: string
  version: string
  is_active: boolean
}

export default function Frameworks() {
  const [frameworks, setFrameworks] = useState<Framework[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('')

  useEffect(() => {
    fetchFrameworks()
  }, [])

  const fetchFrameworks = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get('/api/v1/frameworks', {
        headers: { Authorization: `Bearer ${token}` },
      })
      setFrameworks(response.data.frameworks)
    } catch (error) {
      console.error('Failed to fetch frameworks:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredFrameworks = frameworks.filter(f =>
    f.name.toLowerCase().includes(filter.toLowerCase()) ||
    f.framework_type.toLowerCase().includes(filter.toLowerCase())
  )

  const frameworkTypes = [...new Set(frameworks.map(f => f.framework_type))]

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Compliance Frameworks</h1>
        <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
          Add Framework
        </button>
      </div>

      <div className="mb-6">
        <input
          type="text"
          placeholder="Search frameworks..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="w-full md:w-64 px-4 py-2 border rounded-md"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {frameworkTypes.map(type => (
          <div key={type} className="mb-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-3 uppercase">{type}</h3>
            <div className="space-y-4">
              {filteredFrameworks.filter(f => f.framework_type === type).map(framework => (
                <div key={framework.id} className="bg-white rounded-lg shadow p-4 hover:shadow-md transition">
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-semibold">{framework.name}</h4>
                      <p className="text-sm text-gray-500 mt-1">{framework.description}</p>
                    </div>
                    <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                      v{framework.version}
                    </span>
                  </div>
                  <div className="mt-4 flex justify-end">
                    <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                      Start Assessment →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {filteredFrameworks.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          No frameworks found. Try adjusting your search.
        </div>
      )}
    </div>
  )
}
