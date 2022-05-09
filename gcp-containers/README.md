# How to deploy a k8s cluster with gcloud-cli and terraform

First a main.tf file is needed. Look at the file and [here](https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/getting_started#configuring-the-provider) to find a description of the parameters.

The last part will be an authorization part to be configured. 

But first, a service account with the right kinds of permissions needs to be created. 
A service account is needed for the cluster to initiate and manage different functionalities for the cluster to work.

## Adding credentials

If a service account isn't created, follow [this guide](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) to issue one.

Make sure the necessary permissions are provided.
For the terraform-cloud@ornate-reef-xxxxxx service account, the following permissions were worked:

- Compute Instance Admin (Beta);
- Service Networking Service Agent

One then needs to download the key file from [the service account page](https://console.cloud.google.com/projectselector2/iam-admin/serviceaccounts?supportedpurview=project) by first selecting the right project and then creating or downloading a key for that account.

Once the key file has been downloaded to a safe, private directory (not synced with any external service), export the environment variable:

```
export GOOGLE_APPLICATION_CREDENTIALS=PATH
```

where `PATH` is the filepath of the key file.
You can avoid typing this every time by adding it at the end of your `.bashrc` or `.zshenv`.

## Validating terraform plan

Initialize terraform with `terraform init`.

In order to check whether the infrastructure specification is valid, run: `terraform plan`.

If the output looks good, you can deploy the VM to GCP with `terraform apply`.

