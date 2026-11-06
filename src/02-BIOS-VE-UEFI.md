# BIOS ve UEFI Nedir? (Önyükleme Öncesi Aşama)

Bilgisayarın güç düğmesine basılmasıyla başlayan ve işletim sisteminin kontrolü devralmasına kadar devam eden süreçte, donanımın hazırlanması ve işletim sisteminin başlatılmasını sağlayacak önyükleyicinin bulunması anakart üzerindeki firmware tarafından gerçekleştirilir.

Bu aşamada karşımıza çıkan iki temel teknoloji BIOS (Basic Input/Output System) ve UEFI (Unified Extensible Firmware Interface) olarak adlandırılır.

BIOS ve UEFI, bilgisayarın donanımını başlangıç için hazırlayan, önyükleme aygıtlarını belirleyen ve işletim sisteminin başlatılmasını sağlayan firmware teknolojileridir.

Bu teknolojilerin çalışma biçimleri farklı olsa da temel amaçları aynıdır: Bilgisayarın donanımını başlangıç için hazırlamak ve kontrolü işletim sisteminin önyükleyicisine devretmek.

## 1. BIOS (Basic Input/Output System) ve MBR

BIOS, kişisel bilgisayarlarda kullanılan geleneksel firmware teknolojisidir. IBM PC mimarisiyle 1981 yılında yaygınlaşan bu yaklaşım, bilgisayarın açılışında donanımın hazırlanması ve işletim sisteminin başlatılması için gerekli temel işlevleri sağlar.

BIOS, bilgisayar açıldığında işlemcinin başlangıç kodunu çalıştırmasıyla devreye girer. Donanımın başlangıç kontrollerini gerçekleştirir ve yapılandırılmış önyükleme sırasına göre işletim sisteminin bulunduğu aygıtı belirler.

### Çalışma Mantığı

BIOS tabanlı önyükleme süreci genel olarak aşağıdaki aşamalardan oluşur:

**1. POST (Power-On Self-Test):**

Bilgisayarın açılmasıyla birlikte işlemci, bellek ve temel donanım bileşenleri için başlangıç kontrolleri gerçekleştirilir.

Donanımın başlangıç için uygun olup olmadığı kontrol edilir. Bir hata tespit edilirse sistemin açılışı durdurulabilir veya hata mesajı gösterilebilir.

**2. Donanımın Hazırlanması:**

BIOS, önyükleme için gerekli donanım bileşenlerini hazırlar. Depolama aygıtları algılanır ve yapılandırılmış önyükleme sırası kontrol edilir.

Örneğin bilgisayarın ilk olarak SSD, ardından USB bellek üzerinden başlatılması tercih edilmiş olabilir.

**3. MBR (Master Boot Record):**

BIOS, seçilen önyükleme aygıtının ilk sektörünü okur. MBR bölümleme yapısı kullanılıyorsa bu sektör, geleneksel olarak 512 bayt büyüklüğündedir.

MBR içerisinde üç temel bileşen bulunur:

- **Boot Code (446 bayt):** Önyükleme işlemini başlatmak için kullanılan makine kodunu içerir.
- **Partition Table (64 bayt):** Disk üzerindeki bölümlerin başlangıç ve bitiş bilgilerini içeren bölüm tablosudur.
- **Boot Signature (2 bayt):** Sektörün önyüklenebilir olduğunu belirten imzadır. Değeri `0x55AA` şeklindedir.

MBR yapısının genel görünümü:

```text
MBR (512 Bayt)
┌──────────────────────────────┐
│ Boot Code                    │ 446 Bayt
├──────────────────────────────┤
│ Partition Entry 1            │ 16 Bayt
│ Partition Entry 2            │ 16 Bayt
│ Partition Entry 3            │ 16 Bayt
│ Partition Entry 4            │ 16 Bayt
├──────────────────────────────┤
│ Boot Signature (0x55AA)      │ 2 Bayt
└──────────────────────────────┘
```

**4. Bootloader'ın Başlatılması:**

BIOS, MBR içerisindeki önyükleme kodunu belleğe yükler ve işlemciye bu kodu çalıştırması için kontrolü devreder.

MBR içerisindeki kodun boyutu sınırlı olduğundan GRUB gibi gelişmiş önyükleyiciler genellikle ek önyükleme kodlarına ihtiyaç duyar.

Örneğin GRUB, geleneksel BIOS tabanlı sistemlerde ilk aşamadan sonra gerekli diğer bileşenleri yükleyerek Linux çekirdeğini başlatabilecek duruma gelir.

### MBR'nin Sınırlamaları

MBR bölümleme yapısının önemli sınırlamaları bulunmaktadır:

- **Disk kapasitesi:** Geleneksel 512 bayt sektörlü disklerde yaklaşık 2 TiB (2,2 TB) adresleme sınırı vardır. Bunun nedeni MBR'nin 32 bitlik sektör adreslemesi kullanmasıdır.
- **Bölüm sayısı:** Bir diskte en fazla dört birincil (Primary) bölüm tanımlanabilir.
- **Genişletilmiş bölüm:** Dört birincil bölüm sınırını aşmak için genişletilmiş (Extended) bölüm oluşturulabilir. Bu bölüm içerisinde mantıksal (Logical) bölümler tanımlanabilir.
- **Yedeklilik:** Bölüm tablosunun yedek bir kopyası bulunmaz. MBR'nin zarar görmesi bölüm bilgilerine ve önyükleme işlemlerine erişimi etkileyebilir.
- **Bütünlük kontrolü:** GPT'de bulunan CRC32 tabanlı bölüm tablosu doğrulama mekanizması MBR'de bulunmaz.

MBR'nin sınırlamaları nedeniyle daha büyük diskleri ve daha esnek bölümleme yapılarını destekleyen GPT geliştirilmiştir.

## 2. UEFI (Unified Extensible Firmware Interface) ve GPT

UEFI, modern bilgisayarlarda kullanılan ve geleneksel BIOS yaklaşımının yerini alan firmware arayüzü standardıdır.

UEFI, BIOS'a kıyasla daha gelişmiş önyükleme mekanizmaları, genişletilebilir sürücü desteği, güvenlik özellikleri ve işletim sisteminden bağımsız EFI uygulamalarının çalıştırılabilmesini sağlar.

UEFI'nin en önemli farklılıklarından biri, önyükleme işlemini yalnızca diskin ilk sektöründeki makine koduna bağlı olmadan gerçekleştirebilmesidir.

Firmware, desteklediği dosya sistemleri üzerinden EFI uygulamalarını bulabilir ve doğrudan çalıştırabilir.

### Çalışma Mantığı

UEFI tabanlı önyükleme süreci genel olarak aşağıdaki aşamalardan oluşur:

**1. POST (Power-On Self-Test):**

Bilgisayarın açılmasıyla birlikte işlemci, bellek ve diğer temel donanım bileşenleri kontrol edilir.

Bu aşamanın temel amacı BIOS ile aynıdır. Ancak POST işlemlerinin kapsamı ve uygulanma biçimi firmware üreticisine ve donanım platformuna göre değişebilir.

**2. Donanımın Hazırlanması:**

UEFI firmware'i, sistemin önyükleme yapabilmesi için gerekli donanım bileşenlerini hazırlar.

UEFI'nin önemli özelliklerinden biri, kendi içerisinde sürücü mimarisine sahip olmasıdır. Bu sayede depolama denetleyicileri ve bazı diğer donanım bileşenleri için gerekli sürücüler işletim sistemi başlamadan önce kullanılabilir.

**3. GPT (GUID Partition Table):**

UEFI sistemlerde yaygın olarak kullanılan disk bölümleme yapısı GPT'dir.

GPT, disk bölümlerini benzersiz GUID (Globally Unique Identifier) değerleriyle tanımlar.

MBR'den farklı olarak GPT, disk bölümleme bilgilerini daha esnek bir yapıda saklar.

GPT yapısının önemli özellikleri şunlardır:

- 64 bitlik mantıksal blok adreslemesi kullanır.
- Büyük kapasiteli diskleri destekler.
- Bölümlere benzersiz GUID değerleri atanır.
- Bölüm tablosunun yedek kopyası diskin sonunda tutulur.
- CRC32 ile bölüm tablosunun bütünlüğü kontrol edilebilir.
- Bölüm sayısı, GPT başlığındaki bölüm girdisi sayısına bağlıdır. Yaygın uygulamalarda 128 bölüm kullanılır.

**4. ESP (EFI System Partition):**

UEFI, önyükleyici dosyalarını bulmak için EFI System Partition (ESP) adı verilen özel bir disk bölümünü kullanır.

ESP genellikle FAT32 dosya sistemiyle biçimlendirilir ve içerisinde EFI uygulamaları bulunur.

Linux sistemlerde ESP içerisinde birden fazla önyükleyiciye ait dosyalar bulunabilir.

Örnek ESP dizin yapısı:

```text
/EFI
├── BOOT
│   └── BOOTX64.EFI
├── debian
│   └── grubx64.efi
├── arch
│   └── grubx64.efi
└── systemd
    └── systemd-bootx64.efi
```

Buradaki dosyalar örnek bir dizin yapısını göstermektedir. Gerçek dosya ve dizin adları dağıtıma, önyükleyiciye ve sistem yapılandırmasına göre değişebilir.

**5. NVRAM ve Boot Entries:**

UEFI sistemlerde önyükleme seçenekleri NVRAM üzerinde saklanan girdiler aracılığıyla yönetilebilir.

Bu girdiler Boot Entries olarak adlandırılır.

Her önyükleme girdisi, ilgili EFI uygulamasının bulunduğu disk ve dosya yoluna ilişkin bilgileri içerir.

Örneğin:

```text
Boot0001* debian
Boot0002* UEFI OS
Boot0003* Windows Boot Manager
```

Bu kayıtlar üzerinden firmware hangi EFI uygulamasının başlatılacağını belirleyebilir.

Linux sistemlerde bu girdileri görüntülemek için aşağıdaki komut kullanılabilir:

```bash
efibootmgr -v
```

**6. EFI Uygulamasının Başlatılması:**

UEFI firmware'i seçilen önyükleme girdisine ait EFI uygulamasını bulur ve çalıştırır.

Örneğin GRUB kullanılıyorsa `grubx64.efi` dosyası çalıştırılarak Linux çekirdeğinin yüklenmesi aşamasına geçilir.

UEFI sistemlerde çıkarılabilir medya ve standart önyükleme konumları için varsayılan EFI dosya yolları da tanımlanmıştır.

Örneğin x86-64 sistemlerde:

```text
/EFI/BOOT/BOOTX64.EFI
```

Bu dosya, uygun koşullarda standart geri dönüş (fallback) önyükleme yolu olarak kullanılabilir.

### UEFI'nin Avantajları

UEFI'nin geleneksel BIOS yaklaşımına göre önemli avantajları bulunmaktadır:

- **Büyük disk desteği:** GPT ile birlikte 2 TiB üzerindeki disklerin kullanılmasına olanak sağlar.
- **Esnek bölümleme:** MBR'nin dört birincil bölüm sınırını ortadan kaldırır.
- **Yedeklilik:** GPT bölüm tablosunun yedek kopyası sayesinde bölümleme bilgilerinin kurtarılmasını kolaylaştırır.
- **Güvenlik:** Secure Boot aracılığıyla önyükleme zincirindeki EFI uygulamalarının imzaları doğrulanabilir.
- **Genişletilebilirlik:** Firmware içerisinde farklı donanımlar ve dosya sistemleri için sürücüler bulunabilir.
- **EFI uygulamaları:** İşletim sistemi önyükleyicilerinin yanı sıra çeşitli bakım ve tanılama uygulamaları da çalıştırılabilir.
- **NVRAM desteği:** Önyükleme seçenekleri ve öncelikleri firmware belleğinde saklanabilir.

UEFI'nin grafik arayüz, fare desteği veya ağ üzerinden önyükleme gibi özellikleri bulunabilir. Ancak bunlar her UEFI uygulamasında bulunması zorunlu özellikler değildir.

## 3. Secure Boot (Güvenli Önyükleme)

UEFI ile birlikte sunulan önemli güvenlik özelliklerinden biri Secure Boot'tur.

Secure Boot, bilgisayarın açılış sürecinde çalıştırılacak EFI uygulamalarının güvenilir imzalara sahip olup olmadığını kontrol eder.

Bu mekanizma sayesinde yetkisiz veya güvenilmeyen önyükleme yazılımlarının çalıştırılması engellenebilir.

Secure Boot'un temel çalışma mantığı şöyledir:

1. UEFI firmware'i, güvenilir imza anahtarlarını ve sertifikalarını saklar.
2. Başlatılmak istenen EFI uygulamasının dijital imzası kontrol edilir.
3. Uygulamanın imzası güvenilir bulunursa çalıştırılmasına izin verilir.
4. İmza doğrulanamazsa firmware yapılandırmasına bağlı olarak uygulamanın çalıştırılması engellenir.

Secure Boot sürecinde kullanılan temel anahtar ve veritabanları şunlardır:

| Bileşen | Görevi |
|---|---|
| PK (Platform Key) | Platformun güvenlik sahipliğini belirler. |
| KEK (Key Exchange Key) | İmza veritabanlarının güncellenmesinde yetkilendirme sağlar. |
| db | Güvenilir imzaları ve sertifikaları içerir. |
| dbx | İptal edilmiş veya engellenmesi gereken imzaları içerir. |

Linux sistemlerde Secure Boot desteği, dağıtımın ve kullanılan önyükleyicinin imzalama yöntemine bağlıdır.

Örneğin bazı dağıtımlar Microsoft tarafından imzalanmış bir shim uygulaması kullanabilir. Shim, GRUB gibi sonraki aşama önyükleme bileşenlerinin güvenilirliğini doğrulamaya yardımcı olur.

Secure Boot yalnızca UEFI ile kullanılan bir güvenlik mekanizmasıdır. Her UEFI sistemde etkin olmak zorunda değildir.

## 4. BIOS ve UEFI Karşılaştırma Tablosu

| Özellik | Geleneksel BIOS | Modern UEFI |
|---|---|---|
| Firmware mimarisi | Geleneksel BIOS | UEFI standardı |
| Önyükleme yöntemi | Diskin önyükleme kodunu çalıştırma | EFI uygulamalarını çalıştırma |
| Yaygın bölümleme yapısı | MBR | GPT |
| MBR disk kapasitesi | 512 bayt sektörlerde yaklaşık 2 TiB | GPT ile çok daha büyük diskler |
| Bölüm sayısı | 4 birincil veya genişletilmiş yapı | Yaygın olarak 128 GPT bölümü |
| Önyükleyici konumu | MBR ve devamındaki disk alanları | EFI System Partition |
| Önyükleyici biçimi | Makine kodu | EFI uygulaması (.efi) |
| Önyükleme kayıtları | Firmware ayarları | NVRAM Boot Entries |
| Secure Boot | Standart bir özelliği değildir | Desteklenir |
| Genişletilebilir sürücü mimarisi | Sınırlı geleneksel firmware hizmetleri | UEFI sürücü mimarisi |
| Grafik arayüz | Üreticiye bağlı, genellikle sınırlı | Üreticiye bağlı |
| GPT desteği | Doğrudan geleneksel BIOS önyüklemesinde zorunlu değildir | Yaygın olarak kullanılır |

**Önemli:** BIOS ve MBR ile UEFI ve GPT sık kullanılan eşleşmelerdir ancak birbirlerine zorunlu olarak bağlı değildir. Örneğin GRUB, BIOS modunda GPT bölümleme tablosuna sahip bir diskten de başlatılabilir. Bunun için genellikle BIOS Boot Partition kullanılır. Benzer şekilde bazı UEFI uygulamaları MBR bölümleme yapısına sahip disklerden de önyükleme yapabilir.

## 5. Linux Üzerinde Sistem Türünü Kontrol Etme

Çalışan Linux sisteminin BIOS (Legacy) veya UEFI modunda başlatıldığını anlamak için aşağıdaki komut kullanılabilir:

```bash
[ -d /sys/firmware/efi ] && echo "Sistem: UEFI" || echo "Sistem: BIOS / Legacy"
```

Bu komut, Linux çekirdeğinin oluşturduğu `/sys/firmware/efi` dizininin mevcut olup olmadığını kontrol eder.

- Dizin mevcutsa sistem UEFI modunda başlatılmıştır.
- Dizin mevcut değilse sistem büyük olasılıkla Legacy BIOS modunda başlatılmıştır.

Burada dikkat edilmesi gereken nokta, bu kontrolün bilgisayarın hangi firmware teknolojisine sahip olduğunu değil, mevcut Linux oturumunun hangi önyükleme modunda başlatıldığını göstermesidir.

### UEFI Bilgilerini Görüntüleme

UEFI modunda başlatılmış bir Linux sistemde firmware değişkenleri şu dizinde bulunabilir:

```bash
ls /sys/firmware/efi/
```

Önyükleme girdilerini görüntülemek için:

```bash
sudo efibootmgr -v
```

Bu komut, firmware üzerinde kayıtlı önyükleme seçeneklerini ve EFI uygulamalarının dosya yollarını gösterir.

### Disk Bölümleme Yapısını Kontrol Etme

Diskin MBR veya GPT kullanıp kullanmadığını öğrenmek için:

```bash
sudo fdisk -l
```

Alternatif olarak:

```bash
sudo parted -l
```

`fdisk` çıktısında aşağıdaki ifade görülüyorsa disk GPT bölümleme yapısını kullanmaktadır:

```text
Disklabel type: gpt
```

MBR bölümleme yapısında ise:

```text
Disklabel type: dos
```

ifadesi görülebilir.

## 6. BIOS ve UEFI Önyükleme Sürecinin Genel Akışı

### BIOS Tabanlı Önyükleme

```text
Bilgisayarın Açılması
        |
        v
POST ve Donanım Kontrolü
        |
        v
BIOS Firmware
        |
        v
Önyükleme Aygıtının Seçilmesi
        |
        v
MBR (İlk Disk Sektörü)
        |
        v
İlk Önyükleme Kodu
        |
        v
GRUB ve Diğer Önyükleyici Bileşenleri
        |
        v
Linux Kernel
```

### UEFI Tabanlı Önyükleme

```text
Bilgisayarın Açılması
        |
        v
POST ve Donanım Kontrolü
        |
        v
UEFI Firmware
        |
        v
NVRAM Boot Entries
        |
        v
EFI System Partition (ESP)
        |
        v
EFI Önyükleyici Dosyası (.efi)
        |
        v
Linux Kernel
```

Her iki yapıda da önyükleyicinin Linux çekirdeğini başlatmasıyla birlikte işletim sisteminin diğer açılış aşamaları devreye girer.

## Kaynakça ve İleri Okuma

1. [UEFI Forum – UEFI Specifications](https://uefi.org/specifications)
2. [ArchWiki – GRUB](https://wiki.archlinux.org/title/GRUB)
3. [ArchWiki – EFI System Partition](https://wiki.archlinux.org/title/EFI_system_partition)
4. [ArchWiki – GUID Partition Table](https://wiki.archlinux.org/title/GUID_Partition_Table)
5. [Gentoo Wiki – GRUB](https://wiki.gentoo.org/wiki/GRUB)
6. [GNU GRUB Manual](https://www.gnu.org/software/grub/manual/grub/grub.html)
7. [Linux man-pages – efibootmgr](https://man.archlinux.org/man/efibootmgr.8.en)

---

*Not: BIOS ve UEFI arasındaki farklılıklar yalnızca önyükleme hızından ibaret değildir. Temel farklılık, firmware'in önyükleme uygulamalarını nasıl bulduğu, yüklediği ve çalıştırdığıdır. Disk bölümleme yapısı ve güvenlik mekanizmaları da bu mimarinin önemli parçalarıdır.*