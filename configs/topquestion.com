#proxy_buffering on;
#proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=cache:10m max_size=32m;

upstream gunicorn {
  server localhost:8081;
}

server {
  listen 80;
  server_name topquestion.com;
  root /var/www/topquestion;
  access_log /var/www/topquestion/logs/access.log;
  error_log /var/www/topquestion/logs/error.log;    
  
  location / {
    proxy_pass http://gunicorn;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    #proxy_cache cache;
    #proxy_cache_valid any 1h;
  }

  location ^~ /uploads/ {
    root /var/www/topquestion;
  }

  location ~* \.(css|js|jpg|jpeg|png|ico)$ {
    root /var/www/topquestion;
    expires 30d;
    add_header Cache-Control private;
  }
}
