-- Nido IoT: esquema inicial para Supabase
-- Ejecuta este archivo completo en SQL Editor dentro de tu proyecto Supabase.

create extension if not exists pgcrypto;

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text,
  avatar_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.devices (
  id uuid primary key default gen_random_uuid(),
  public_code text not null unique,
  pairing_code_hash text not null,
  name text not null default 'Incubadora IoT',
  model text not null default 'Nido Q-01',
  owner_id uuid references auth.users(id) on delete set null,
  status text not null default 'offline' check (status in ('online', 'offline', 'maintenance')),
  last_seen_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.device_readings (
  id bigint generated always as identity primary key,
  device_id uuid not null references public.devices(id) on delete cascade,
  temperature numeric(5,2) not null check (temperature between -40 and 100),
  humidity numeric(5,2) not null check (humidity between 0 and 100),
  recorded_at timestamptz not null default now(),
  created_at timestamptz not null default now()
);

create index if not exists idx_devices_owner on public.devices(owner_id);
create index if not exists idx_device_readings_device_time on public.device_readings(device_id, recorded_at desc);

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, full_name, avatar_url)
  values (
    new.id,
    coalesce(new.raw_user_meta_data ->> 'full_name', new.raw_user_meta_data ->> 'name'),
    new.raw_user_meta_data ->> 'avatar_url'
  )
  on conflict (id) do update
    set full_name = excluded.full_name,
        avatar_url = excluded.avatar_url,
        updated_at = now();
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
after insert or update on auth.users
for each row execute procedure public.handle_new_user();

create or replace function public.preview_device(p_public_code text)
returns table (
  public_code text,
  name text,
  model text,
  available boolean
)
language sql
security definer set search_path = public
as $$
  select d.public_code, d.name, d.model, d.owner_id is null
  from public.devices d
  where upper(d.public_code) = upper(trim(p_public_code))
    and d.owner_id is null
  limit 1;
$$;

create or replace function public.claim_device(
  p_public_code text,
  p_pairing_code text,
  p_device_name text default null
)
returns setof public.devices
language plpgsql
security definer set search_path = public
as $$
declare
  claimed_device public.devices;
begin
  if auth.uid() is null then
    raise exception 'Debes iniciar sesión para vincular un dispositivo.';
  end if;

  update public.devices
  set owner_id = auth.uid(),
      name = coalesce(nullif(trim(p_device_name), ''), name),
      updated_at = now()
  where upper(public_code) = upper(trim(p_public_code))
    and owner_id is null
    and pairing_code_hash = crypt(trim(p_pairing_code), pairing_code_hash)
  returning * into claimed_device;

  if claimed_device.id is null then
    raise exception 'Código de vinculación incorrecto o dispositivo no disponible.';
  end if;

  return next claimed_device;
end;
$$;

revoke all on function public.preview_device(text) from public;
grant execute on function public.preview_device(text) to anon, authenticated;

revoke all on function public.claim_device(text, text, text) from public;
grant execute on function public.claim_device(text, text, text) to authenticated;

alter table public.profiles enable row level security;
alter table public.devices enable row level security;
alter table public.device_readings enable row level security;

drop policy if exists "profiles_select_own" on public.profiles;
create policy "profiles_select_own"
on public.profiles for select
to authenticated
using ((select auth.uid()) = id);

drop policy if exists "profiles_update_own" on public.profiles;
create policy "profiles_update_own"
on public.profiles for update
to authenticated
using ((select auth.uid()) = id)
with check ((select auth.uid()) = id);

drop policy if exists "devices_select_owned" on public.devices;
create policy "devices_select_owned"
on public.devices for select
to authenticated
using ((select auth.uid()) = owner_id);

drop policy if exists "devices_update_owned" on public.devices;
create policy "devices_update_owned"
on public.devices for update
to authenticated
using ((select auth.uid()) = owner_id)
with check ((select auth.uid()) = owner_id);

drop policy if exists "readings_select_owned" on public.device_readings;
create policy "readings_select_owned"
on public.device_readings for select
to authenticated
using (
  exists (
    select 1
    from public.devices d
    where d.id = device_readings.device_id
      and d.owner_id = (select auth.uid())
  )
);

do $$
begin
  alter publication supabase_realtime add table public.device_readings;
exception
  when duplicate_object then null;
end $$;

insert into public.devices (public_code, pairing_code_hash, name, model)
values (
  'INC-C4R7-82K1',
  crypt('738914', gen_salt('bf')),
  'Incubadora principal',
  'Nido Q-01'
)
on conflict (public_code) do nothing;
