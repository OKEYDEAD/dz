СКАЧАТЬ ПЕРЕД ОТКРЫТИЕМ!!!
ТРИ ПРИМЕРА ИЗ ЗАДАНИЯ!
Примеры использования
Пример 1: Сетевая конфигурация
' IP-адреса серверов
server1_ip := 192.168.1.10
server2_ip := 192.168.1.11

{
  servers: #($server1_ip$, $server2_ip$),
  port: 8080,
  ssl: {
    enabled: true,
    cert_path: "/etc/ssl/cert.pem"
  }
}
YAML

servers:
192.168.1.1
192.168.1.11
port: 8080.0
ssl:
  enabled: true
  cert_path: /etc/ssl/cert.pem

Пример 2: Конфигурация игры
' Параметры персонажа
health := 100.0
speed := 5.5

{
  player: {
    name: "hero",
    stats: {
      health: $health$,
      speed: $speed$,
      inventory: #( "sword", "potion", 3.14 )
    }
  },
  enemies: #(
    { type: "orc", hp: 50.0 },
    { type: "dragon", hp: 500.0 }
  )
}

YAML

player:
  name: hero
  stats:
    health: 100.0
    speed: 5.5
    inventory:
    
sword
potion
3.14
enemies:
type: orc
hp: 50.0
type: dragon
hp: 500.0

Пример 3: Настройки CI/CD

timeout := 300.0
retries := 3.0

{
  pipeline: {
    stages: #("build", "test", "deploy"),
    timeout_sec: $timeout$,
    retry_policy: {
      max_retries: $retries$,
      backoff: #(1.0, 2.0, 4.0)
    }
  }
}

YAML

pipeline:
  stages:
  
build
test
deploy
timeout_sec: 300.0
retry_policy:
  max_retries: 3.0
  backoff:
1.0
2.0
4.0
