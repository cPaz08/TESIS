import dotenv from 'dotenv'
import mqtt from 'mqtt'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { createClient } from '@supabase/supabase-js'

const currentDirectory = dirname(fileURLToPath(import.meta.url))
dotenv.config({ path: join(currentDirectory, '.env') })

const required = ['SUPABASE_URL', 'SUPABASE_SERVICE_ROLE_KEY']
const missing = required.filter((key) => !process.env[key])
if (missing.length) {
  console.error(`Faltan variables: ${missing.join(', ')}. Copia services/.env.example como services/.env.`)
  process.exit(1)
}

const brokerUrl = process.env.MQTT_BROKER_URL || 'mqtt://broker.hivemq.com:1883'
const topic = process.env.MQTT_TOPIC || 'incubadora/+/datos'
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY, {
  auth: { persistSession: false, autoRefreshToken: false },
})

const mqttClient = mqtt.connect(brokerUrl, {
  username: process.env.MQTT_USERNAME || undefined,
  password: process.env.MQTT_PASSWORD || undefined,
  reconnectPeriod: 3000,
  connectTimeout: 15000,
  clean: true,
})

mqttClient.on('connect', () => {
  console.log(`MQTT conectado: ${brokerUrl}`)
  mqttClient.subscribe(topic, { qos: 0 }, (error) => {
    if (error) console.error('No se pudo suscribir:', error.message)
    else console.log(`Escuchando: ${topic}`)
  })
})

mqttClient.on('reconnect', () => console.log('Reconectando a MQTT...'))
mqttClient.on('error', (error) => console.error('Error MQTT:', error.message))

mqttClient.on('message', async (receivedTopic, buffer) => {
  try {
    const payload = JSON.parse(buffer.toString())
    const topicParts = receivedTopic.split('/')
    const publicCode = String(payload.deviceCode || payload.device_id || topicParts.at(-2) || '').trim().toUpperCase()
    const temperature = Number(payload.temperature ?? payload.temperatura)
    const humidity = Number(payload.humidity ?? payload.humedad)

    if (!publicCode || !Number.isFinite(temperature) || !Number.isFinite(humidity)) {
      throw new Error('El mensaje necesita deviceCode, temperature y humidity.')
    }

    const { data: device, error: deviceError } = await supabase
      .from('devices')
      .select('id, public_code')
      .eq('public_code', publicCode)
      .maybeSingle()

    if (deviceError) throw deviceError
    if (!device) throw new Error(`Dispositivo desconocido: ${publicCode}`)

    const recordedAt = payload.recordedAt || payload.timestamp || new Date().toISOString()
    const [{ error: readingError }, { error: statusError }] = await Promise.all([
      supabase.from('device_readings').insert({
        device_id: device.id,
        temperature,
        humidity,
        recorded_at: recordedAt,
      }),
      supabase.from('devices').update({
        status: 'online',
        last_seen_at: recordedAt,
        updated_at: new Date().toISOString(),
      }).eq('id', device.id),
    ])

    if (readingError) throw readingError
    if (statusError) console.warn('Lectura guardada, pero no se actualizó el estado:', statusError.message)

    console.log(`[${new Date().toLocaleTimeString()}] ${publicCode}: ${temperature} °C, ${humidity} %`)
  } catch (error) {
    console.error(`Mensaje rechazado en ${receivedTopic}:`, error.message)
  }
})
