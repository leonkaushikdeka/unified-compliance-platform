import { Outlet, Link, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { clsx } from 'clsx'

const navigation = [
  { name: 'Dashboard', href: '/' },
  { name: 'Frameworks', href: '/frameworks' },
  { name: 'Assessments', href: '/assessments' },
  { name: 'DPDP', href: '/dpdp' },
  { name: 'Reports', href: '/reports' },
  { name: 'Settings', href: '/settings' },
]

export default function Layout() {
  const location = useLocation()

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex h-16 bg-white shadow">
        <div className="flex items-center px-4">
          <span className="text-xl font-bold text-primary-600">Compliance Platform</span>
        </div>
        <div className="flex items-center ml-auto px-4 space-x-4">
          <span className="text-sm text-gray-600">user@example.com</span>
        </div>
      </div>

      <div className="flex">
        <aside className="w-64 bg-white shadow hidden md:block">
          <nav className="mt-5 px-2">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={clsx(
                  'mt-1 px-3 py-2 rounded-md text-sm font-medium',
                  location.pathname === item.href
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-gray-600 hover:bg-gray-50'
                )}
              >
                {item.name}
              </Link>
            ))}
          </nav>
        </aside>

        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
