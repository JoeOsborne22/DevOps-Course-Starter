terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 2.49"
    } 
  }
  backend "azurerm" {
        resource_group_name  = "tfstate"
        storage_account_name = "tfstate13267"
        container_name       = "tfstate"
        key                  = "terraform.tfstate"
    }
}
provider "azurerm" {
  features {

  }
}

data "azurerm_resource_group" "main" {
  name     = "StandardChartered21_JosephOsborne_ProjectExercise"
}

