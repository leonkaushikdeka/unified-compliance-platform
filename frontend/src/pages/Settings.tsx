import { useState } from 'react'

export default function Settings() {
  const [activeTab, setActiveTab] = useState('profile')

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Settings</h1>

      <div className="flex gap-6">
        <div className="w-48">
          <nav className="space-y-1">
            {['profile', 'organization', 'security', 'notifications', 'billing'].map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === tab
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                {tab.replace(/\b\w/g, l => l.toUpperCase())}
              </button>
            ))}
          </nav>
        </div>

        <div className="flex-1 bg-white rounded-lg shadow p-6">
          {activeTab === 'profile' && (
            <div>
              <h2 className="text-lg font-semibold mb-4">Profile Settings</h2>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                    <input type="text" className="w-full px-3 py-2 border rounded-md" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                    <input type="text" className="w-full px-3 py-2 border rounded-md" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input type="email" className="w-full px-3 py-2 border rounded-md" />
                </div>
                <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                  Save Changes
                </button>
              </div>
            </div>
          )}

          {activeTab === 'organization' && (
            <div>
              <h2 className="text-lg font-semibold mb-4">Organization Settings</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Organization Name</label>
                  <input type="text" className="w-full px-3 py-2 border rounded-md" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Plan</label>
                  <select className="w-full px-3 py-2 border rounded-md">
                    <option>Starter</option>
                    <option>Professional</option>
                    <option>Enterprise</option>
                  </select>
                </div>
                <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                  Save Changes
                </button>
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div>
              <h2 className="text-lg font-semibold mb-4">Security Settings</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Current Password</label>
                  <input type="password" className="w-full px-3 py-2 border rounded-md" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">New Password</label>
                  <input type="password" className="w-full px-3 py-2 border rounded-md" />
                </div>
                <button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                  Change Password
                </button>
              </div>
            </div>
          )}

          {(activeTab === 'notifications' || activeTab === 'billing') && (
            <div>
              <h2 className="text-lg font-semibold mb-4">
                {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Settings
              </h2>
              <p className="text-gray-500">This section is under construction.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
