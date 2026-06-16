import { useEffect, useMemo, useState } from 'react'
import {
  Activity,
  ArrowLeft,
  ArrowRight,
  Bell,
  Check,
  ChevronDown,
  Cloud,
  Database,
  Download,
  Droplets,
  Egg,
  Gauge,
  HardDrive,
  History,
  LayoutDashboard,
  Link2,
  LoaderCircle,
  LockKeyhole,
  LogOut,
  Menu,
  MoreHorizontal,
  QrCode,
  Radio,
  RefreshCw,
  ScanLine,
  Settings,
  ShieldCheck,
  Sparkles,
  Thermometer,
  Wifi,
  X,
} from 'lucide-react'
import { isSupabaseConfigured, supabase } from './lib/supabase'
import { createNextReading, demoDevice, demoUser, initialReadings } from './lib/mockData'

const FLOW = {
  LANDING: 'landing',
  CONNECT: 'connect',
  LOGIN: 'login',
  PAIR: 'pair',
  DASHBOARD: 'dashboard',
}

function Brand({ compact = false }) {
  return (
    <button className="brand" type="button" aria-label="Ir al inicio">
      <span className="brand-mark"><Egg size={compact ? 18 : 20} strokeWidth={2.4} /></span>
      <span>Nido<span className="brand-dot">.</span></span>
    </button>
  )
}

function GoogleIcon() {
  return (
    <svg viewBox="0 0 24 24" width="19" height="19" aria-hidden="true">
      <path fill="#4285F4" d="M21.6 12.23c0-.71-.06-1.4-.18-2.06H12v3.9h5.38a4.6 4.6 0 0 1-2 3.02v2.54h3.24c1.9-1.75 2.98-4.33 2.98-7.4Z" />
      <path fill="#34A853" d="M12 22c2.7 0 4.98-.9 6.63-2.42l-3.24-2.54c-.9.6-2.05.96-3.39.96-2.61 0-4.82-1.76-5.61-4.13H3.04v2.62A10 10 0 0 0 12 22Z" />
      <path fill="#FBBC05" d="M6.39 13.87A6.02 6.02 0 0 1 6.07 12c0-.65.11-1.29.32-1.87V7.51H3.04A10 10 0 0 0 2 12c0 1.61.39 3.14 1.04 4.49l3.35-2.62Z" />
      <path fill="#EA4335" d="M12 6c1.47 0 2.8.51 3.84 1.5l2.87-2.88A9.63 9.63 0 0 0 12 2a10 10 0 0 0-8.96 5.51l3.35 2.62C7.18 7.76 9.39 6 12 6Z" />
    </svg>
  )
}

function PublicHeader({ onConnect, onDemo }) {
  return (
    <header className="public-header shell">
      <Brand />
      <nav className="public-nav" aria-label="Navegación principal">
        <a href="#funcionamiento">Cómo funciona</a>
        <a href="#seguridad">Seguridad</a>
        <button className="nav-demo" type="button" onClick={onDemo}>Ver demostración</button>
        <button className="button button-dark button-small" type="button" onClick={onConnect}>
          Conectar dispositivo
        </button>
      </nav>
      <button className="mobile-menu" type="button" onClick={onConnect} aria-label="Conectar dispositivo">
        <Menu size={22} />
      </button>
    </header>
  )
}

function Landing({ onConnect, onDemo }) {
  return (
    <div className="landing-page">
      <PublicHeader onConnect={onConnect} onDemo={onDemo} />
      <main>
        <section className="hero shell">
          <div className="hero-copy">
            <div className="eyebrow"><span className="live-pulse" /> Monitoreo inteligente para incubadoras</div>
            <h1>Cuida cada nacimiento,<br /><span>incluso a la distancia.</span></h1>
            <p>
              Temperatura y humedad en tiempo real, alertas oportunas y un historial claro para tomar mejores decisiones durante la incubación.
            </p>
            <div className="hero-actions">
              <button className="button button-primary" type="button" onClick={onConnect}>
                Conectar mi dispositivo <ArrowRight size={18} />
              </button>
              <button className="button button-ghost" type="button" onClick={onDemo}>
                Explorar dashboard
              </button>
            </div>
            <div className="hero-trust">
              <span><ShieldCheck size={16} /> Datos protegidos</span>
              <span><Wifi size={16} /> Acceso desde cualquier lugar</span>
            </div>
          </div>

          <div className="hero-visual" aria-label="Vista previa del dashboard">
            <div className="ambient ambient-one" />
            <div className="ambient ambient-two" />
            <div className="preview-window">
              <div className="preview-topbar">
                <div className="preview-dots"><i /><i /><i /></div>
                <span>Incubadora principal</span>
                <div className="preview-avatar">CP</div>
              </div>
              <div className="preview-body">
                <div className="preview-sidebar">
                  <span className="preview-logo"><Egg size={18} /></span>
                  <i className="active"><LayoutDashboard size={17} /></i>
                  <i><Activity size={17} /></i>
                  <i><Bell size={17} /></i>
                  <i><Settings size={17} /></i>
                </div>
                <div className="preview-content">
                  <div className="preview-heading">
                    <div><small>Buenos días</small><strong>Tu incubadora está estable</strong></div>
                    <span className="status-pill"><i /> En línea</span>
                  </div>
                  <div className="preview-metrics">
                    <div className="mini-card temp">
                      <span><Thermometer size={17} /></span>
                      <small>Temperatura</small>
                      <strong>37.6<sup>°C</sup></strong>
                      <em>Rango óptimo</em>
                    </div>
                    <div className="mini-card hum">
                      <span><Droplets size={17} /></span>
                      <small>Humedad</small>
                      <strong>58<sup>%</sup></strong>
                      <em>Rango óptimo</em>
                    </div>
                  </div>
                  <div className="preview-chart-card">
                    <div className="chart-title"><span>Últimas 24 horas</span><MoreHorizontal size={17} /></div>
                    <svg viewBox="0 0 420 115" role="img" aria-label="Gráfico de temperatura">
                      <defs>
                        <linearGradient id="previewFill" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0" stopColor="#e56e3f" stopOpacity=".22" />
                          <stop offset="1" stopColor="#e56e3f" stopOpacity="0" />
                        </linearGradient>
                      </defs>
                      <path className="grid-line" d="M0 25H420M0 58H420M0 91H420" />
                      <path fill="url(#previewFill)" d="M0,78 C36,67 45,31 82,48 C123,67 140,88 178,67 C218,45 246,30 278,51 C313,75 338,37 370,43 C391,47 404,32 420,27 L420,115 L0,115Z" />
                      <path className="preview-line" d="M0,78 C36,67 45,31 82,48 C123,67 140,88 178,67 C218,45 246,30 278,51 C313,75 338,37 370,43 C391,47 404,32 420,27" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
            <div className="floating-alert">
              <span><Check size={16} /></span>
              <div><strong>Condiciones óptimas</strong><small>Actualizado hace 4 s</small></div>
            </div>
          </div>
        </section>

        <section className="steps-section shell" id="funcionamiento">
          <div className="section-kicker">Simple desde el primer minuto</div>
          <h2>Del dispositivo a tus manos en tres pasos.</h2>
          <div className="steps-grid">
            <article><span>01</span><div className="step-icon"><ScanLine size={25} /></div><h3>Identifica</h3><p>Ingresa el código impreso en el dispositivo o escanea su QR.</p></article>
            <article><span>02</span><div className="step-icon"><Link2 size={25} /></div><h3>Vincula</h3><p>Accede con Google y confirma que el dispositivo pertenece a tu cuenta.</p></article>
            <article><span>03</span><div className="step-icon"><Activity size={25} /></div><h3>Monitorea</h3><p>Consulta valores en vivo, tendencias históricas y alertas importantes.</p></article>
          </div>
        </section>

        <section className="security-strip" id="seguridad">
          <div className="shell security-inner">
            <div><ShieldCheck size={28} /><span><strong>Tu información es tuya.</strong><small>Cada cuenta solo puede consultar sus propios dispositivos.</small></span></div>
            <div className="security-points"><span><LockKeyhole size={16} /> Acceso protegido</span><span><Database size={16} /> Historial seguro</span><span><Cloud size={16} /> Respaldo opcional</span></div>
          </div>
        </section>
      </main>
    </div>
  )
}

function FlowShell({ children, onBack, step, user }) {
  const stepNumber = step === FLOW.CONNECT ? 1 : step === FLOW.LOGIN ? 2 : 3
  return (
    <div className="flow-page">
      <header className="flow-header shell">
        <Brand />
        <div className="flow-security"><LockKeyhole size={15} /> Conexión protegida</div>
      </header>
      <main className="flow-main">
        <button className="back-button" type="button" onClick={onBack}><ArrowLeft size={17} /> Volver</button>
        <div className="flow-card">
          <div className="progress-row" aria-label={`Paso ${stepNumber} de 3`}>
            {[1, 2, 3].map((value) => (
              <div key={value} className={`progress-item ${value <= stepNumber ? 'done' : ''}`}>
                <span>{value < stepNumber ? <Check size={14} /> : value}</span>
                {value < 3 && <i />}
              </div>
            ))}
          </div>
          {children}
        </div>
        <p className="flow-help">¿Necesitas ayuda? <button type="button">Consulta la guía de instalación</button></p>
      </main>
      <div className="flow-orb orb-one" /><div className="flow-orb orb-two" />
    </div>
  )
}

function DeviceCodeInput({ value, onChange, disabled }) {
  return (
    <div className="code-input-wrap">
      <QrCode size={20} />
      <input
        value={value}
        onChange={(event) => onChange(event.target.value.toUpperCase())}
        placeholder="INC-XXXX-XXXX"
        autoComplete="off"
        spellCheck="false"
        disabled={disabled}
        aria-label="Código del dispositivo"
      />
      <button type="button" title="Escanear QR" aria-label="Escanear código QR" disabled={disabled}><ScanLine size={20} /></button>
    </div>
  )
}

function ConnectStep({ onValidated, onBack }) {
  const [code, setCode] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function validateDevice(event) {
    event.preventDefault()
    setError('')
    const normalized = code.trim().toUpperCase()
    if (!normalized) {
      setError('Ingresa el código impreso en tu dispositivo.')
      return
    }

    setLoading(true)
    try {
      if (normalized === demoDevice.public_code) {
        localStorage.setItem('pending_device_code', normalized)
        onValidated(demoDevice)
        return
      }

      if (!isSupabaseConfigured) {
        setError('Código no encontrado. Para probar el prototipo usa INC-C4R7-82K1.')
        return
      }

      const { data, error: rpcError } = await supabase.rpc('preview_device', { p_public_code: normalized })
      if (rpcError) throw rpcError
      const found = Array.isArray(data) ? data[0] : data
      if (!found) {
        setError('No encontramos un dispositivo disponible con ese código.')
        return
      }
      localStorage.setItem('pending_device_code', normalized)
      onValidated({ ...found, public_code: normalized })
    } catch (requestError) {
      setError(requestError.message || 'No pudimos comprobar el dispositivo.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <FlowShell onBack={onBack} step={FLOW.CONNECT}>
      <div className="flow-icon"><ScanLine size={28} /></div>
      <div className="flow-title"><span>Paso 1 de 3</span><h1>Encuentra tu dispositivo</h1><p>Escribe el código que aparece en la etiqueta de tu incubadora.</p></div>
      <form onSubmit={validateDevice} className="flow-form">
        <label htmlFor="device-code">Código del dispositivo</label>
        <DeviceCodeInput value={code} onChange={setCode} disabled={loading} />
        <div className="input-hint"><span>Ejemplo: INC-C4R7-82K1</span><button type="button" onClick={() => setCode(demoDevice.public_code)}>Usar código demo</button></div>
        {error && <div className="form-error" role="alert">{error}</div>}
        <button className="button button-primary button-wide" type="submit" disabled={loading}>
          {loading ? <><LoaderCircle className="spin" size={18} /> Comprobando</> : <>Continuar <ArrowRight size={18} /></>}
        </button>
      </form>
      <div className="where-code"><div><QrCode size={28} /></div><span><strong>¿Dónde está el código?</strong><small>Lo encontrarás en la etiqueta lateral del dispositivo y en la tarjeta incluida en el empaque.</small></span></div>
    </FlowShell>
  )
}

function DeviceFound({ device }) {
  return (
    <div className="device-found">
      <div className="device-illustration"><Egg size={28} /><span className="device-signal"><Wifi size={13} /></span></div>
      <div><small>Dispositivo encontrado</small><strong>{device?.name || 'Incubadora IoT'}</strong><span>{device?.model || 'Nido Q-01'} · {device?.public_code}</span></div>
      <span className="available-badge"><Check size={13} /> Disponible</span>
    </div>
  )
}

function LoginStep({ device, onLoggedIn, onBack }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function signIn() {
    setLoading(true)
    setError('')
    try {
      if (!isSupabaseConfigured) {
        await new Promise((resolve) => setTimeout(resolve, 650))
        onLoggedIn(demoUser)
        return
      }
      const redirectTo = import.meta.env.VITE_APP_URL || window.location.origin
      const { error: authError } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: { redirectTo },
      })
      if (authError) throw authError
    } catch (authError) {
      setError(authError.message || 'No pudimos iniciar sesión con Google.')
      setLoading(false)
    }
  }

  return (
    <FlowShell onBack={onBack} step={FLOW.LOGIN}>
      <div className="flow-icon success"><Check size={28} /></div>
      <div className="flow-title"><span>Paso 2 de 3</span><h1>Protege tu dispositivo</h1><p>Inicia sesión para vincularlo a tu cuenta y consultar sus datos desde cualquier lugar.</p></div>
      <DeviceFound device={device} />
      <div className="login-separator"><i /><span>Continuar de forma segura</span><i /></div>
      <button className="google-button" type="button" onClick={signIn} disabled={loading}>
        {loading ? <LoaderCircle className="spin" size={19} /> : <GoogleIcon />}
        Continuar con Google
      </button>
      {error && <div className="form-error" role="alert">{error}</div>}
      {!isSupabaseConfigured && <div className="demo-notice"><Sparkles size={16} /><span>Modo demostración activo. El botón simulará un acceso con Google.</span></div>}
      <p className="privacy-copy">Usaremos tu identidad únicamente para proteger el acceso a tus dispositivos. El permiso de Google Drive se solicitará por separado.</p>
    </FlowShell>
  )
}

function PairStep({ device, user, onPaired, onBack }) {
  const [pairingCode, setPairingCode] = useState('')
  const [name, setName] = useState(device?.name || 'Incubadora principal')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function pair(event) {
    event.preventDefault()
    setError('')
    if (pairingCode.length < 6) {
      setError('Ingresa el código de vinculación de seis dígitos.')
      return
    }
    setLoading(true)
    try {
      if (!isSupabaseConfigured) {
        await new Promise((resolve) => setTimeout(resolve, 700))
        if (pairingCode !== demoDevice.pairingCode) {
          setError('Código incorrecto. En la demostración usa 738914.')
          return
        }
        localStorage.removeItem('pending_device_code')
        onPaired({ ...device, name })
        return
      }

      const { data, error: rpcError } = await supabase.rpc('claim_device', {
        p_public_code: device.public_code,
        p_pairing_code: pairingCode,
        p_device_name: name,
      })
      if (rpcError) throw rpcError
      const paired = Array.isArray(data) ? data[0] : data
      localStorage.removeItem('pending_device_code')
      onPaired(paired || { ...device, name })
    } catch (pairError) {
      setError(pairError.message || 'No pudimos vincular el dispositivo.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <FlowShell onBack={onBack} step={FLOW.PAIR} user={user}>
      <div className="flow-icon"><Link2 size={28} /></div>
      <div className="flow-title"><span>Paso 3 de 3</span><h1>Último paso</h1><p>Confirma el código secreto para asociar esta incubadora a tu cuenta.</p></div>
      <div className="account-chip"><div className="user-avatar">{initials(user)}</div><span><small>Conectando como</small><strong>{user?.user_metadata?.full_name || user?.email}</strong></span><Check size={16} /></div>
      <form className="flow-form compact" onSubmit={pair}>
        <label htmlFor="device-name">Nombre del dispositivo</label>
        <input id="device-name" className="text-input" value={name} onChange={(event) => setName(event.target.value)} />
        <label htmlFor="pair-code">Código de vinculación</label>
        <input id="pair-code" className="pin-input" inputMode="numeric" maxLength="6" value={pairingCode} onChange={(event) => setPairingCode(event.target.value.replace(/\D/g, ''))} placeholder="••••••" />
        <div className="input-hint"><span>Es diferente al ID público.</span>{!isSupabaseConfigured && <button type="button" onClick={() => setPairingCode('738914')}>Usar 738914</button>}</div>
        {error && <div className="form-error" role="alert">{error}</div>}
        <button className="button button-primary button-wide" type="submit" disabled={loading}>
          {loading ? <><LoaderCircle className="spin" size={18} /> Vinculando</> : <><Link2 size={18} /> Vincular dispositivo</>}
        </button>
      </form>
    </FlowShell>
  )
}

function initials(user) {
  const name = user?.user_metadata?.full_name || user?.email || 'Usuario'
  return name.split(/\s+/).slice(0, 2).map((part) => part[0]).join('').toUpperCase()
}

function LineChart({ readings, metric = 'temperature' }) {
  const width = 820
  const height = 260
  const padX = 14
  const padY = 22
  const values = readings.map((item) => Number(item[metric]))
  const fallback = metric === 'temperature' ? [36.8, 38.2] : [50, 65]
  const actualMin = Math.min(...values, fallback[0])
  const actualMax = Math.max(...values, fallback[1])
  const span = Math.max(0.1, actualMax - actualMin)
  const min = actualMin - span * 0.12
  const max = actualMax + span * 0.12
  const xFor = (index) => padX + (index / Math.max(1, values.length - 1)) * (width - padX * 2)
  const yFor = (value) => padY + ((max - value) / (max - min)) * (height - padY * 2)
  const points = values.map((value, index) => `${xFor(index)},${yFor(value)}`).join(' ')
  const areaPoints = `${padX},${height - padY} ${points} ${width - padX},${height - padY}`
  const lastX = xFor(values.length - 1)
  const lastY = yFor(values.at(-1) || 0)
  const gradientId = metric === 'temperature' ? 'temperatureArea' : 'humidityArea'

  return (
    <svg className={`main-chart ${metric}`} viewBox={`0 0 ${width} ${height}`} role="img" aria-label={`Historial de ${metric === 'temperature' ? 'temperatura' : 'humedad'}`}>
      <defs>
        <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="currentColor" stopOpacity=".18" />
          <stop offset="1" stopColor="currentColor" stopOpacity="0" />
        </linearGradient>
      </defs>
      {[0.15, 0.38, 0.61, 0.84].map((ratio) => <line key={ratio} x1="0" x2={width} y1={height * ratio} y2={height * ratio} className="chart-grid" />)}
      <polygon points={areaPoints} fill={`url(#${gradientId})`} />
      <polyline points={points} className="chart-polyline" />
      <line x1={lastX} x2={lastX} y1={lastY} y2={height - padY} className="chart-cursor" />
      <circle cx={lastX} cy={lastY} r="5" className="chart-point" />
    </svg>
  )
}

function MetricCard({ type, value, delta }) {
  const temperature = type === 'temperature'
  return (
    <article className={`metric-card ${temperature ? 'temperature' : 'humidity'}`}>
      <div className="metric-top">
        <div className="metric-icon">{temperature ? <Thermometer size={21} /> : <Droplets size={21} />}</div>
        <button type="button" aria-label="Más opciones"><MoreHorizontal size={20} /></button>
      </div>
      <span>{temperature ? 'Temperatura' : 'Humedad relativa'}</span>
      <strong>{value}<sup>{temperature ? '°C' : '%'}</sup></strong>
      <div className="metric-footer"><span><i /> Dentro del rango</span><small>{delta}</small></div>
    </article>
  )
}

function Sidebar({ active, setActive, onLogout }) {
  const items = [
    ['overview', LayoutDashboard, 'Resumen'],
    ['history', History, 'Historial'],
    ['alerts', Bell, 'Alertas'],
    ['devices', Radio, 'Dispositivos'],
  ]
  return (
    <aside className="dashboard-sidebar">
      <Brand compact />
      <nav>
        {items.map(([id, Icon, label]) => <button key={id} className={active === id ? 'active' : ''} type="button" onClick={() => setActive(id)}><Icon size={19} /><span>{label}</span></button>)}
      </nav>
      <div className="sidebar-bottom">
        <button type="button"><Settings size={19} /><span>Ajustes</span></button>
        <button type="button" onClick={onLogout}><LogOut size={19} /><span>Cerrar sesión</span></button>
      </div>
    </aside>
  )
}

function BackupCard({ onOpen }) {
  return (
    <article className="backup-card">
      <div className="backup-art"><HardDrive size={31} /><span><Cloud size={16} /></span></div>
      <div><strong>Respalda tu historial</strong><p>Conecta Google Drive para guardar copias periódicas de tus registros.</p></div>
      <button type="button" onClick={onOpen}>Configurar <ArrowRight size={15} /></button>
    </article>
  )
}

function BackupModal({ onClose }) {
  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={onClose}>
      <div className="modal-card" role="dialog" aria-modal="true" aria-labelledby="backup-title" onMouseDown={(event) => event.stopPropagation()}>
        <button className="modal-close" type="button" onClick={onClose}><X size={20} /></button>
        <div className="modal-icon"><HardDrive size={28} /></div>
        <span className="modal-kicker">Integración opcional</span>
        <h2 id="backup-title">Respaldo en Google Drive</h2>
        <p>Esta función guardará archivos CSV periódicos sin usar Drive como base principal del dashboard.</p>
        <div className="permission-list">
          <span><Check size={16} /> Crear únicamente los archivos del sistema</span>
          <span><Check size={16} /> No leer otros documentos de tu Drive</span>
          <span><Check size={16} /> Desconectar el permiso cuando desees</span>
        </div>
        <button className="button button-dark button-wide" type="button" onClick={onClose}><GoogleIcon /> Conectar en una próxima versión</button>
        <button className="modal-later" type="button" onClick={onClose}>Ahora no</button>
      </div>
    </div>
  )
}

function Dashboard({ user, device, readings, onLogout }) {
  const [active, setActive] = useState('overview')
  const [metric, setMetric] = useState('temperature')
  const [range, setRange] = useState('24 h')
  const [backupOpen, setBackupOpen] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const current = readings.at(-1) || { temperature: 37.6, humidity: 58 }
  const recentRows = [...readings].reverse().slice(0, 6)

  const stats = useMemo(() => {
    const temperatures = readings.map((reading) => Number(reading.temperature))
    const humidities = readings.map((reading) => Number(reading.humidity))
    const avg = (values) => values.reduce((sum, value) => sum + value, 0) / Math.max(1, values.length)
    return {
      avgTemperature: avg(temperatures).toFixed(2),
      avgHumidity: avg(humidities).toFixed(1),
      minTemperature: Math.min(...temperatures).toFixed(2),
      maxTemperature: Math.max(...temperatures).toFixed(2),
    }
  }, [readings])

  return (
    <div className="dashboard-page">
      <Sidebar active={active} setActive={setActive} onLogout={onLogout} />
      <header className="dashboard-mobile-header"><Brand compact /><button type="button" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}><Menu size={22} /></button></header>
      {mobileMenuOpen && <div className="mobile-nav-popover"><button onClick={() => setMobileMenuOpen(false)}><LayoutDashboard size={17} /> Resumen</button><button onClick={onLogout}><LogOut size={17} /> Cerrar sesión</button></div>}
      <main className="dashboard-main">
        <header className="dashboard-topbar">
          <div className="device-selector"><span className="device-selector-icon"><Egg size={19} /></span><div><small>Dispositivo activo</small><strong>{device?.name || 'Incubadora principal'}</strong></div><ChevronDown size={17} /></div>
          <div className="topbar-actions"><button type="button" className="notification-button"><Bell size={19} /><i /></button><div className="topbar-user"><div>{initials(user)}</div><span><strong>{user?.user_metadata?.full_name || 'Usuario'}</strong><small>{user?.email}</small></span><ChevronDown size={16} /></div></div>
        </header>

        <div className="dashboard-content">
          <section className="dashboard-welcome">
            <div><span className="section-kicker">Panel de monitoreo</span><h1>Buenos días, {user?.user_metadata?.full_name?.split(' ')[0] || 'Carlos'}.</h1><p>Todo marcha bien. Tu incubadora se encuentra dentro de los rangos configurados.</p></div>
            <div className="online-status"><span><i /> En línea</span><small>Último dato: ahora</small></div>
          </section>

          {!isSupabaseConfigured && <div className="mode-banner"><Sparkles size={17} /><span><strong>Modo demostración.</strong> Los valores cambian automáticamente para simular lecturas MQTT.</span><button type="button" onClick={() => setBackupOpen(true)}>Ver siguiente paso</button></div>}

          <section className="metrics-grid">
            <MetricCard type="temperature" value={current.temperature.toFixed(2)} delta={`${stats.minTemperature}° a ${stats.maxTemperature}°`} />
            <MetricCard type="humidity" value={current.humidity.toFixed(1)} delta={`Promedio ${stats.avgHumidity}%`} />
            <article className="metric-card system-card">
              <div className="metric-top"><div className="metric-icon"><Gauge size={21} /></div><button type="button"><MoreHorizontal size={20} /></button></div>
              <span>Estado del sistema</span><strong className="system-value">Estable</strong>
              <div className="metric-footer"><span><i /> Sensores activos</span><small>2 de 2</small></div>
            </article>
          </section>

          <section className="dashboard-layout">
            <article className="chart-card dashboard-card">
              <div className="card-heading">
                <div><span>Tendencia de parámetros</span><small>Promedio de temperatura: {stats.avgTemperature} °C</small></div>
                <div className="chart-controls">
                  <div className="metric-switch"><button className={metric === 'temperature' ? 'active' : ''} onClick={() => setMetric('temperature')} type="button">Temperatura</button><button className={metric === 'humidity' ? 'active' : ''} onClick={() => setMetric('humidity')} type="button">Humedad</button></div>
                  <select value={range} onChange={(event) => setRange(event.target.value)} aria-label="Rango del gráfico"><option>1 h</option><option>6 h</option><option>24 h</option></select>
                </div>
              </div>
              <div className="chart-area">
                <div className="chart-y-labels"><span>{metric === 'temperature' ? '38.5°' : '70%'}</span><span>{metric === 'temperature' ? '37.8°' : '63%'}</span><span>{metric === 'temperature' ? '37.1°' : '56%'}</span><span>{metric === 'temperature' ? '36.4°' : '49%'}</span></div>
                <LineChart readings={readings} metric={metric} />
              </div>
              <div className="chart-x-labels"><span>00:00</span><span>04:00</span><span>08:00</span><span>12:00</span><span>16:00</span><span>Ahora</span></div>
              <div className="chart-legend"><span><i className={metric} /> {metric === 'temperature' ? 'Temperatura registrada' : 'Humedad registrada'}</span><span><i className="ideal" /> Rango recomendado</span></div>
            </article>

            <aside className="right-column">
              <article className="status-card dashboard-card">
                <div className="card-heading"><div><span>Salud del dispositivo</span><small>Diagnóstico en tiempo real</small></div><RefreshCw size={18} /></div>
                <div className="health-score"><div className="score-ring"><strong>98</strong><small>/100</small></div><span><strong>Excelente</strong><small>Todos los sistemas responden</small></span></div>
                <div className="health-list">
                  <div><span><Wifi size={17} /> Conexión MQTT</span><strong className="good">Estable</strong></div>
                  <div><span><Radio size={17} /> Sensor DHT22</span><strong className="good">Activo</strong></div>
                  <div><span><Activity size={17} /> Frecuencia de datos</span><strong>Cada 5 s</strong></div>
                </div>
              </article>
              <BackupCard onOpen={() => setBackupOpen(true)} />
            </aside>
          </section>

          <section className="records-card dashboard-card">
            <div className="card-heading"><div><span>Registros recientes</span><small>Últimas lecturas recibidas del dispositivo</small></div><button className="export-button" type="button"><Download size={16} /> Exportar CSV</button></div>
            <div className="table-wrap">
              <table>
                <thead><tr><th>Fecha y hora</th><th>Temperatura</th><th>Humedad</th><th>Estado</th></tr></thead>
                <tbody>
                  {recentRows.map((reading) => <tr key={reading.id}><td>{formatDate(reading.recorded_at)}</td><td><Thermometer size={15} /> {Number(reading.temperature).toFixed(2)} °C</td><td><Droplets size={15} /> {Number(reading.humidity).toFixed(1)} %</td><td><span className="table-status"><i /> Óptimo</span></td></tr>)}
                </tbody>
              </table>
            </div>
          </section>
        </div>
      </main>
      {backupOpen && <BackupModal onClose={() => setBackupOpen(false)} />}
    </div>
  )
}

function formatDate(value) {
  return new Intl.DateTimeFormat('es-PE', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit', second: '2-digit' }).format(new Date(value))
}

function LoadingScreen() {
  return <div className="loading-screen"><Brand /><LoaderCircle className="spin" size={26} /><span>Preparando tu experiencia</span></div>
}

export default function App() {
  const [step, setStep] = useState(FLOW.LANDING)
  const [device, setDevice] = useState(null)
  const [user, setUser] = useState(null)
  const [readings, setReadings] = useState(initialReadings)
  const [booting, setBooting] = useState(isSupabaseConfigured)

  useEffect(() => {
    if (!isSupabaseConfigured) return undefined

    let mounted = true
    let subscription

    async function bootstrap() {
      const { data: sessionData } = await supabase.auth.getSession()
      const sessionUser = sessionData.session?.user || null
      if (!mounted) return
      setUser(sessionUser)

      if (sessionUser) {
        const pendingCode = localStorage.getItem('pending_device_code')
        if (pendingCode) {
          const { data } = await supabase.rpc('preview_device', { p_public_code: pendingCode })
          const found = Array.isArray(data) ? data[0] : data
          setDevice({ ...(found || {}), public_code: pendingCode })
          setStep(FLOW.PAIR)
        } else {
          const { data: devices } = await supabase.from('devices').select('*').order('created_at').limit(1)
          if (devices?.[0]) {
            setDevice(devices[0])
            const { data: storedReadings } = await supabase.from('device_readings').select('*').eq('device_id', devices[0].id).order('recorded_at', { ascending: false }).limit(80)
            if (storedReadings?.length) setReadings(storedReadings.reverse())
            setStep(FLOW.DASHBOARD)
          }
        }
      }
      setBooting(false)
    }

    bootstrap()
    const authListener = supabase.auth.onAuthStateChange((_event, session) => {
      if (!mounted) return
      setUser(session?.user || null)
      if (session?.user && localStorage.getItem('pending_device_code')) setStep(FLOW.PAIR)
    })
    subscription = authListener.data.subscription

    return () => {
      mounted = false
      subscription?.unsubscribe()
    }
  }, [])

  useEffect(() => {
    if (step !== FLOW.DASHBOARD || !device) return undefined

    if (!isSupabaseConfigured) {
      const timer = window.setInterval(() => {
        setReadings((current) => [...current.slice(-44), createNextReading(current.at(-1))])
      }, 4000)
      return () => window.clearInterval(timer)
    }

    const channel = supabase
      .channel(`readings:${device.id}`)
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'device_readings', filter: `device_id=eq.${device.id}` }, (payload) => {
        setReadings((current) => [...current.slice(-79), payload.new])
      })
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [step, device])

  async function logout() {
    if (isSupabaseConfigured) await supabase.auth.signOut()
    localStorage.removeItem('pending_device_code')
    setUser(null)
    setDevice(null)
    setReadings(initialReadings)
    setStep(FLOW.LANDING)
  }

  function openDemo() {
    setUser(demoUser)
    setDevice(demoDevice)
    setReadings(initialReadings)
    setStep(FLOW.DASHBOARD)
  }

  if (booting) return <LoadingScreen />

  if (step === FLOW.LANDING) return <Landing onConnect={() => setStep(FLOW.CONNECT)} onDemo={openDemo} />
  if (step === FLOW.CONNECT) return <ConnectStep onBack={() => setStep(FLOW.LANDING)} onValidated={(found) => { setDevice(found); setStep(FLOW.LOGIN) }} />
  if (step === FLOW.LOGIN) return <LoginStep device={device} onBack={() => setStep(FLOW.CONNECT)} onLoggedIn={(loggedUser) => { setUser(loggedUser); setStep(FLOW.PAIR) }} />
  if (step === FLOW.PAIR) return <PairStep device={device} user={user} onBack={() => setStep(FLOW.LOGIN)} onPaired={(paired) => { setDevice(paired); setReadings(initialReadings); setStep(FLOW.DASHBOARD) }} />
  return <Dashboard user={user || demoUser} device={device || demoDevice} readings={readings} onLogout={logout} />
}
