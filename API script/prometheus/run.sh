
#TODO: only run this on controller2
if docker start prometheus0; then
	true
else
docker run \
    -d \
    -p 9090:9090 \
    -v $PWD/etc_prometheus:/etc/prometheus \
    --name=prometheus0 \
    prom/prometheus
fi

if docker start grafana0; then
	true
else
docker run \
	-d \
	-p 3000:3000 \
	-v "/opt/grafana-storage:/var/lib/grafana" \
	--net="host" \
	--name=grafana0 \
	grafana/grafana
fi
