job "currency_converter" {
  type = "service"

  datacenters = [
    "dc1"
  ]

  vault {
    policies = [
      "nomad-server"
    ]
  }

  meta {
    submit = "[[ timeNowUTC ]]"
  }

  group "currency_converter" {
    count = 1
    update {
      max_parallel = 1
      min_healthy_time = "20s"
      healthy_deadline = "3m"
      auto_revert = true
    }

    task "currency_converter" {
      driver = "docker"
      config {
        network_mode = "host"
        image = "registry.g-host.ru/alex/currency_converter:[[ env "CI_COMMIT_SHORT_SHA" ]]"
      }

      template {
        data = <<EOH
              {{ with secret "ghost/currency_converter" }}
              BROKER_PASSWORD="{{ .Data.data.BROKER_PASSWORD }}"
              BROKER_USER="{{ .Data.data.BROKER_USER }}"
              SECRET_KEY="{{ .Data.data.SECRET_KEY }}"
              DB_PASSWORD="{{ .Data.data.DB_PASSWORD }}"
              {{ end }}
          EOH
        destination = "secrets/env"
        env = true
      }

      env {
        DB_NAME = "currency_converter"
        DB_USER = "currency_converter"
        DB_HOST = "10.0.0.6"
        DB_PORT = "5432"
        LISTEN_PORT = "${NOMAD_PORT_http}"
        PARSER_DELAY_SEC = 1800 # 30 min
        ENTRYPOINT_FILE="/app/entrypoint.sh"
      }

      resources {
        cpu = 100
        memory = 200
        network {
          mbits = 20
          port "http" {}
        }
      }

      service {
        tags = [
          "traefik.enable=true",
          "traefik.frontend.rule=Host:converter.alexue4.ru",
          "traefik.backend.healthcheck.path=/",
          "traefik.backend.healthcheck.interval=10s",
          "traefik.backend.loadbalancer.sticky=true",
        ]
        name = "currency-converter"
        port = "http"
        check {
          name = "converter.alexue4.ru instance alive"
          type = "http"
          path = "/"
          interval = "10s"
          timeout = "2s"
        }

      }

      logs {
        max_files = 2
        max_file_size = 10
      }
    }
  }
  group "currency_converter_celery" {
    count = 1

    task "currency_converter_celerybeat" {
      driver = "docker"
      config {
        network_mode = "host"
        image = "registry.g-host.ru/alex/currency_converter:[[ env "CI_COMMIT_SHORT_SHA" ]]"
      }
      template {
        data = <<EOH
              {{ with secret "ghost/currency_converter" }}
              BROKER_PASSWORD="{{ .Data.data.BROKER_PASSWORD }}"
              BROKER_USER="{{ .Data.data.BROKER_USER }}"
              SECRET_KEY="{{ .Data.data.SECRET_KEY }}"
              DB_PASSWORD="{{ .Data.data.DB_PASSWORD }}"
              {{ end }}
          EOH
        destination = "secrets/env"
        env = true
      }

      env {
        DB_NAME = "currency_converter"
        DB_USER = "currency_converter"
        DB_HOST = "10.0.0.6"
        DB_PORT = "5432"
        LISTEN_PORT = "${NOMAD_PORT_http}"
        BROKER_USER = "root"
        ENTRYPOINT_FILE = "/app/entrypoint-celery-beat.sh"
      }

      resources {
        cpu = 100
        memory = 200
        network {
          mbits = 20
        }
      }

      service {
        name = "currency-converter-celerybeat"
      }

      logs {
        max_files = 2
        max_file_size = 10
      }
    }

    task "ghost_ru_celeryd" {
      driver = "docker"
      config {
        network_mode = "host"
        image = "registry.g-host.ru/alex/currency_converter:[[ env "CI_COMMIT_SHORT_SHA" ]]"
      }
      template {
        data = <<EOH
              {{ with secret "ghost/currency_converter" }}
              BROKER_PASSWORD="{{ .Data.data.BROKER_PASSWORD }}"
              BROKER_USER="{{ .Data.data.BROKER_USER }}"
              SECRET_KEY="{{ .Data.data.SECRET_KEY }}"
              DB_PASSWORD="{{ .Data.data.DB_PASSWORD }}"
              {{ end }}
          EOH
        destination = "secrets/env"
        env = true
      }

      env {
        DB_NAME = "currency_converter"
        DB_USER = "currency_converter"
        DB_HOST = "10.0.0.6"
        DB_PORT = "5432"
        LISTEN_PORT = "${NOMAD_PORT_http}"
        C_FORCE_ROOT = "1"
        ENTRYPOINT_FILE="/app/entrypoint-celery.sh"

      }

      resources {
        cpu = 200
        memory = 200
        network {
          mbits = 20
        }
      }

      service {
        name = "currency-converter-celeryd"
      }

      logs {
        max_files = 2
        max_file_size = 10
      }
    }
  }


}