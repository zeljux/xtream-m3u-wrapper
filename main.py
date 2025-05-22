from flask import Flask, request, Response, jsonify
import requests
import os

app = Flask(__name__)

# Sahte kullanıcı verisi
VALID_USERS = {
    "test": "test"
}

M3U_URL = "https://raw.githubusercontent.com/Sakubaba00/saku/refs/heads/main/playlist1.m3u"

@app.route('/get.php')
def get_playlist():
    username = request.args.get('username')
    password = request.args.get('password')
    file_type = request.args.get('type', 'm3u')

    if VALID_USERS.get(username) != password:
        return "Geçersiz kullanıcı adı veya şifre", 401

    if file_type in ['m3u', 'm3u_plus']:
        try:
            response = requests.get(M3U_URL, timeout=10)
            response.raise_for_status()
            return Response(response.text, mimetype='application/x-mpegURL')
        except Exception as e:
            return f"Hata oluştu: {e}", 500
    else:
        return "Desteklenmeyen 'type' parametresi.", 400

@app.route('/player_api.php')
def player_api():
    username = request.args.get('username')
    password = request.args.get('password')

    if VALID_USERS.get(username) == password:
        return jsonify({
            "user_info": {
                "username": username,
                "password": password,
                "status": "Active",
                "exp_date": "9999999999",
                "is_trial": "0",
                "active_cons": "1",
                "created_at": "2020-01-01",
                "max_connections": "1"
            },
            "server_info": {
                "url": request.host,
                "port": 443,
                "https_port": 443,
                "server_protocol": "http",
                "rtmp_port": "25461",
                "timezone": "Europe/Istanbul",
                "timestamp_now": "1710000000"
            }
        })
    else:
        return jsonify({"user_info": {"status": "Disabled"}})

@app.route('/xmltv.php')
def epg():
    return Response("""<?xml version="1.0" encoding="UTF-8"?><tv></tv>""", mimetype="application/xml")

# Port ayarı
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
