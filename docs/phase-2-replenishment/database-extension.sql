-- Phase 2 Cloud SQL extension for replenishment decisions.
-- Dialect target: PostgreSQL-compatible Cloud SQL.
-- Assumes Phase 1 tables already exist.

create table source_inventory_snapshot (
  snapshot_id uuid primary key,
  facility_id varchar(64) not null references facility(facility_id),
  location_id varchar(128) references warehouse_location(location_id),
  sku_id varchar(128) not null references sku_master(sku_id),
  available_quantity integer not null,
  reserved_quantity integer not null default 0,
  snapshot_source varchar(64) not null,
  captured_at timestamptz not null,
  created_at timestamptz not null default now()
);

create table replenishment_candidate (
  candidate_id uuid primary key,
  inspection_id uuid not null references inspection_event(inspection_id),
  facility_id varchar(64) not null references facility(facility_id),
  target_location_id varchar(128) not null references warehouse_location(location_id),
  sku_id varchar(128) not null references sku_master(sku_id),
  fill_state varchar(32) not null,
  fill_percentage numeric(5, 2),
  confidence_score numeric(5, 4) not null,
  candidate_status varchar(32) not null default 'new',
  idempotency_key varchar(255) not null unique,
  created_at timestamptz not null default now()
);

create table replenishment_recommendation (
  recommendation_id uuid primary key,
  candidate_id uuid not null references replenishment_candidate(candidate_id),
  facility_id varchar(64) not null references facility(facility_id),
  target_location_id varchar(128) not null references warehouse_location(location_id),
  source_location_id varchar(128) references warehouse_location(location_id),
  sku_id varchar(128) not null references sku_master(sku_id),
  recommended_quantity integer not null,
  priority_score integer not null,
  priority varchar(32) not null,
  execution_method varchar(64) not null,
  recommendation_status varchar(32) not null default 'pending_approval',
  decision_reasons jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table replenishment_approval (
  approval_id uuid primary key,
  recommendation_id uuid not null references replenishment_recommendation(recommendation_id),
  approver_id varchar(128) not null,
  decision varchar(32) not null,
  modified_quantity integer,
  modified_execution_method varchar(64),
  notes text,
  decided_at timestamptz not null default now()
);

create table replenishment_task (
  task_id uuid primary key,
  recommendation_id uuid not null references replenishment_recommendation(recommendation_id),
  facility_id varchar(64) not null references facility(facility_id),
  target_location_id varchar(128) not null references warehouse_location(location_id),
  source_location_id varchar(128) references warehouse_location(location_id),
  sku_id varchar(128) not null references sku_master(sku_id),
  quantity integer not null,
  execution_method varchar(64) not null,
  external_task_id varchar(128),
  task_status varchar(32) not null default 'created',
  assigned_to varchar(128),
  created_at timestamptz not null default now(),
  started_at timestamptz,
  completed_at timestamptz,
  cancelled_at timestamptz
);

create table replenishment_verification (
  verification_id uuid primary key,
  task_id uuid not null references replenishment_task(task_id),
  requested_inspection_id uuid references inspection_event(inspection_id),
  verification_status varchar(32) not null default 'requested',
  verified_fill_state varchar(32),
  verified_fill_percentage numeric(5, 2),
  notes text,
  created_at timestamptz not null default now(),
  verified_at timestamptz
);

create index idx_replenishment_candidate_status on replenishment_candidate(candidate_status);
create index idx_replenishment_candidate_target_sku on replenishment_candidate(facility_id, target_location_id, sku_id);
create index idx_replenishment_recommendation_status on replenishment_recommendation(recommendation_status);
create index idx_replenishment_recommendation_priority on replenishment_recommendation(priority, priority_score);
create index idx_replenishment_task_status on replenishment_task(task_status);
create index idx_replenishment_task_external on replenishment_task(external_task_id);

