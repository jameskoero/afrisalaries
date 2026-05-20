import { useState } from "react"

const API = "https://afrisalaries.onrender.com"

const COUNTRIES = [
  {code:"KE",name:"Kenya"},
  {code:"NG",name:"Nigeria"},
  {code:"ZA",name:"South Africa"},
  {code:"GH",name:"Ghana"},
  {code:"ET",name:"Ethiopia"},
  {code:"TZ",name:"Tanzania"},
  {code:"UG",name:"Uganda"},
  {code:"RW",name:"Rwanda"},
]

const BAND_COLORS = {
  LOW:    { bg:"bg-red-900/40",    border:"border-red-500",    text:"text-red-400"    },
  MEDIUM: { bg:"bg-yellow-900/40", border:"border-yellow-500", text:"text-yellow-400" },
  HIGH:   { bg:"bg-green-900/40",  border:"border-green-500",  text:"text-green-400"  },
}

export default function App() {
  const [desc,    setDesc]    = useState("")
  const [country, setCountry] = useState("KE")
  const [result,  setResult]  = useState(null)
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)

  async function predict() {
    if (!desc.trim()) { setError("Please enter a job description."); return }
    setLoading(true); setError(null); setResult(null)
    try {
      const r = await fetch(`${API}/predict`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ description: desc, country })
      })
      if (!r.ok) throw new Error(`API error ${r.status}`)
      setResult(await r.json())
    } catch(e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const band = result?.band
  const bc   = band ? BAND_COLORS[band] : null

  return (
    <div className="min-h-screen p-4 md:p-8 max-w-2xl mx-auto">

      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-[#C9A84C] mb-1">AfriSalaries</h1>
        <p className="text-slate-400 text-sm">
          ML-powered salary intelligence for African tech roles
        </p>
        <p className="text-slate-600 text-xs mt-1">
          Stack Overflow Survey 2022–2025 · 1,526 real data points · CC BY-SA 4.0
        </p>
      </div>

      {/* Input card */}
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-5 mb-4">
        <label className="block text-sm text-[#C9A84C] font-medium mb-2">
          Job Description
        </label>
        <textarea
          rows={5}
          value={desc}
          onChange={e => setDesc(e.target.value)}
          placeholder="Paste a job description or type role details e.g. Senior Python Developer 5+ years AWS Remote Nairobi..."
          className="w-full bg-slate-900 border border-slate-600 rounded-lg p-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#C9A84C] resize-none"
        />

        <label className="block text-sm text-[#C9A84C] font-medium mt-4 mb-2">
          Country
        </label>
        <select
          value={country}
          onChange={e => setCountry(e.target.value)}
          className="w-full bg-slate-900 border border-slate-600 rounded-lg p-3 text-sm text-slate-200 focus:outline-none focus:border-[#C9A84C]"
        >
          {COUNTRIES.map(c => (
            <option key={c.code} value={c.code}>{c.name}</option>
          ))}
        </select>

        <button
          onClick={predict}
          disabled={loading}
          className="w-full mt-4 bg-[#C9A84C] hover:bg-[#b8963e] disabled:opacity-50 text-[#0A1628] font-bold py-3 rounded-lg transition-colors"
        >
          {loading ? "Analysing..." : "Predict Salary Band"}
        </button>

        {error && (
          <p className="mt-3 text-red-400 text-sm text-center">{error}</p>
        )}
      </div>

      {/* Result card */}
      {result && bc && (
        <div className={`${bc.bg} border ${bc.border} rounded-xl p-5 mb-4`}>
          <div className="flex items-center justify-between mb-4">
            <div>
              <span className={`text-4xl font-black ${bc.text}`}>{band}</span>
              <p className="text-slate-400 text-xs mt-1">{result.band_meaning}</p>
            </div>
            <div className="text-right">
              <p className="text-slate-400 text-xs">Confidence</p>
              <p className={`text-xl font-bold ${bc.text}`}>
                {Math.round(result.confidence * 100)}%
              </p>
            </div>
          </div>

          <div className="bg-slate-900/50 rounded-lg p-4 mb-4">
            <p className="text-slate-400 text-xs mb-2">Annual Salary Range (USD)</p>
            <div className="flex items-center justify-between">
              <div className="text-center">
                <p className="text-xs text-slate-500">P25</p>
                <p className="text-lg font-bold text-slate-200">
                  ${result.salary_low?.toLocaleString()}
                </p>
              </div>
              <div className="text-center">
                <p className="text-xs text-[#C9A84C]">
                  {result.country_median ? "Country Median" : "Band Median"}
                </p>
                <p className="text-2xl font-black text-[#C9A84C]">
                  ${result.salary_mid?.toLocaleString()}
                </p>
              </div>
              <div className="text-center">
                <p className="text-xs text-slate-500">P75</p>
                <p className="text-lg font-bold text-slate-200">
                  ${result.salary_high?.toLocaleString()}
                </p>
              </div>
            </div>
          </div>

          <div>
            <p className="text-slate-400 text-xs mb-2">Top Salary Drivers</p>
            <ul className="space-y-1">
              {result.top_factors?.map((f,i) => (
                <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
                  <span className="text-[#C9A84C] mt-0.5">▸</span>{f}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Disclaimer */}
      <p className="text-slate-600 text-xs text-center">
        Statistical estimates only · Base salary · Excludes equity & bonuses<br/>
        Built by James Koero · Kisumu, Kenya · github.com/jameskoero/afrisalaries
      </p>
    </div>
  )
}
