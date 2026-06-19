
# 🔥 ReconX - Subdomain & HTTP Reconnaissance Toolkit

**ReconX** adalah tools all-in-one untuk **Bug Bounty** dan **Penetration Testing** yang menggabungkan kekuatan **Subfinder** (nyari subdomain) sama **Httpx** (ngecek host hidup).

---

## 🚀 Fitur Unggulan

| Fitur | Deskripsi |
|-------|-----------|
| ⚡ **Super Cepat** | Multi-threading sampe 100 thread |
| 🎯 **Akurat** | Deteksi status code, judul, teknologi website |
| 📁 **Export Data** | Hasil scan ke `.txt` dan `.json` |
| 🤫 **Mode Pasif** | OSINT only, tanpa DNS resolution |
| 🔄 **Follow Redirects** | Ikuti redirect 301/302 |

---

## 📦 Instalasi
git clone https://github.com/daffazxxs/ReconX.git
cd ReconX


##Cara Pakai 
python3 reconx.py -d target.com

##Scan dengan export 
python3 reconx.py -d target.com --export -t 100

##MODE pasif(OSINT ONLY)
python3 reconx.py -d target.com --passive

##Scan dengan follow redirects
python3 reconx.py -d target.com --follow

# Install Subfinder
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Install Httpx
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

terimakasih projectdiscovery izin memakai tools kalian 

## 🛠️ Options Lengkap

| Flag | Deskripsi |
|------|-----------|
| `-d, --domain` | Domain target (wajib) |
| `-o, --output` | File output subdomain |
| `-l, --live` | File output live host |
| `--passive` | Mode pasif (OSINT only) |
| `-t, --threads` | Jumlah threads (default: 50) |
| `--no-title` | Skip title detection |
| `--no-tech` | Skip tech detection |
| `--no-status` | Skip status code |
| `--follow` | Follow redirects |
| `--export` | Export ke file |
| `-v, --verbose` | Verbose mode |




# Install Python dependencies
pip install colorama
