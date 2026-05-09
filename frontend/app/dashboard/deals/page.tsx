'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import api from '@/lib/api'

interface Deal {
  id: string
  client_id: string
  property_id: string
  stage: string
  deal_value: number
  commission_pct: number
  commission_amt: number
  notes: string
}

interface Client { id: string; full_name: string }
interface Property { id: string; title: string; price: number }

const stages = [
  { key: 'initial', label: 'تواصل أولي', color: 'border-blue-500/30 bg-blue-500/5' },
  { key: 'viewing', label: 'معاينة', color: 'border-yellow-500/30 bg-yellow-500/5' },
  { key: 'negotiating', label: 'مفاوضة', color: 'border-orange-500/30 bg-orange-500/5' },
  { key: 'contract', label: 'عقد', color: 'border-purple-500/30 bg-purple-500/5' },
  { key: 'closed', label: 'مغلقة ✅', color: 'border-green-500/30 bg-green-500/5' },
]

export default function DealsPage() {
  const router = useRouter()
  const [deals, setDeals] = useState<Deal[]>([])
  const [clients, setClients] = useState<Client[]>([])
  const [properties, setProperties] = useState<Property[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    client_id: '', property_id: '', deal_value: '', commission_pct: '2.5', notes: ''
  })

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.push('/'); return }
    Promise.all([
      api.get('/deals').then(r => setDeals(r.data)),
      api.get('/clients').then(r => setClients(r.data)),
      api.get('/properties').then(r => setProperties(r.data)),
    ]).finally(() => setLoading(false))
  }, [])

  const fetchDeals = async () => {
    const res = await api.get('/deals')
    setDeals(res.data)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await api.post('/deals', {
      ...form,
      deal_value: parseFloat(form.deal_value),
      commission_pct: parseFloat(form.commission_pct),
    })
    setShowForm(false)
    setForm({ client_id: '', property_id: '', deal_value: '', commission_pct: '2.5', notes: '' })
    fetchDeals()
  }

  const updateStage = async (id: string, stage: string) => {
    await api.patch(`/deals/${id}`, { stage })
    fetchDeals()
  }

  const getClient = (id: string) => clients.find(c => c.id === id)
  const getProperty = (id: string) => properties.find(p => p.id === id)

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
          <a href="/dashboard/clients" className="text-gray-400 hover:text-white text-sm">العملاء</a>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-bold">الصفقات</h1>
          <button onClick={() => setShowForm(!showForm)}
            className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-xl text-sm font-medium">
            + صفقة جديدة
          </button>
        </div>

        {showForm && (
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 mb-8">
            <h2 className="text-lg font-semibold mb-4">صفقة جديدة</h2>
            <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
              <select value={form.client_id} onChange={e => setForm({...form, client_id: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white" required>
                <option value="">اختر العميل</option>
                {clients.map(c => <option key={c.id} value={c.id}>{c.full_name}</option>)}
              </select>
              <select value={form.property_id} onChange={e => setForm({...form, property_id: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white" required>
                <option value="">اختر العقار</option>
                {properties.map(p => <option key={p.id} value={p.id}>{p.title}</option>)}
              </select>
              <input placeholder="قيمة الصفقة (ر.س)" type="number" value={form.deal_value}
                onChange={e => setForm({...form, deal_value: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white text-right" required />
              <input placeholder="نسبة العمولة %" type="number" step="0.1" value={form.commission_pct}
                onChange={e => setForm({...form, commission_pct: e.target.value})}
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

        {/* Pipeline */}
        {loading ? (
          <div className="text-center text-gray-400 py-20">جاري التحميل...</div>
        ) : (
          <div className="grid grid-cols-5 gap-3">
            {stages.map(stage => (
              <div key={stage.key} className={`border rounded-2xl p-4 ${stage.color}`}>
                <h3 className="text-sm font-semibold mb-3 text-center">{stage.label}</h3>
                <div className="space-y-2">
                  {deals.filter(d => d.stage === stage.key).map(deal => (
                    <div key={deal.id} className="bg-gray-900 rounded-xl p-3 text-xs">
                      <p className="font-semibold mb-1">{getClient(deal.client_id)?.full_name}</p>
                      <p className="text-gray-400 mb-2">{getProperty(deal.property_id)?.title}</p>
                      <p className="text-orange-500 font-bold">{deal.deal_value.toLocaleString()} ر.س</p>
                      <p className="text-green-400 text-xs mt-1">عمولة: {deal.commission_amt.toLocaleString()}</p>
                      <select value={deal.stage} onChange={e => updateStage(deal.id, e.target.value)}
                        className="mt-2 w-full bg-gray-800 text-gray-300 rounded-lg px-2 py-1 text-xs border border-gray-700">
                        {stages.map(s => <option key={s.key} value={s.key}>{s.label}</option>)}
                      </select>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}