variable "credentials" {
    description = "My credentials"
    default = "./keys/my_credentials.json"
}

variable "project" {
  description = "Project"
  default     = "terraform-demo-447806"
}

variable "region" {
  description = "Region of project"
  default     = "us-west1"
}

variable "location" {
  description = "Location of the project"
  default     = "US"
}

variable "bigquery_dataset_name" {
  description = "My BigQuery Dataset name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My storage bucket name"
  default     = "terraform-demo-447806_terraform_bucket"
}

variable "gcs_storage_class" {
  description = "Bucket storage class"
  default     = "STANDARD"
}