variable "docker_image" {
    type = string
    description = "name of image hostring quote posters webserver, as stored in registry"
    default = "topicextractorwebserver"
}

variable "docker_image_tag" {
    type = string
    description = "tag of image hostring quote posters webserver, as stored in registry"
    default = "dev"
}