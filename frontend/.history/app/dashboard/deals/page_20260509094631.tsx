'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import api from '@/lib/api'

interface Client {
  id: string
  full_name: string
  phone: string
  email: string
  budget: number
  interest_type: string
  status: string
  city: string
  notes: string
}

const statusColors: Record<string, string> = {
  new: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  contacted: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
  viewing: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
  negotiating: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
  closed: 'bg-green-500/10 text-green-400 border-green-500/20',
}

const statusLabels: Record<string, string> = {
  new: 'جديد', contacted: 'تم التواصل',
  viewing: 'معاينة', negotiating: 'مفاوضة', closed: 'مغلق',
}

const interestLabels: Record<string, string> = {
  apartment: 'شقة', villa: 'فيلا',
  land: 'أرض', commercial: 'تجاري', any: 'أي نوع',
}

export default function ClientsPage() {
  const router = useRouter()
  const [clients, setClients] = useState<Client[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    full_name: '', phone: '', email: '', budget: '',
    interest_type: 'any', city: '', notes: ''
  })

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.push('/'); return }
    fetchClients()
  }, [])

  const fetchClients = async () => {
    try {
      const res = await api.get('/clients')
      setClients(res.data)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await api.post('/clients', {
      ...form,
      budget: form.budget ? parseFloat(form.budget) : null,
    })
    setShowForm(false)
    setForm({ full_name: '', phone: '', email: '', budget: '', interest_type: 'any', city: '', notes: '' })
    fetchClients()
  }

  const updateStatus = async (id: string, status: string) => {
    await api.patch(`/clients/${id}`, { status })
    fetchClients()
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white" dir="rtl">
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <a href="/dashboard" className="flex items-center gap-3">
          <div className="w-9 h-9 bg-orange-500 rounded-xl flex items-center justify-center">🏠</div>
          <span className="font-bold text-lg">عقاري</span>
        </a>
        <div className="flex items-center gap-4">
          <a href="/dashboard" className="text-gray-400 hover:text-white text-sm">الرئيسية</a>
          <a href="/dashboard/properties" className="text-gray-400 hover:text-white text-sm">العقارات</a>
          <a href="/dashboard/deals" className="text-gray-400 hover:text-white text-sm">الصفقات</a>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-bold">العملاء</h1>
          <button onClick={() => setShowForm(!showForm)}
            className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-xl text-sm font-medium">
            + إضافة عميل
          </button>
        </div>

        {showForm && (
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 mb-8">
            <h2 className="text-lg font-semibold mb-4">إضافة عميل جديد</h2>
            <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
              <input placeholder="الاسم الكامل" value={form.full_name} onChange={e => setForm({...form, full_name: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white text-right" required />
              <input placeholder="رقم الجوال" value={form.phone} onChange={e => setForm({...form, phone: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white text-right" required />
              <input placeholder="الإيميل (اختياري)" value={form.email} onChange={e => setForm({...form, email: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white text-right" />
              <input placeholder="الميزانية (ر.س)" type="number" value={form.budget} onChange={e => setForm({...form, budget: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white text-right" />
              <select value={form.interest_type} onChange={e => setForm({...form, interest_type: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white">
                <option value="any">أي نوع</option>
                <option value="apartment">شقة</option>
                <option value="villa">فيلا</option>
                <option value="land">أرض</option>
              </select>
              <input placeholder="المدينة" value={form.city} onChange={e => setForm({...form, city: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white text-right" />
              <textarea placeholder="ملاحظات" value={form.notes} onChange={e => setForm({...form, notes: e.target.value})}
                className="col-span-2 bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white text-right h-20 resize-none" />
              <div className="col-span-2 flex gap-3 justify-end">
                <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 text-gray-400 text-sm">إلغاء</button>
                <button type="submit" className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-xl text-sm">حفظ</button>
              </div>
            </form>
          </div>
        )}

        {loading ? (
          <div className="text-center text-gray-400 py-20">جاري التحميل...</div>
        ) : (
          <div className="space-y-3">
            {clients.map(c => (
              <div key={c.id} className="bg-gray-900 border border-gray-800 rounded-2xl p-5 flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-gray-800 rounded-xl flex items-center justify-center text-lg">👤</div>
                  <div>
                    <p className="font-semibold">{c.full_name}</p>
                    <p className="text-gray-400 text-sm">{c.phone} · {interestLabels[c.interest_type]}</p>
                    {c.budget && <p className="text-orange-500 text-sm">{c.budget.toLocaleString()} ر.س</p>}
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <select value={c.status} onChange={e => updateStatus(c.id, e.target.value)}
                    className={`text-xs px-3 py-1.5 rounded-lg border bg-transparent cursor-pointer ${statusColors[c.status]}`}>
                    {Object.entries(statusLabels).map(([k, v]) => (
                      <option key={k} value={k} className="bg-gray-900 text-white">{v}</option>
                    ))}
                  </select>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}