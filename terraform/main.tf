# Provider tells terraform what resource types we're using and provides a way to pass
# in specific configurations for that provider
provider "aws" {
  region                  = "us-west-2"
  shared_credentials_file = "~/.aws/credentials"
  profile                 = "default"
}

terraform {
  backend "s3" {
    profile = "default"
    bucket  = "bmf-global-tf-state-v1"
    # Important: This needs to be different in each project otherwise we will overwrite state!
    key     = "gem-sieve/terraform.tfstate"
    region  = "us-west-2"
    encrypt = true
  }
}

data "terraform_remote_state" "general-networking" {
  backend = "s3"
  config = {
    bucket = "bmf-global-tf-state-v1"
    key = "general-networking/terraform.tfstate"
    region = "us-west-2"
    profile = "default"
    encrypt = true
  }
}

locals {
  base_tags = {
    team = "bmf"
    application = "gem-sieve"
    env = "test"
  }
}
