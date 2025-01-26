# run docker postgres locally
docker run -it \
 -e POSTGRES_USER="root" \
 -e POSTGRES_PASSWORD="root" \
 -e POSTGRES_DB="ny_taxi" \
 -v $(pwd)/ny_taxi_data:/var/lib/postgresql/data \
 -p 5432:5432 \
 --network=pg-network \
 --name=pg_database \
 postgres:13

# run pgadmin for postgres locally
# access via localhost:8080

docker run -it \
   -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
   -e PGADMIN_DEFAULT_PASSWORD="root" \
   -p 8080:80 \
   --network=pg-network \
   --name=pgadmin \
   dpage/pgadmin4


# run ingestion script
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
  --username=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db_name=ny_taxi \
  --table_name="yellow_taxi_trips" \
  --url=${URL}


# unpack zipped file that's downloaded from above URL
gzip -d yellow_tripdata_2021-01.csv.gz

# build ingestion container
docker build -t taxi_ingest:v001 .

# run ingest_data in network-configured build
#
docker run -it \
  --network=docker_default \
  taxi_ingest:v001 \
  --username=root \
  --password=root \
  --host=docker-pgdatabase-1 \
  --port=5432 \
  --db_name=ny_taxi \
  --table_name="yellow_taxi_trips" \
  --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"