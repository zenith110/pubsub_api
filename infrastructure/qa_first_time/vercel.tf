
data "vercel_project_directory" "example" {
  path = "../../frontend/"
}

data "vercel_project" "example" {
  name = var.vercel_project_name
}

resource "vercel_deployment" "example" {
  project_id = data.vercel_project.example.id
  files      = data.vercel_project_directory.example.files
  production = false

  project_settings = {
    output_directory = "/build"
    build_command    = "CI=false npm run build"
    framework        = "create-react-app"
    root_directory   = "../../frontend/"
  }

  environment = {
    REACT_APP_PUBSUB_API_URL = cloudflare_record.qa-backend.name
  }
}