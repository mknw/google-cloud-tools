provider "google" {
   project = "ornate-reef-342810"
   region  = "europe-west1"
   zone    = "europe-west1-b"

}

resource "google_compute_instance" "vm_instance" { 
   name = "terraform-instance"
   machine_type = "e2-micro"

   boot_disk { 
      initialize_params {
         image = "debian-cloud/debian-9"
      }
   }
   
   network_interface {
      # A default network is created for all GCP projects
      network = "default"
      access_config {
      }
   }
}

resource "google_compute_network" "vpc_network" {
   name                    = "terraform-network"
   auto_create_subnetworks = "true"
}