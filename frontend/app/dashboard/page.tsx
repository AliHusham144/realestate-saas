'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import api from '@/lib/api'

interface Stats {
  total_properties: number
  available_properties: number
  reserved_properties: number
  sold_properties: number
  total_clients: number
  new_clients: number
  active_clients: number
  total_deals: number
  open_deals: number
  closed_deals: number
  total_commission: number
  avg_deal_value: number
}

export default function DashboardPage() {
  const router = useRouter()
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.push('/'); return }
    api.get('/stats')
      .then(res => setStats(res.data))
      .catch(() => { localStorage.removeItem('token'); router.push('/') })
      .finally(() => setLoading(false))
  }, [router])

  const logout = () => {
    localStorage.removeItem('token')
    router.push('/')
  }

  if (loading) return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="text-orange-500 text-xl">جاري التحميل...</div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-950 text-white" dir="rtl">
      {/* Navbar */}
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-orange-500 rounded-xl flex items-center justify-center text-lg">🏠</div>
          <span className="font-bold text-lg">عقاري</span>
        </div>
        <div className="flex items-center gap-4">
          <a href="/dashboard/properties" className="text-gray-400 hover:text-white text-sm">العقارات</a>
          <a href="/dashboard/clients" className="text-gray-400 hover:text-white text-sm">العملاء</a>
          <a href="/dashboard/deals" className="text-gray-400 hover:text-white text-sm">الصفقات</a>
          <button onClick={logout} className="text-gray-500 hover:text-red-400 text-sm">خروج</button>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold mb-8">لوحة التحكم</h1>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <StatCard label="إجمالي العقارات" value={stats?.total_properties} color="orange" />
          <StatCard label="متاح" value={stats?.available_properties} color="green" />
          <StatCard label="محجوز" value={stats?.reserved_properties} color="yellow" />
          <StatCard label="مباع" value={stats?.sold_properties} color="red" />
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <StatCard label="إجمالي العملاء" value={stats?.total_clients} color="blue" />
          <StatCard label="عملاء جدد" value={stats?.new_clients} color="purple" />
          <StatCard label="صفقات مفتوحة" value={stats?.open_deals} color="orange" />
          <StatCard label="صفقات مغلقة" value={stats?.closed_deals} color="green" />
        </div>

        {/* Financial */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
            <p className="text-gray-400 text-sm mb-1">إجمالي العمولات</p>
            <p className="text-3xl font-bold text-orange-500">
              {stats?.total_commission.toLocaleString()} ر.س
            </p>
          </div>
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
            <p className="text-gray-400 text-sm mb-1">متوسط قيمة الصفقة</p>
            <p className="text-3xl font-bold text-blue-400">
              {stats?.avg_deal_value.toLocaleString()} ر.س
            </p>
          </div>
        </div>
      </main>
    </div>
  )
}

function StatCard({ label, value, color }: { label: string, value?: number, color: string }) {
  const colors: Record<string, string> = {
    orange: 'text-orange-500', green: 'text-green-400',
    yellow: 'text-yellow-400', red: 'text-red-400',
    blue: 'text-blue-400', purple: 'text-purple-400',
  }
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
      <p className="text-gray-400 text-xs mb-2">{label}</p>
      <p className={`text-3xl font-bold ${colors[color]}`}>{value ?? 0}</p>
    </div>
  )
}