terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.21"
    }
  }
}


provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
  zone        = var.zone
}

resource "google_compute_network" "vpc_network" {
  name                    = "terraform-network"
  auto_create_subnetworks = "true"
}

resource "google_compute_instance" "vm_instance" {
  name         = "terraform-instance"
  machine_type = "e2-micro"
  tags         = ["web", "dev"]

  boot_disk {
    initialize_params {
      image = "cos-cloud/cos-stable"
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    # 
    network = google_compute_network.vpc_network.name
    access_config {
    }
  }
}

// Add if external connection is needed.
# resource "google_compute_firewall" "terraform_rule" {
#   name = "terraform-firewall-rule" 
#   network = google_compute_network.vpc_network.name
#   
#   allow {
#     protocol = "icmp"
#   }
# 
#   allow {
#     protocol = "tcp"
#     ports = ["8080"]
#   }
# 
#   source_tags = ["web"]
# }

output "ip" {
  value = google_compute_instance.vm_instance.network_interface.0.network_ip
}