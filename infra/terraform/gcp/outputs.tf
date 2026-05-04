output "raw_images_bucket" {
  value = google_storage_bucket.raw_images.name
}

output "processed_images_bucket" {
  value = google_storage_bucket.processed_images.name
}

output "cloud_sql_instance" {
  value = google_sql_database_instance.inspection.connection_name
}

output "workload_service_account" {
  value = google_service_account.workload.email
}

