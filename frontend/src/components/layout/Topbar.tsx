import { useAuthStore } from '../../store/authStore'
import { useAuth } from '../../hooks/useAuth'

interface Props { connected: boolean }

export default function Topbar({ connected }: Props) {
  const { user }    = useAuthStore()
  const { logoutUser } = useAuth()

  return (
    <div className="h-[52px] bg-white border-b border-gray-200 flex items-center justify-between px-5 flex-shrink-0">
      <div className="flex items-center gap-2.5">
        <div className="w-[30px] h-[30px] bg-brand-500 rounded-lg flex items-center justify-center">
          <i className="ti ti-brain text-white text-base" />
        </div>
        <span className="text-sm font-medium text-gray-900">Autonomous Agent</span>
        <span className="text-[10px] text-brand-500 bg-brand-50 px-2 py-0.5 rounded-full font-medium">v1.0</span>
      </div>
      <div className="flex items-center gap-2.5">
        <div className={`flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full border ${connected ? 'text-gray-500 border-gray-200' : 'text-red-500 border-red-200'}`}>
          <div className={`w-1.5 h-1.5 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`} />
          {connected ? 'WebSocket live' : 'Disconnected'}
        </div>
        <div className="flex items-center gap-2 text-xs text-gray-500 cursor-pointer px-3 py-1.5 rounded-full border border-gray-200 hover:bg-gray-50"
          onClick={logoutUser}>
          <div className="w-5 h-5 rounded-full bg-brand-50 flex items-center justify-center text-[10px] font-medium text-brand-600">
            {user?.username?.[0]?.toUpperCase()}
          </div>
          {user?.username}
          <i className="ti ti-logout text-sm text-gray-400" />
        </div>
      </div>
    </div>
  )
}