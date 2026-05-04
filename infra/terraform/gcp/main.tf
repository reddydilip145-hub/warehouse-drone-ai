provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  name_prefix = "warehouse-drone-ai-${var.environment}"
}

resource "google_storage_bucket" "raw_images" {
  name                        = "${local.name_prefix}-raw-images"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = false
}

resource "google_storage_bucket" "processed_images" {
  name                        = "${local.name_prefix}-processed-images"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = false
}

resource "google_sql_database_instance" "inspection" {
  name             = "${local.name_prefix}-sql"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-custom-1-3840"

    backup_configuration {
      enabled = true
    }
  }
}

resource "google_sql_database" "warehouse" {
  name     = "warehouse_drone_ai"
  instance = google_sql_database_instance.inspection.name
}

resource "google_service_account" "workload" {
  account_id   = "${local.name_prefix}-svc"
  display_name = "Warehouse Drone AI workload service account"
}

