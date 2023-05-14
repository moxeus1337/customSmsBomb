# customSmsBomb
[![Version](https://img.shields.io/badge/Version-1.0.0-green)]()
[![Python](https://img.shields.io/badge/Python-v3.10.0-yellow)]()

Herhangi bir SmsBomber'ın API'lerinin kolaylıkla entegre edilebileceği bir SmsBomber.</br>
Elinde API'si bulunup SmsBomber'a eklemek isteyenler için, __[Geliştirme](https://github.com/x000001x/customSmsBomb#Geliştirme)__.

## Gereklilikler
- Python *3.10+*

## Özellikleri 
- Multithread & Proxy desteği.
- Eşzamanlı çoklu hedef desteği.
- Desteklenen sitelerden otomatik Proxy listesi indirme.
- Yeni API bulunduğunda kolayca kod yazmadan programa eklenebilmesi.

## API Listesi
Bu programın amacı başka SmsBomber'ların API'leri tek bir çatı altında toplamak. 
Bu amaç doğrultusunda şuanlık API'leri entegre edilmiş __2__ SmsBomber vardır.
- __[75hz1](https://github.com/75hz1/SmsBomb)__
- __[TBomb](https://github.com/TheSpeedX/TBomb)__

_Sadece __Türkiye__'de çalışan API'ler alınmıştır._

## Kurulum
```
pip install -r requirements.txt
```

### Desteklenen Proxy Siteleri
* [proxyscrape](https://proxyscrape.com/free-proxy-list) -> `pxscrape:http`

## Kullanım
```
usage: main.py [-h] -p PHONES [-m MAILS] [-c COUNT] [-x PROXY] [-th THREAD]

optional arguments:
  -h, --help            show this help message and exit
  -p PHONES, --phones PHONES
                        Sms gönderilecek numara veya liste dosyası.
  -m MAILS, --mails MAILS
                        Mail gönderilecek mail ceya liste dosyası
  -c COUNT, --count COUNT
                        Gönderilecek sms sayısı veya liste dosyası
  -x PROXY, --proxy PROXY
                        Proxy dosya ismi veya indirme site ismi
  -th THREAD, --thread THREAD
                        Telefon başına düşen thread sayısı
```
## Örnek Kullanım
```
# Normal kullanım
python main.py -p 5555555555 -m mail@gmail.com -x proxies.txt:http -th 4 -c 100

# Eğer -m parametresi girilmesse mail adresi rastgele üretilir.
# Eğer -x parametresi girilmesse proxy kullanılmaz.
# Eğer -x parametresine desteklenen site adı girilirse o sitedeki en gücel proxy listesini indirir.
# Örneğin -x pxscrape:http
# Eğer -th parametresi girilmesse her telefona 1 thread düşer.
# Eğer -c parametresi girilmesse sonsuza dek gönderir.

python main.py -p victims.txt -m victims.txt -x proxies:http -th 4 -c victims.txt
# Bu kod 'victims.txt' de bulunan tüm numarala dosyada her numara için ayrıca belirtilen sayı kadar eşzamanlı olarak mesaj gönderir.

// victims.txt
5555555555 mail@gmail.com 100
5555555554 mail2@gmail.com 50

# Eğer mail yerine * işareti girilirse mail rastgele üretilir.
// victims.txt
5555555555 * 100 
5555555554 mail2@gmail.com 50
# 5555555555 için mail rastgele üretilecek

# Eğer -c parametresine "victims.txt" yerine 1 sayı girilirse tüm numaralara o sayı kadar gönderilir.
python main.py -p victims.txt -m victims.txt -x proxies:http -th 4 -c 100
# Bu kod 5555555555 ve 5555555554 numarasına 100 tane sms gönder demektir.

# EK BİLGİ ÖNEMLİ
# Proxy için -x parametresine dosya ismi (proxies.txt) girildikten sonra ":" koyup proxy tipini belirtmek gerekiyor.
# Örneğin : proxies.txt:http 
```

## Geliştirme
Eğer elinizde yeni bir API varsa, kolayca SmsBomber'a ekleyebilirsiniz.</br>
Eğer API'yi Github da SmsBomber'a ekletmek istiyorsanız _[Discord](https://discordapp.com/users/1093922128698556498)_.

## API Ekleme
API bilgileri __2__ formatta tutulur.
- __[JSON](api/params.json)__
- __[Code](api/payloads_manager/custom_payloads.py)__

### Ortak Parametreler
- JSON formatında her API için ortak olarak bulunan bazı parametreler vardır.
- Bu parametreler :
  - `name`
  - `payload`
- `name` parametresi API'nin ismini belirtir.
- `payload` parametresi ise _[requests](https://pypi.org/project/requests/)_ paketiylen yapılacak bir HTTP isteğine `**kwargs` olarak iletilecektir.
- Bunlara ek olarak bazı özel ifadeler JSON formatında bazı değişkenleri temsil eder. Bu ifadeler:
  - `%%PHONE_NUMBER%%`
  - `%%MAIL_ADDRESS%%`
- İlk ifade telefon numarasını temsil ederken 2. ifade mail adresini temsil eder.
- Aşağıdaki örnekteki JSON formatındaki API'nin Python'daki karşılığı: 
  - `requests.post(url="https://api.company.com/sendSms", json={"phone": self.phone})`
- Örnek API
```json
"payload": {
    "url": "https://api.company.com/sendSms",
    "json": {
        "phone": "%%PHONE_NUMBER%%"
    }
}
``` 

### JSON
- İlk baştaki JSON anahtarı _[requests](https://pypi.org/project/requests/)_ paketiyle hangi metodun yapılacağını belirler.
- Method anahtarları :
  - `post`
  - `get`
  - `put`
  - `customMethods`
- Kullanılan API'nin başarılı sonuç verip vermediğini test etmek için __3__ tane yöntem vardır.
- Metod anahtarlarının içindeki __3__ doğrulama yöntemi :
  - `json`
  - `statusCode`
  - `custom`

**Doğrulama Algoritması**
- Standart olarak HTTP isteği yapıldıktan sonra _[requests](https://pypi.org/project/requests/)_ paketinin dödürdüğü yanıt objesi alınır.
- Doğrulama metoduna göre yanıt objesi doğrulama fonksiyonuna gönderilir. 

**Doğrulama Fonksiyonları**
- JSON Tabanlı
  - JSON yanıtındaki `validatePath` yolundaki değer eğer `validateData`'ya eşitse sms başarıyla gönderilmiş demektir. 
  - `validatePath` JSON formatında `yol1.yol2.yol3` şeklinde belirtilmelidir.
  - `yol1.yol2.yol3` değerinin Python'daki karşılığı: `r.json()["yol1"][["yol2"]["yol3"]` olacaktır.
- statusCode Tabanlı
  - Yanıt objesindeki `status_code` değeri `validatePath` değerindeki koda eşitse sms başarıyla gönderilmiş demektir. 
  - `statusCode` tabanlı doğrulamada `validatePath` değerinin olması gerekmez.
 
 API'lerin JSON formatını daha iyi anlamak istiyorsanız __[params](api/params.json)__ dosyasını inceleyebilirsiniz.
 
### Code
- Bu formattaki API'ler doğrudan __[CustomPayloads](api/payloads_manager/custom_payloads.py)__ sınıfına fonksiyon olarak kaydedilir.
- Özellikle JSON formatına uymayan, token alınması gereken veya birden fazla HTTP isteğinin yapıldığı API'ler için kullanışlıdır.

**Tanımlama**
- Aldıkları tek JSON anahtarı `methodName`'dir. 
- `methodName` değeri __[CustomPayloads](api/payloads_manager/custom_payloads.py)__ sınıfındaki fonksiyon ismi ile aynı olmalıdır.
- API'lerin bilgilerinin tutulduğu __[params](api/params.json)__ dosyasında en altta bulunan `customMethods` içindeki `custom` değerinin içine tanımlanırlar.
- Fonksiyon isminin sonuna `_custom` eklenmesi gereklidir. 
- `methodName` değerine fonksiyon ismi `_custom` olmadan yazılmalıdır.

**API Fonksiyonu**
- __[CustomPayloads](api/payloads_manager/custom_payloads.py)__ sınıfında tanımlanır.
- _[requests](https://pypi.org/project/requests/)_ paketinin dödürdüğü yanıt objesi döndürülmelidir.
- Arg olarak sadece Proxy fonksiyona iletilir.
- İstenen kod yazılabilir.

**Doğrulama Fonksiyonu**
- Fonksiyona sadece _[requests](https://pypi.org/project/requests/)_ paketinin döndürdüğü yanıt objesi iletilir.
- __[CustomChecker](api/check/custom_check.py)__ sınıf içinde tanımlanırlar.
- Her custom API'nin kendi doğrulama fonksiyonu olmalıdır.
- Eğer fonksiyon `True` döndürürse başarılı olmuş demektir.
- Eğer fonksiyon `False` dödürürse başarısız olmuş demektir.
- Fonksiyon ismi `methodName` değeri ile aynı olmalıdır ve sonuna `_custom_check` eklenmelidir.
- Mümkünse statik veya sınıf metodu olmalıdırlar.

**Örnek**
```python
# API fonksiyonu
def kahvedunyasi_custom(self, proxy):
    url = "https://core.kahvedunyasi.com/api/users/sms/send"
    data={"mobile_number": self.phone, "token_type": "register_token"}
    response = requests.post(url, data=data, proxies=proxy)
    return response 

# Doğrulama fonksiyonu
@staticmethod
def kahvedunyasi_custom_check(response_obj):
    message = response_obj.json()["meta"]["messages"]["error"]
    if len(message) == 0:
        return True

# JSON formatındaki tanımı
"customMethods": {
    "json": [],
    "statusCode": [],
    "custom": [
        {
            "name": "KahveDunyasi",
            "methodName": "kahvedunyasi",
            "payload": {}
        }
    ]
}
```
----
#### SORUMLULUK REDDİ
> PROGRAM VE TÜM BİLGİLER "OLDUĞU GİBİ" SAĞLANMAKTADIR. AÇIK VEYA ÖRTÜLÜ, BELİRLİ BİR AMACA UYGUNLUK VEYA İHLAL ETMEME GARANTİLERİ DE DAHİL ANCAK BUNLARLA SINIRLI OLMAMAK KAYDIYLA HERHANGİ BİR TÜRDE GARANTİ YOKTUR. YAZARLAR VEYA TELİF HAKKI SAHİPLERİ, YAZILIMLA VEYA YAZILIMIN KULLANIMIYLA BAĞLANTILI OLARAK ORTAYA ÇIKAN HERHANGİ BİR İDDİA, HASAR VEYA DİĞER SORUMLULUK İÇİN SÖZLEŞME HAKLARI, HAKSIZ FİİL HAKLARI VEYA DİĞER HUKUK TEORİLERİNİ KULLANARAK HERHANGİ BİR SORUMLULUK KABUL ETMEZLER.
>
>Burada sağlanan herhangi bir kod veya bilgiyi kullanarak yukarıdaki Feragatname'nin tüm parçalarına uymayı kabul edersiniz.

#### DISCLAIMER

> THE SOFTWARE AND ALL INFORMATION HERE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
>
> By using any code or information provided here you are agreeing to all parts of the above Disclaimer. 
