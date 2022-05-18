# Infrastructure configuration

Or: *How to deploy a k8s cluster with gcloud-cli and terraform*.

To perform these changes, you will need: 

- GCP account
- GCP project (with billing enabled)
- kubectl (? check)

The following instructions have been tested on a machine supporting [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install).

## Google Cloud

Install [gcloud-cli](https://cloud.google.com/sdk/docs/install). Then type in your terminal:

```gcloud init```

and press Enter. 

<!-- Add here: 
1. how to add service account
2. give the right permissions (least priviledge access principle).
3. Download json file for service account [see this guide](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)
   Once the key file has been downloaded to a safe, private directory (not synced with any external service), export the environment variable:
4. export env variable.
   ```
   export GOOGLE_APPLICATION_CREDENTIALS=PATH
   ```
-->

## Terraform

Before continuing the setup, it is recommended to go (or at least *read*) through the [GCP Terraform tutorial](https://learn.hashicorp.com/collections/terraform/gcp-get-started).
This takes 30 minutes top and will enable one to better understand the HCL (*Hashicorp Configuration Language*) syntax, necessary to declare the infrastructure to deploy.

1. verify that the variables defined in `terraform.tfvars` are as intended.
2. verify that default settings in `variables.tf` are as intended.

### Validating terraform plan

Initialize terraform with `terraform init`.

In order to check whether the infrastructure specification is valid, run: `terraform plan`.

If the output looks good, you can deploy the VM to GCP with `terraform apply`.

