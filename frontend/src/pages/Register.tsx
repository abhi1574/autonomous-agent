import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Register() {
  const [username, setUsername] = useState('')
  const [email,    setEmail   ] = useState('')
  const [password, setPassword] = useState('')
  const [showPass, setShowPass] = useState(false)
  const { register, loading, error } = useAuth()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    register(username, email, password)
  }

  return (
    <div className="min-h-screen grid grid-cols-2">

      {/* Left Panel */}
      <div className="bg-brand-600 p-12 flex flex-col justify-between">
        <div>
          <div className="flex items-center gap-3 mb-12">
            <div className="w-9 h-9 bg-white/20 rounded-xl flex items-center justify-center">
              <i className="ti ti-brain text-white text-xl" />
            </div>
            <span className="text-white font-medium text-lg">Autonomous Agent</span>
          </div>
          <h1 className="text-3xl font-medium text-white leading-snug mb-4">
            Create your account
          </h1>
          <p className="text-white/70 text-sm leading-relaxed mb-10">
            Join and start running intelligent multi-agent tasks in minutes.
          </p>
          <div className="bg-white/10 rounded-xl p-5">
            <div className="text-white text-sm font-medium mb-3">What you get</div>
            <div className="flex flex-col gap-3">
              {[
                'Access to 5 specialist AI agents',
                'Real-time task pipeline visualization',
                'Vector memory across all tasks',
                'Full tool call analytics',
                'WebSocket live feed',
              ].map(item => (
                <div key={item} className="flex items-center gap-2 text-white/80 text-sm">
                  <i className="ti ti-check text-green-300 text-sm flex-shrink-0" />
                  {item}
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="text-white/40 text-xs">
          FastAPI · React · PostgreSQL · Redis · Qdrant
        </div>
      </div>

      {/* Right Panel */}
      <div className="bg-white flex items-center justify-center p-12">
        <div className="w-full max-w-sm">
          <h2 className="text-2xl font-medium text-gray-900 mb-1">Create account</h2>
          <p className="text-sm text-gray-500 mb-8">Fill in your details to get started</p>

          {error && (
            <div className="flex items-center gap-2 bg-red-50 border border-red-200 rounded-lg px-4 py-3 mb-5 text-red-700 text-sm">
              <i className="ti ti-alert-circle text-base flex-shrink-0" />
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div>
              <label className="text-xs font-medium text-gray-600 mb-1.5 block">Username</label>
              <div className="relative">
                <i className="ti ti-user absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-base" />
                <input type="text" value={username} onChange={e => setUsername(e.target.value)}
                  placeholder="Choose a username"
                  className="w-full h-10 pl-9 pr-3 text-sm border border-gray-200 rounded-lg bg-gray-50 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-50 focus:bg-white" />
              </div>
            </div>

            <div>
              <label className="text-xs font-medium text-gray-600 mb-1.5 block">Email</label>
              <div className="relative">
                <i className="ti ti-mail absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-base" />
                <input type="email" value={email} onChange={e => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  className="w-full h-10 pl-9 pr-3 text-sm border border-gray-200 rounded-lg bg-gray-50 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-50 focus:bg-white" />
              </div>
            </div>

            <div>
              <label className="text-xs font-medium text-gray-600 mb-1.5 block">Password</label>
              <div className="relative">
                <i className="ti ti-lock absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-base" />
                <input type={showPass ? 'text' : 'password'} value={password} onChange={e => setPassword(e.target.value)}
                  placeholder="Create a password"
                  className="w-full h-10 pl-9 pr-10 text-sm border border-gray-200 rounded-lg bg-gray-50 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-50 focus:bg-white" />
                <button type="button" onClick={() => setShowPass(!showPass)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                  <i className={`ti ${showPass ? 'ti-eye-off' : 'ti-eye'} text-base`} />
                </button>
              </div>
            </div>

            <button type="submit" disabled={loading}
              className="w-full h-10 bg-brand-500 hover:bg-brand-600 text-white text-sm font-medium rounded-lg flex items-center justify-center gap-2 disabled:opacity-50 mt-1">
              <i className="ti ti-user-plus text-base" />
              {loading ? 'Creating account...' : 'Create account'}
            </button>
          </form>

          <p className="text-center text-xs text-gray-400 mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-brand-600 font-medium hover:underline">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  )
}