interface Props {
  active  : string
  onChange: (page: string) => void
}

const navItems = [
  { id: 'dashboard', icon: 'ti-layout-dashboard', label: 'Dashboard' },
  { id: 'tasks',     icon: 'ti-list',             label: 'Tasks'     },
  { id: 'agents',    icon: 'ti-robot',            label: 'Agents'    },
  { id: 'tools',     icon: 'ti-tools',            label: 'Tool logs' },
  { id: 'settings',  icon: 'ti-settings',         label: 'Settings'  },
  { id: 'docs',      icon: 'ti-book',             label: 'API docs'  },
]

export default function Sidebar({ active, onChange }: Props) {
  return (
    <div className="w-[200px] bg-white border-r border-gray-200 flex flex-col gap-0.5 p-3 flex-shrink-0">
      <div className="text-[10px] font-medium text-gray-400 uppercase tracking-wider px-2.5 py-1 mb-1">Main</div>
      {navItems.slice(0, 4).map(item => (
        <button key={item.id} onClick={() => onChange(item.id)}
          className={`flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-sm cursor-pointer w-full text-left transition-colors
            ${active === item.id
              ? 'bg-brand-50 text-brand-600 font-medium'
              : 'text-gray-500 hover:bg-gray-50'}`}>
          <i className={`ti ${item.icon} text-base ${active === item.id ? 'text-brand-500' : ''}`} />
          {item.label}
        </button>
      ))}
      <div className="h-px bg-gray-100 my-2" />
      <div className="text-[10px] font-medium text-gray-400 uppercase tracking-wider px-2.5 py-1 mb-1">System</div>
      {navItems.slice(4).map(item => (
        <button key={item.id} onClick={() => onChange(item.id)}
          className={`flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-sm cursor-pointer w-full text-left transition-colors
            ${active === item.id
              ? 'bg-brand-50 text-brand-600 font-medium'
              : 'text-gray-500 hover:bg-gray-50'}`}>
          <i className={`ti ${item.icon} text-base ${active === item.id ? 'text-brand-500' : ''}`} />
          {item.label}
        </button>
      ))}
    </div>
  )
}