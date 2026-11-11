# Linux Önyükleme Sürecine Genel Bakış

Bir bilgisayarın güç düğmesine basılmasından kullanıcı kabuğunun hazır olmasına kadar, kontrol farklı yazılım katmanları arasında el değiştirir. Her aşama bir sonrakine gerekli donanım ve çalışma ortamını hazırlar. Bu zinciri anlamak için açılışı tek bir programın yaptığı iş gibi değil, birbirini izleyen hazırlık ve devir adımları olarak düşünmek gerekir.

Önyüklemenin ilk kısmında firmware donanımı başlatır ve işletim sistemini yükleyecek önyükleyiciyi bulur. Önyükleyici çekirdeği çalışmaya hazırlar; çekirdek donanımı ve sistemin temel kaynaklarını yönetmeye başlar. Çekirdek gerçek kök dosya sistemine ulaşabilmek için gerekiyorsa initramfs ortamını çalıştırır. Ardından gerçek sistemin init süreci servisleri başlatır ve kullanıcıya terminal ya da grafik oturumu sunulur.

## Açılışın ana aşamaları

| Sıra | Aşama | Temel görevi |
|---|---|---|
| 1 | BIOS veya UEFI firmware | Açılışta temel donanım kontrollerini yapar, önyükleme aygıtını ve yolunu belirler; uygun önyükleme kodunu veya EFI uygulamasını çalıştırır. |
| 2 | Önyükleyici | Başlatılacak işletim sistemi veya çekirdek sürümünü seçer; çekirdek imajını, varsa initramfs'i ve çekirdek parametrelerini belleğe yükleyip kontrolü çekirdeğe devreder. |
| 3 | Linux çekirdeği | Kendi başlangıç kodunu çalıştırır; işlemciyi, belleği, aygıtları ve süreç yönetimi gibi temel alt sistemleri hazırlar. Sonraki aşamayı başlatmak için ilk kullanıcı alanı programını çalıştırır. |
| 4 | Initramfs | Gerçek kök dosya sistemi hemen bağlanamıyorsa bellekte geçici bir kullanıcı alanı sağlar; sürücüleri ve depolama katmanlarını hazırlar, gerçek kök dosya sistemini bulup bağlar. |
| 5 | Gerçek sistemin init süreci (PID 1) | Gerçek kök dosya sisteminde çalışmaya devam eder; servisleri ve sistemin normal çalışma ortamını başlatır, süreçlerin yaşam döngüsünü yönetir. |
| 6 | Terminal ve kullanıcı shell'i | TTY ve getty gibi bileşenler üzerinden kullanıcı oturumunu hazırlar. Shell komutları yorumlar ve programların çalıştırılmasını sağlar. |

Bu aşamalar arasında kontrolün devredilmesi, önceki bileşenin bütün işi tamamladığı anlamına gelmez. Her bileşen kendi sorumluluğunu yerine getirip bir sonrakinin başlayabileceği koşulları hazırlar. Örneğin önyükleyici çekirdeği belleğe yükler ama çekirdeğin alt sistemlerini başlatmaz; initramfs de çoğunlukla sistemi son kullanıcı ortamına getirmek yerine gerçek kök dosya sistemine geçişi hazırlar.

```text
Güç düğmesi
    ↓
BIOS / UEFI
    ↓
Önyükleyici
    ↓
Linux çekirdeği
    ↓
Initramfs (kullanılıyorsa)
    ↓
Gerçek kök dosya sistemi ve PID 1
    ↓
TTY / getty / shell
    ↓
Kullanıcı oturumu
```

Şema genel akışı gösterir; her sistemde adımların ayrıntısı aynı değildir. BIOS ve UEFI önyükleyiciyi farklı yöntemlerle başlatır. Önyükleyici seçimi, çekirdek parametreleri ve donanım mimarisi de çekirdeğin izlediği yolu etkileyebilir. Initramfs kullanılan sistemlerde çekirdek önce bu imajdaki `/init` programını çalıştırır; bu program gerekli diskleri ve dosya sistemi katmanlarını hazırlayıp gerçek kök dosya sistemine geçer. Initramfs kullanılmadığında çekirdek, gerçek kök dosya sistemini doğrudan bağlayıp oradaki init programını başlatabilir.

Gerçek kök dosya sistemine geçildikten sonra PID 1 servisleri, aygıtları ve oturum açma altyapısını yönetir. Yapılandırmaya göre kullanıcı bir metin konsolunda TTY ve getty üzerinden shell'e ulaşabilir veya grafik oturumu başlatılabilir. Böylece önyükleme zincirinin sonunda kullanıcı, sistemde program çalıştırabileceği bir ortama kavuşur.

Devamındaki bölümler bu aşamaları sırayla ayrıntılandırır: önce BIOS ve UEFI'nin önyükleyiciyi nasıl bulduğunu, ardından önyükleyicinin çekirdeği nasıl yüklediğini; sonrasında da çekirdekten kullanıcı oturumuna uzanan süreci inceleyeceğiz.
