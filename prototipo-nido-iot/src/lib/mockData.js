const now = Date.now()

export const demoDevice = {
  id: 'demo-device-01',
  public_code: 'INC-C4R7-82K1',
  pairingCode: '738914',
  name: 'Incubadora principal',
  model: 'Nido Q-01',
  status: 'online',
  last_seen_at: new Date().toISOString(),
}

export const demoUser = {
  id: 'demo-user',
  email: 'carlos@demo.pe',
  user_metadata: {
    full_name: 'Carlos Paz',
    avatar_url: '',
  },
}

export const initialReadings = Array.from({ length: 28 }, (_, index) => {
  const wave = Math.sin(index / 3.2)
  return {
    id: index + 1,
    temperature: Number((37.45 + wave * 0.18 + Math.random() * 0.08).toFixed(2)),
    humidity: Number((58.2 + Math.cos(index / 4) * 1.7 + Math.random() * 0.5).toFixed(1)),
    recorded_at: new Date(now - (27 - index) * 5 * 60 * 1000).toISOString(),
  }
})

export function createNextReading(previous) {
  const previousTemperature = previous?.temperature ?? 37.5
  const previousHumidity = previous?.humidity ?? 58
  const temperature = Math.min(38.1, Math.max(36.9, previousTemperature + (Math.random() - 0.49) * 0.09))
  const humidity = Math.min(64, Math.max(52, previousHumidity + (Math.random() - 0.5) * 0.75))

  return {
    id: crypto.randomUUID(),
    temperature: Number(temperature.toFixed(2)),
    humidity: Number(humidity.toFixed(1)),
    recorded_at: new Date().toISOString(),
  }
}
