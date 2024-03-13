terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "topicextractor" {
  name     = "rg-topicextractor"
  location = "West Europe"
}

data "azurerm_resource_group" "quote_posters" {
  name     = "rg-quoteposters"
}

resource "azurerm_service_plan" "topicextractor" {
  name                = "asp-topicextractor"
  location            = azurerm_resource_group.topicextractor.location
  resource_group_name = azurerm_resource_group.topicextractor.name
  sku_name            = "B1"
  os_type             = "Linux"
}

data "azurerm_container_registry" "acr" {
  name                = "acrquoteposters"
  resource_group_name = data.azurerm_resource_group.quote_posters.name
}

resource "azurerm_linux_web_app" "topicextractor" {
  name                = "wa-topicextractor"
  resource_group_name = azurerm_resource_group.topicextractor.name
  location            = azurerm_service_plan.topicextractor.location
  service_plan_id     = azurerm_service_plan.topicextractor.id

  app_settings = {
    DOCKER_REGISTRY_SERVER_PASSWORD = data.azurerm_container_registry.acr.admin_password
    DOCKER_REGISTRY_SERVER_USERNAME = data.azurerm_container_registry.acr.admin_username
    DOCKER_REGISTRY_SERVER_URL = data.azurerm_container_registry.acr.login_server
  }

  site_config {
    application_stack {
      docker_image = "${data.azurerm_container_registry.acr.login_server}/${var.docker_image}"
      docker_image_tag = var.docker_image_tag
    }
  }
}