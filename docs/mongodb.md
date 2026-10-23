# MongoDB

La aplicación usa MongoDB como base de datos para almacenar transacciones (ingresos/gastos) y deudas. Tienes tres opciones, de más simple a más robusta.

## Opción A — Instancia local para pruebas (rápida, sin instalación en el sistema)

Ideal para desarrollar o probar sin tocar el sistema operativo (no requiere `sudo` ni paquetes `apt`):

```bash
# Descargar el binario portable de MongoDB
curl -fsSL "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2204-7.0.14.tgz" -o /tmp/mongo.tgz
tar xzf /tmp/mongo.tgz -C /tmp

# Crear carpeta de datos y arrancar el servidor en segundo plano
mkdir -p ~/mongo-data
/tmp/mongodb-linux-x86_64-ubuntu2204-7.0.14/bin/mongod \
  --dbpath ~/mongo-data --port 27017 --bind_ip 127.0.0.1 \
  --logpath ~/mongo-data/mongod.log --fork
```

Verificar que quedó arriba:

```bash
/tmp/mongodb-linux-x86_64-ubuntu2204-7.0.14/bin/mongod --version
```

> Esta opción no persiste si reinicias el servidor o lo matas por error; úsala solo para desarrollo/pruebas locales.

## Opción B — MongoDB instalado en el sistema (requiere permisos de administrador)

```bash
sudo apt install -y mongodb-org
sudo systemctl enable --now mongod
```

Consulta la [guía oficial de instalación](https://www.mongodb.com/docs/manual/administration/install-on-linux/) según tu distribución.

## Opción C — MongoDB Atlas (gratuito, en la nube, recomendado para producción)

1. Crea una cuenta gratuita en [mongodb.com/atlas](https://www.mongodb.com/cloud/atlas/register).
2. Crea un clúster gratuito (*M0 Free Tier*).
3. En *Database Access*, crea un usuario con contraseña.
4. En *Network Access*, agrega la IP del servidor donde correrá el bot (o `0.0.0.0/0` para pruebas).
5. Copia el *connection string* (`mongodb+srv://usuario:contraseña@cluster.mongodb.net/`).

Esta opción es la recomendada si el bot va a correr 24/7, ya que no depende de que el servidor local esté encendido.

## Configurar la conexión

Una vez tengas MongoDB corriendo (cualquiera de las 3 opciones), indica la URI en el archivo `.env` — ver [`docs/configuracion.md`](configuracion.md).
