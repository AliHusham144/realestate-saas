'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import api from '@/lib/api'

interface Property {
  id: string
  title: string
  type: string
  status: string
  price: number
  area_sqm: number
  bedrooms: number
  bathrooms: number
  city: string
  district: string
}

const statusColors: Record<string, string> = {
  available: 'bg-green-500/10 text-green-400 border-green-500/20',
  reserved: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
  sold: 'bg-red-500/10 text-red-400 border-red-500/20',
}

const statusLabels: Record<string, string> = {
  available: 'متاح',
  reserved: 'محجوز',
  sold: 'مباع',
}

const typeLabels: Record<string, string> = {
  apartment: 'شقة',
  villa: 'فيلا',
  land: 'أرض',
  commercial: 'تجاري',
}

export default function PropertiesPage() {
  const router = useRouter()
  const [properties, setProperties] = useState<Property[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    title: '', type: 'apartment', price: '', area_sqm: '',
    bedrooms: '0', bathrooms: '0', city: '', district: '', description: ''
  })

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.push('/'); return }
    fetchProperties()
  }, [])

  const fetchProperties = async () => {
    try {
      const res = await api.get('/properties')
      setProperties(res.data)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await api.post('/properties', {
      ...form,
      price: parseFloat(form.price),
      area_sqm: parseFloat(form.area_sqm),
      bedrooms: parseInt(form.bedrooms),
      bathrooms: parseInt(form.bathrooms),
    })
    setShowForm(false)
    setForm({ title: '', type: 'apartment', price: '', area_sqm: '', bedrooms: '0', bathrooms: '0', city: '', district: '', description: '' })
    fetchProperties()
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white" dir="rtl">
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <a href="/dashboard" className="flex items-center gap-3">
            <div className="w-9 h-9 bg-orange-500 rounded-xl flex items-center justify-center">🏠</div>
            <span className="font-bold text-lg">عقاري</span>
          </a>
        </div>
        <div className="flex items-center gap-4">
          <a href="/dashboard" className="text-gray-400 hover:text-white text-sm">الرئيسية</a>
          <a href="/dashboard/clients" className="text-gray-400 hover:text-white text-sm">العملاء</a>
          <a href="/dashboard/deals" className="text-gray-400 hover:text-white text-sm">الصفقات</a>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-bold">العقارات</h1>
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-xl text-sm font-medium"
          >
            + إضافة عقار
          </button>
        </div>

        {/* Form */}
        {showForm && (
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 mb-8">
            <h2 className="text-lg font-semibold mb-4">إضافة عقار جديد</h2>
            <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
              <input placeholder="اسم العقار" value={form.title} onChange={e => setForm({...form, title: e.target.value})}
                className="col-span-2 bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white text-right" required />
              <select value={form.type} onChange={e => setForm({...form, type: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white">
                <option value="apartment">شقة</option>
                <option value="villa">فيلا</option>
                <option value="land">أرض</option>
                <option value="commercial">تجاري</option>
              </select>
              <input placeholder="السعر (ر.س)" type="number" value={form.price} onChange={e => setForm({...form, price: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white text-right" required />
              <input placeholder="المساحة (م²)" type="number" value={form.area_sqm} onChange={e => setForm({...form, area_sqm: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white text-right" required />
              <input placeholder="عدد الغرف" type="number" value={form.bedrooms} onChange={e => setForm({...form, bedrooms: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white text-right" />
              <input placeholder="المدينة" value={form.city} onChange={e => setForm({...form, city: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white text-right" required />
              <input placeholder="الحي" value={form.district} onChange={e => setForm({...form, district: e.target.value})}
                className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white text-right" />
              <div className="col-span-2 flex gap-3 justify-end">
                <button type="button" onClick={() => setShowForm(false)}
                  className="px-4 py-2 text-gray-400 hover:text-white text-sm">إلغاء</button>
                <button type="submit"
                  className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-xl text-sm font-medium">حفظ</button>
              </div>
            </form>
          </div>
        )}

        {/* List */}
        {loading ? (
          <div className="text-center text-gray-400 py-20">جاري التحميل...</div>
        ) : properties.length === 0 ? (
          <div className="text-center text-gray-400 py-20">لا يوجد عقارات بعد</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {properties.map(p => (
              <div key={p.id} className="bg-gray-900 border border-gray-800 rounded-2xl p-5 hover:border-gray-700 transition-colors">
                <div className="flex items-start justify-between mb-3">
                  <span className={`text-xs px-2 py-1 rounded-lg border ${statusColors[p.status]}`}>
                    {statusLabels[p.status]}
                  </span>
                  <span className="text-gray-500 text-sm">{typeLabels[p.type]}</span>
                </div>
                <h3 className="font-semibold text-white mb-1">{p.title}</h3>
                <p className="text-gray-400 text-sm mb-3">📍 {p.city} — {p.district}</p>
                <p className="text-orange-500 font-bold text-lg mb-3">{p.price.toLocaleString()} ر.س</p>
                <div className="flex gap-4 text-gray-500 text-xs">
                  {p.bedrooms > 0 && <span>🛏 {p.bedrooms} غرف</span>}
                  {p.bathrooms > 0 && <span>🚿 {p.bathrooms}</span>}
                  <span>📐 {p.area_sqm} م²</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}