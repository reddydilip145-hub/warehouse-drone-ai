-- Phase 1 Cloud SQL schema for drone rack inspection.
-- Dialect target: PostgreSQL-compatible Cloud SQL.

create table facility (
  facility_id varchar(64) primary key,
  name varchar(255) not null,
  timezone varchar(64) not null,
  status varchar(32) not null default 'active',
  created_at timestamptz not null default now()
);

create table warehouse_zone (
  zone_id varchar(64) primary key,
  facility_id varchar(64) not null references facility(facility_id),
  name varchar(255) not null,
  zone_type varchar(64) not null,
  flight_allowed boolean not null default false,
  created_at timestamptz not null default now()
);

create table warehouse_location (
  location_id varchar(128) primary key,
  facility_id varchar(64) not null references facility(facility_id),
  zone_id varchar(64) not null references warehouse_zone(zone_id),
  aisle_id varchar(64) not null,
  rack_id varchar(64) not null,
  bay_id varchar(64),
  shelf_level varchar(64),
  bin_id varchar(64),
  coordinate_x numeric(12, 4),
  coordinate_y numeric(12, 4),
  coordinate_z numeric(12, 4),
  qr_marker_id varchar(128),
  flight_allowed boolean not null default false,
  inspection_required boolean not null default true,
  active boolean not null default true,
  created_at timestamptz not null default now()
);

create table sku_master (
  sku_id varchar(128) primary key,
  upc varchar(64),
  description text not null,
  category varchar(128),
  handling_class varchar(64),
  case_weight numeric(10, 3),
  length_cm numeric(10, 3),
  width_cm numeric(10, 3),
  height_cm numeric(10, 3),
  active boolean not null default true,
  created_at timestamptz not null default now()
);

create table location_sku_plan (
  location_id varchar(128) not null references warehouse_location(location_id),
  sku_id varchar(128) not null references sku_master(sku_id),
  max_capacity integer,
  min_threshold integer,
  effective_from timestamptz not null default now(),
  effective_to timestamptz,
  primary key (location_id, sku_id, effective_from)
);

create table drone_device (
  drone_id varchar(128) primary key,
  facility_id varchar(64) not null references facility(facility_id),
  name varchar(255) not null,
  device_model varchar(128),
  camera_model varchar(128),
  status varchar(32) not null default 'active',
  created_at timestamptz not null default now()
);

create table inspection_batch (
  batch_id uuid primary key,
  facility_id varchar(64) not null references facility(facility_id),
  zone_id varchar(64) not null references warehouse_zone(zone_id),
  drone_id varchar(128) not null references drone_device(drone_id),
  route_id varchar(128) not null,
  started_at timestamptz not null,
  completed_at timestamptz,
  status varchar(32) not null default 'running',
  planned_location_count integer,
  captured_location_count integer,
  created_at timestamptz not null default now()
);

create table image_capture (
  image_id uuid primary key,
  batch_id uuid not null references inspection_batch(batch_id),
  facility_id varchar(64) not null references facility(facility_id),
  location_id varchar(128) references warehouse_location(location_id),
  drone_id varchar(128) not null references drone_device(drone_id),
  idempotency_key varchar(255) not null unique,
  raw_object_key text not null,
  thumbnail_object_key text,
  captured_at timestamptz not null,
  camera_angle varchar(64),
  image_quality varchar(32) not null default 'unchecked',
  upload_status varchar(32) not null default 'uploaded',
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table model_version (
  model_version_id varchar(128) primary key,
  model_name varchar(128) not null,
  registry_uri text,
  stage varchar(32) not null,
  metrics jsonb not null default '{}'::jsonb,
  approved_by varchar(128),
  approved_at timestamptz,
  created_at timestamptz not null default now()
);

create table detection_result (
  detection_id uuid primary key,
  image_id uuid not null references image_capture(image_id),
  location_id varchar(128) references warehouse_location(location_id),
  model_version_id varchar(128) not null references model_version(model_version_id),
  expected_sku varchar(128),
  detected_sku varchar(128),
  fill_state varchar(32) not null,
  fill_percentage numeric(5, 2),
  confidence_score numeric(5, 4) not null,
  exception_type varchar(64),
  inference_status varchar(32) not null default 'completed',
  inference_latency_ms integer,
  inference_metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table inspection_event (
  inspection_id uuid primary key,
  batch_id uuid not null references inspection_batch(batch_id),
  image_id uuid not null references image_capture(image_id),
  detection_id uuid references detection_result(detection_id),
  facility_id varchar(64) not null references facility(facility_id),
  location_id varchar(128) references warehouse_location(location_id),
  drone_id varchar(128) not null references drone_device(drone_id),
  event_type varchar(64) not null,
  severity varchar(32) not null default 'medium',
  review_status varchar(32) not null default 'pending',
  created_at timestamptz not null default now()
);

create table inspection_review (
  review_id uuid primary key,
  inspection_id uuid not null references inspection_event(inspection_id),
  reviewer_id varchar(128) not null,
  decision varchar(32) not null,
  corrected_fill_state varchar(32),
  corrected_sku varchar(128),
  notes text,
  reviewed_at timestamptz not null default now()
);

create index idx_image_capture_batch on image_capture(batch_id);
create index idx_image_capture_location on image_capture(location_id);
create index idx_detection_result_location on detection_result(location_id);
create index idx_detection_result_fill_state on detection_result(fill_state);
create index idx_inspection_event_review_status on inspection_event(review_status);
create index idx_inspection_event_location on inspection_event(location_id);

