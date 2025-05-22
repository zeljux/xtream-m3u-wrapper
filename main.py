from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

@app.route('/get.php')
def get_playlist():
    username = request.args.get('username')
    password = request.args.get('password')
    file_type = request.args.get('type', 'm3u')  # Varsayılan 'm3u'
    output = request.args.get('output')  # Kullanılmasa da gelen parametre olabilir

    # Username ve password kontrol ediliyor gibi davran (isteğe bağlı)
    if not username or not password:
        return "Eksik kullanıcı adı veya şifre", 400

    if file_type in ['m3u', 'm3u_plus']:  # İkisini de destekle
        m3u_url = "https://raw.githubusercontent.com/Sakubaba00/saku/refs/heads/main/playlist1.m3u"
        try:
            response = requests.get(m3u_url, timeout=10)
            response.raise_for_status()
            return Response(response.text, mimetype='application/x-mpegURL')
        except Exception as e:
            return f"Hata oluştu: {e}", 500
    else:
        return "Desteklenmeyen 'type' parametresi.", 400

# Port ayarı
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
