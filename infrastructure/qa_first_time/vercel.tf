
data "vercel_project_directory" "example" {
  path = "../../frontend/"
}

data "vercel_project" "example" {
  name = "pubsub-api"
}

resource "vercel_deployment" "example" {
  project_id = data.vercel_project.example.id
  files      = data.vercel_project_directory.example.files
  production = false

  project_settings = {
    output_directory = "/build"
    build_command    = "npm run build"
    framework        = "create-react-app"
    root_directory   = ""
  }

  environment = {
    REACT_APP_PUBSUB_API_URL = cloudflare_record.qa-backend.name
  }
}