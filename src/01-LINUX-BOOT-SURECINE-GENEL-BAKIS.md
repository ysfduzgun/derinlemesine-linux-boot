# Linux Çekirdeği (Kernel)

Önyükleyici (Bootloader), çekirdek imajını (`vmlinuz`) ve varsa başlangıç dosya sistemini (`initramfs`) belleğe yükleyerek kontrolü Linux çekirdeğine devreder.

Bu noktadan itibaren işletim sisteminin en temel bileşeni olan Linux Kernel (Çekirdek) çalışmaya başlar.

Kernel, donanım ile yazılım arasındaki iletişimi sağlayan ve sistem kaynaklarını yöneten ana bileşendir. İşlemci, bellek, depolama aygıtları, ağ kartları ve diğer donanımların yönetiminden sorumludur.

Linux çekirdeğinin temel görevleri şunlardır:

- **İşlem yönetimi:** Çalışan programların süreçlerini oluşturur, sonlandırır ve işlemci zamanını yönetir.
- **Bellek yönetimi:** Fiziksel ve sanal belleğin kullanımını düzenler.
- **Donanım yönetimi:** Donanım bileşenleriyle sürücüler aracılığıyla iletişim kurar.
- **Dosya sistemi yönetimi:** Dosya sistemlerine erişimi ve VFS altyapısını yönetir.
- **Ağ yönetimi:** Ağ protokollerini ve ağ aygıtlarının çalışma mekanizmalarını yönetir.
- **Güvenlik ve erişim denetimi:** Süreçlerin ve kullanıcıların sistem kaynaklarına erişimini kontrol eder.

Bu bölümde, çekirdek imajının belleğe nasıl yüklendiğini, işlemcinin çalışma modlarının nasıl hazırlandığını, çekirdek alt sistemlerinin nasıl ilklendirildiğini ve kullanıcı alanının nasıl başlatıldığını inceleyeceğiz.

## 1. Vmlinuz Anatomisi

Modern Linux dağıtımlarında çekirdek imajı genellikle aşağıdaki dizinde bulunur:

```text
/boot/vmlinuz-<kernel-version>
```

Örneğin:

```text
/boot/vmlinuz-6.12.113+deb13-amd64
```

Buradaki dosya adı geleneksel bir adlandırma biçimidir. `vmlinuz` isminin açılımı konusunda yaygın açıklamalar bulunsa da dosya adındaki harfler, modern çekirdek imajının iç yapısını kesin olarak tanımlamaz.

Linux çekirdeğinin çalıştırılabilir dosyası olan `vmlinux`, genellikle sıkıştırılmamış ELF biçimindeki çekirdek imajını ifade eder. `vmlinuz` ise önyükleme için hazırlanmış, genellikle sıkıştırılmış çekirdek imajıdır.

### bzImage Nedir?

x86 ve x86-64 sistemlerde yaygın olarak kullanılan çekirdek imajı biçimi `bzImage` olarak adlandırılır.

Buradaki `bz` ifadesi, imajın mutlaka bzip2 algoritmasıyla sıkıştırıldığı anlamına gelmez. Tarihsel olarak büyük çekirdek imajlarını düşük bellek alanından bağımsız biçimde yükleyebilmek amacıyla geliştirilen bir biçimdir.

bzImage, çekirdeğin önyükleme sırasında ihtiyaç duyduğu hazırlık kodlarını ve sıkıştırılmış çekirdek gövdesini bir arada barındırır.

Genel yapısı şu bileşenlerden oluşur:

| Bileşen | Görevi |
|---|---|
| Boot Sector | Önyükleyiciyle iletişim ve başlangıç bilgilerini içerir. |
| Setup Code | Önyükleme parametrelerini işler ve mimariye özgü başlangıç hazırlıklarını gerçekleştirir. |
| Decompressor | Sıkıştırılmış çekirdek gövdesini açar. |
| Compressed Kernel | İşletim sisteminin ana çekirdek kodunu içerir. |
| Boot Header | Önyükleyiciye gerekli çekirdek bilgilerini ve desteklenen özellikleri bildirir. |

Genel görünüm:

```text
vmlinuz (bzImage)
│
├── Boot Header
│   └── Önyükleme bilgileri
│
├── Setup Code
│   └── Başlangıç hazırlıkları
│
├── Decompressor
│   └── Sıkıştırılmış imajı açar
│
└── Compressed Kernel
    └── Linux çekirdeğinin ana kodu
```

### Çekirdek Sıkıştırma Algoritmaları

Linux çekirdeği farklı sıkıştırma algoritmaları kullanılarak derlenebilir.

Yaygın algoritmalar:

| Algoritma | Özellik |
|---|---|
| Gzip | Yaygın ve geniş uyumluluğa sahip sıkıştırma algoritması. |
| XZ | Yüksek sıkıştırma oranı sunar. |
| LZ4 | Hızlı sıkıştırma ve açma performansıyla bilinir. |
| Zstandard (Zstd) | Sıkıştırma oranı ve performans arasında denge sunar. |
| LZO | Hızlı açma performansı sunan algoritmalardan biridir. |

Kullanılabilecek algoritmalar, çekirdeğin derleme sırasında etkinleştirilen yapılandırma seçeneklerine bağlıdır.

**Önemli:** Çekirdek imajının açılması ile initramfs imajının açılması iki farklı işlemdir. Çekirdek imajını kendi decompressor kodu açarken initramfs, çekirdek tarafından ayrıca açılarak başlangıç dosya sistemi hâline getirilir.

### vmlinux ve vmlinuz Arasındaki Fark

| Özellik | vmlinux | vmlinuz |
|---|---|---|
| Yapı | Genellikle ELF biçiminde | Önyükleme imajı |
| Sıkıştırma | Genellikle sıkıştırılmamış | Genellikle sıkıştırılmış |
| Kullanım | Geliştirme, hata ayıklama ve analiz | Sistem önyüklemesi |
| Decompressor | Genellikle bulunmaz | Kendi açılış mekanizmasını içerir |
| Dağıtımlardaki konum | Derleme kaynaklarında veya debug paketlerinde | Genellikle /boot altında |

vmlinux ve vmlinuz birbirleriyle ilişkili olsa da doğrudan aynı dosyanın farklı isimleri olarak değerlendirilmemelidir. Önyükleme imajı oluşturulurken mimariye özgü ek kodlar ve yapılandırmalar da kullanılır.

## 2. İşlemci Modları ve Kernel Başlangıcı

Linux çekirdeğinin başlangıç sürecini anlayabilmek için işlemcinin çalışma modlarını bilmek gerekir.

x86 mimarisinde işlemci, farklı bellek erişim ve çalışma yetenekleri sunan çeşitli modlarda çalışabilir.

Bu modların en önemlileri şunlardır:

- Real Mode (Gerçek Mod)
- Protected Mode (Korumalı Mod)
- Long Mode (64-bit Mod)

### 2.1. Real Mode (Gerçek Mod)

Real Mode, x86 işlemcilerin geleneksel başlangıç çalışma modudur.

İşlemcinin sıfırlanmasının ardından x86 mimarisinde başlangıç durumu bu mod üzerinden tanımlanır.

Temel özellikleri:

- 16-bit çalışma ortamı sunar.
- Geleneksel adresleme yapısında 1 MB bellek alanına erişebilir.
- Bellek koruması ve modern sanal bellek mekanizmaları bulunmaz.
- Eski BIOS yazılımlarıyla uyumluluk sağlar.

BIOS üzerinden başlatılan geleneksel x86 önyükleme sürecinde çekirdeğin başlangıç kodu Real Mode ortamında çalıştırılır.

Bu aşamada önyükleyiciden gelen başlangıç parametreleri ve sistem bilgileri işlenir.

### 2.2. Protected Mode (Korumalı Mod)

Protected Mode, x86 işlemcilerin daha gelişmiş bellek yönetimi ve koruma mekanizmalarını kullanmasını sağlar.

Temel özellikleri:

- 32-bit adresleme ve işlem yetenekleri sunar.
- Bellek segmentasyonu ve koruma mekanizmaları sağlar.
- GDT (Global Descriptor Table) kullanır.
- İşlemci istisnaları ve kesmeler için gerekli altyapıyı destekler.
- Sanal bellek yönetimi için gerekli mekanizmaların kullanılmasına imkân tanır.

Bu modda işlemci, sistem belleğini daha kontrollü bir şekilde yönetebilir.

### 2.3. Long Mode (64-bit Mod)

Long Mode, x86-64 mimarisinde kullanılan 64-bit çalışma ortamıdır.

Modern 64-bit Linux çekirdeklerinin çalışabilmesi için işlemcinin bu moda geçmesi gerekir.

Temel özellikleri:

- 64-bit işlem ve adresleme desteği sağlar.
- Genişletilmiş işlemci yazmaçlarını kullanır.
- 64-bit sanal adresleme mekanizmalarını destekler.
- Modern bellek yönetimi ve sayfalama mekanizmalarını kullanır.

Long Mode'a geçiş sırasında işlemcinin gerekli özellikleri desteklemesi, sayfalama mekanizmalarının hazırlanması ve ilgili kontrol yazmaçlarının yapılandırılması gerekir.

### İşlemci Modlarının Genel Akışı

Geleneksel BIOS tabanlı x86-64 önyüklemesinde genel olarak aşağıdaki geçişler gerçekleşebilir:

```text
       BIOS / Bootloader
              |
              v
        REAL MODE
           16-bit
              |
              v
      PROTECTED MODE
           32-bit
              |
              v
        LONG MODE
           64-bit
              |
              v
       Kernel Başlangıcı
```

**Önemli:** Bu şema geleneksel x86 BIOS başlangıç yolunu basitleştirerek gösterir. UEFI üzerinden başlatılan x86-64 sistemlerde firmware, EFI uygulamalarını zaten 64-bit Long Mode ortamında çalıştırabilir. Dolayısıyla her Linux önyüklemesinde işlemcinin mutlaka 16-bit Real Mode'dan başlayıp 32-bit Protected Mode üzerinden 64-bit Long Mode'a geçtiğini söylemek doğru değildir.

UEFI ve BIOS başlangıç yolları, Linux çekirdeğinin mimariye özgü başlangıç kodlarında farklılık gösterir.

## 3. Çekirdeğin Sıkıştırmasının Açılması (Decompression)

Önyükleyici tarafından belleğe yüklenen çekirdek imajı, doğrudan normal çekirdek çalışma ortamına geçmeden önce kendi başlangıç kodlarını çalıştırır.

Bu başlangıç kodları, mimariye ve önyükleme yöntemine bağlı olarak gerekli hazırlıkları gerçekleştirir.

Özellikle x86-64 sistemlerde decompressor kodunun görevleri şunlardır:

1. Önyükleyiciden gelen başlangıç bilgilerini değerlendirmek.
2. Gerekli işlemci özelliklerini kontrol etmek.
3. Bellek alanlarını ve çekirdeğin yerleşimini hazırlamak.
4. Sıkıştırılmış çekirdek gövdesini açmak.
5. Açılan çekirdeği uygun bellek alanına yerleştirmek.
6. Kontrolü çekirdeğin mimariye özgü başlangıç koduna devretmek.

Sıkıştırılmış çekirdeğin açılması sırasında mevcut bellek haritasının dikkate alınması gerekir. Çekirdek imajının kendi üzerine yazılmasını veya BIOS, firmware ve diğer sistem bileşenleri için ayrılmış bellek alanlarının bozulmasını önlemek önemlidir.

Bu nedenle çekirdek, kendisini bellekte uygun bir konuma yerleştirmek için gerekli düzenlemeleri gerçekleştirir.

### Decompression Sonrası Başlangıç

Çekirdek gövdesi açıldıktan sonra mimariye özgü başlangıç kodları çalıştırılır.

x86-64 mimarisinde bu aşamada aşağıdaki dosya ve bileşenler önemlidir:

| Dosya / Bileşen | Görevi |
|---|---|
| arch/x86/boot/ | x86 önyükleme hazırlık kodları |
| arch/x86/boot/compressed/ | Çekirdek açma ve yerleştirme kodları |
| arch/x86/kernel/head_64.S | 64-bit mimariye özgü erken başlangıç kodu |
| init/main.c | Mimari bağımsız çekirdek başlangıç fonksiyonları |

Bu aşamaların ardından çekirdek, mimariye özgü başlangıç işlemlerini tamamlayarak C dilinde yazılmış ana başlangıç fonksiyonuna ulaşır.

Bu fonksiyon:

```c
start_kernel()
```

olarak adlandırılır.

## 4. start_kernel() ve Çekirdek Alt Sistemlerinin İlklendirilmesi

Linux çekirdeğinin ana başlangıç fonksiyonu olan `start_kernel()`, çekirdeğin temel çalışma altyapısının hazırlanmasından sorumludur.

Kaynak kod içerisinde:

```text
init/main.c
```

dosyasında bulunur.

Bu fonksiyon çalıştığında henüz normal kullanıcı uygulamaları veya grafiksel masaüstü ortamı başlatılmamıştır.

Çekirdek, kendi temel altyapısını hazırlayarak sistemin süreçleri ve donanımı yönetebileceği duruma gelmesini sağlar.

Bu aşamada gerçekleştirilen önemli işlemler şunlardır:

### 4.1. Mimariye Özgü Hazırlıklar

Çekirdek ilk olarak işlemci mimarisine özgü başlangıç işlemlerini gerçekleştirir.

Bu görevlerde `setup_arch()` fonksiyonu önemli rol oynar.

Örneğin:

- Fiziksel bellek haritasının değerlendirilmesi.
- İşlemci ve platform bilgilerinin hazırlanması.
- Firmware tarafından sağlanan bilgilerin işlenmesi.
- Mimariye özgü başlangıç parametrelerinin değerlendirilmesi.
- Kullanılabilir ve ayrılmış bellek alanlarının belirlenmesi.

### 4.2. Bellek Yönetiminin Başlatılması

Çekirdek, fiziksel ve sanal belleği yönetebilmek için gerekli altyapıyı oluşturur.

Bu kapsamda:

- Fiziksel bellek sayfaları yönetilebilir hâle getirilir.
- Bellek ayırma mekanizmaları hazırlanır.
- Sanal bellek yönetimi için gerekli yapılar oluşturulur.
- Bellek bölgeleri ve NUMA gibi platform özellikleri değerlendirilir.
- Kernel alanı ve kullanıcı alanı arasındaki bellek koruması hazırlanır.

Linux çekirdeğinin bellek yönetimi altyapısı, sistemdeki süreçlerin birbirlerinin bellek alanlarına kontrolsüz şekilde erişmesini engelleyen önemli mekanizmalar içerir.

### 4.3. Süreç Zamanlayıcısının Başlatılması

Linux, aynı anda birçok programın çalışmasını sağlayabilmek için işlemci zamanını süreçler arasında paylaştırır.

Bu işlemi Scheduler (Zamanlayıcı) gerçekleştirir.

Çekirdeğin başlangıç aşamasında:

```c
sched_init()
```

fonksiyonu aracılığıyla zamanlayıcı altyapısının gerekli başlangıç yapıları hazırlanır.

Zamanlayıcının temel görevleri:

- Çalıştırılmaya hazır süreçleri yönetmek.
- İşlemci zamanını süreçler arasında paylaştırmak.
- Öncelik ve zamanlama politikalarını uygulamak.
- Çok çekirdekli işlemcilerde süreçleri uygun işlemcilere dağıtmak.

### 4.4. Kesme ve İstisna Yönetimi

İşlemci, normal komut yürütme akışının dışında bazı olaylara tepki vermek zorundadır.

Örneğin:

- Klavyeden bir tuşa basılması.
- Ağ kartına yeni bir veri paketinin ulaşması.
- Disk okuma işleminin tamamlanması.
- İşlemci üzerinde bir hata oluşması.

Bu olayların yönetilmesinde Interrupt (Kesme) ve Exception (İstisna) mekanizmaları kullanılır.

Çekirdek başlangıcında GDT, IDT ve kesme altyapısı gibi yapılar hazırlanır.

Önemli bileşenler:

- **GDT (Global Descriptor Table):** x86 mimarisinde segment tanımlamalarını ve işlemci çalışma ortamına ilişkin bilgileri tutar.
- **IDT (Interrupt Descriptor Table):** İşlemci kesmelerinin ve istisnalarının hangi işleyiciler tarafından karşılanacağını belirler.
- **IRQ (Interrupt Request):** Donanım aygıtlarından gelen kesme isteklerini ifade eder.

### 4.5. Sanal Dosya Sistemi (VFS)

Linux, farklı dosya sistemlerine ortak bir arayüz üzerinden erişebilmek için VFS (Virtual File System) kullanır.

Örneğin sistemde:

- ext4
- XFS
- Btrfs
- FAT32
- NTFS

gibi farklı dosya sistemleri bulunabilir.

VFS, uygulamaların ve çekirdeğin bu dosya sistemlerine ortak bir arayüz üzerinden erişmesini sağlar.

Çekirdek başlangıcında VFS altyapısının gerekli veri yapıları ve önbellekleri hazırlanır.

### Önemli Başlangıç Fonksiyonları

Aşağıdaki tabloda çekirdek başlangıcında karşılaşılan bazı önemli fonksiyon ve bileşenler özetlenmiştir.

| Fonksiyon / Bileşen | Görevi |
|---|---|
| setup_arch() | Mimariye özgü donanım ve bellek hazırlıklarını gerçekleştirir. |
| mm_core_init() | Bellek yönetiminin temel altyapısını başlatır. |
| sched_init() | Süreç zamanlayıcı altyapısını hazırlar. |
| trap_init() | İşlemci istisna ve trap mekanizmalarını hazırlar. |
| init_IRQ() | Donanım kesme altyapısının başlatılmasında görev alır. |
| vfs_caches_init() | VFS önbelleklerini ve gerekli veri yapılarını oluşturur. |
| rest_init() | İlk kernel thread'lerinin oluşturulmasını ve başlangıç sürecinin devamını sağlar. |

**Not:** Bu tablo başlangıç sürecindeki önemli bileşenleri temsil eder. Gerçek çağrı sırası ve fonksiyonların görev dağılımı çekirdek sürümüne ve işlemci mimarisine göre değişebilir. Bazı hazırlıklar doğrudan bu fonksiyonların içinde, bazıları ise mimariye özgü kodlarda gerçekleştirilir.

## 5. Çekirdek Parametreleri (Kernel Command Line)

Önyükleyici, Linux çekirdeğine başlangıç sırasında kullanacağı parametreleri iletir.

Bu parametreler Kernel Command Line olarak adlandırılır.

Çekirdek parametreleri, sistemin hangi diskten başlatılacağını, hangi sürücülerin kullanılacağını, hata ayıklama seviyesini ve çeşitli donanım özelliklerinin nasıl çalışacağını belirleyebilir.

Örneğin GRUB yapılandırmasında:

```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
```

şeklinde tanımlanan parametreler çekirdeğe iletilebilir.

Çalışan Linux sistemde kullanılan parametreleri görmek için:

```bash
cat /proc/cmdline
```

komutu kullanılabilir.

### Yaygın Kernel Parametreleri

| Parametre | Açıklama |
|---|---|
| root=UUID=... | Gerçek kök dosya sisteminin konumunu belirtir. |
| ro | Kök dosya sisteminin başlangıçta salt okunur bağlanmasını ister. |
| rw | Kök dosya sisteminin okunabilir ve yazılabilir bağlanmasını ister. |
| quiet | Çekirdeğin konsola yazdırdığı mesajları azaltır. |
| loglevel=3 | Konsola yazdırılan çekirdek mesajlarının seviyesini sınırlar. |
| init=/path | Varsayılan init programının yerine belirtilen programı başlatır. |
| systemd.unit=... | systemd'nin başlatacağı hedefi veya birimi belirler. |
| nomodeset | Çekirdeğin başlangıçta grafik mod ayarlaması yapmasını sınırlar. |
| panic=10 | Kernel panic durumunda belirtilen süre sonunda yeniden başlatmayı sağlar. |

**Önemli:** Bütün parametreler doğrudan Linux çekirdeği tarafından işlenmez. Bazıları initramfs içerisindeki araçlar veya sonrasında başlatılan init sistemi tarafından değerlendirilir.

Örneğin `splash` parametresi, genellikle Plymouth gibi grafiksel açılış ekranı bileşenleri tarafından değerlendirilir. Genel amaçlı bir Linux çekirdek parametresi değildir.

Benzer şekilde `systemd.unit=` parametresi systemd tarafından işlenir.

### init= Parametresi

`init=` parametresi, çekirdeğin başlatacağı ilk kullanıcı alanı programını belirlemek için kullanılır.

Örneğin:

```text
init=/bin/bash
```

Bu parametreyle sistemin normal init programı yerine Bash başlatılabilir.

Bu yöntem bazı kurtarma ve hata ayıklama senaryolarında kullanılabilir. Ancak gerçek kök dosya sisteminin erişilebilir olması ve gerekli dosyaların bulunması gerekir.

Bu işlem, normal bir kullanıcı oturumu başlatmaz ve sistem servislerini otomatik olarak çalıştırmaz.

## 6. PID 0 ve PID 1

Linux süreç yönetimini anlayabilmek için PID kavramını bilmek gerekir.

PID (Process ID), sistemde çalışan her sürece verilen benzersiz işlem numarasıdır.

Linux sistemlerde süreçlerin oluşturulması ve yönetilmesi çekirdeğin görevlerinden biridir.

Önyükleme sırasında özel öneme sahip iki süreç bulunur:

- PID 0: Idle Task (Boşta Bekleme Süreci).
- PID 1: İlk kullanıcı alanı süreci (Init).

### 6.1. PID 0 (Idle Process)

Linux çekirdeğinin başlangıç görev yapısı PID 0 olarak bilinir.

Bu görev geleneksel olarak swapper veya idle task olarak adlandırılır.

PID 0'ın temel görevi, işlemcinin çalıştırılacak başka bir görevi bulunmadığında boşta kalma işlemlerini yürütmektir.

Modern sistemlerde işlemcinin boşta kaldığı durumlarda uygun güç tasarrufu mekanizmaları kullanılabilir.

Örneğin işlemci, ACPI ve işlemci mimarisinin sunduğu mekanizmalar aracılığıyla düşük güç tüketimli bekleme durumlarına geçebilir.

Önemli bir ayrıntı: PID 0, normal kullanıcı süreçleri gibi oluşturulan standart bir süreç değildir. Çekirdeğin başlangıçtan itibaren yönettiği özel bir görev yapısıdır.

### 6.2. PID 1 (İlk Kullanıcı Alanı Süreci)

Çekirdeğin başlangıç işlemleri tamamlandığında kullanıcı alanının başlatılması gerekir.

Bu aşamada `rest_init()` fonksiyonu devreye girer.

Bu fonksiyon, çekirdek başlangıcında iki önemli kernel thread oluşturur:

- `kernel_init`
- `kthreadd`

Başlangıçta oluşturulan `kernel_init` görevi PID 1 numarasını alır.

Daha sonra çekirdek başlangıç işlemlerini tamamlayarak ilk kullanıcı alanı programını çalıştırmaya hazırlanır.

Bu noktada initramfs kullanılıyorsa ilk çalıştırılan program genellikle initramfs içerisindeki:

```text
/init
```

programıdır.

Initramfs kullanılmayan veya farklı başlangıç yapılandırmalarında çekirdek doğrudan gerçek kök dosya sistemindeki init programını başlatabilir.

Başlatılacak init programı için yaygın konumlar şunlardır:

```text
/sbin/init
/usr/lib/systemd/systemd
/bin/init
```

Bu dosyalar kullanılan dağıtıma ve init sistemine göre değişir.

Örneğin systemd kullanılan bir dağıtımda PID 1 görevi systemd tarafından üstlenilir.

Bunu çalışan sistemde kontrol etmek için:

```bash
ps -p 1 -o pid,ppid,comm,args
```

komutu kullanılabilir.

Örnek çıktı:

```text
PID  PPID  COMMAND  COMMAND
1    0     systemd  /sbin/init
```

### PID 0 ve PID 1 Arasındaki Fark

| Özellik | PID 0 | PID 1 |
|---|---|---|
| Adı | Idle / Swapper | Init |
| Görevi | İşlemci boşta kaldığında bekleme işlemlerini yürütmek | Kullanıcı alanını başlatmak ve sistemin süreçlerini yönetmek |
| Türü | Özel çekirdek görevi | İlk kullanıcı alanı süreci |
| Kullanıcı alanında mı? | Hayır | Evet |
| Örnek | Idle Task | systemd, OpenRC veya SysVinit |

### PID 1 ve Kthreadd İlişkisi

Linux çekirdeği, donanım ve sistem işlemlerini gerçekleştirmek için bazı özel kernel thread'ler oluşturur.

Bu thread'ler kullanıcı alanında çalışan normal programlardan farklıdır.

Örneğin:

- `kthreadd`: Çekirdek thread'lerinin oluşturulmasını yönetir.
- `kworker`: Çekirdeğin workqueue altyapısında arka plan görevlerini yürütür.
- `kswapd`: Bellek yönetiminde sayfa geri kazanımı işlemlerine yardımcı olur.

Bu süreçlerin çoğu kullanıcı alanından bağımsız olarak çekirdek içerisinde çalışır.

## 7. Kernel ve User Space (Kullanıcı Alanı)

Linux işletim sisteminde bellek ve işlemci yetkileri açısından iki temel çalışma alanı bulunur:

- Kernel Space (Çekirdek Alanı)
- User Space (Kullanıcı Alanı)

Bu ayrım, sistemin güvenli ve kararlı çalışabilmesi için önemlidir.

### Kernel Space

Kernel Space, Linux çekirdeğinin ve çekirdek modüllerinin çalıştığı ayrıcalıklı çalışma alanıdır.

Bu alanda çalışan kodlar donanım ve sistem kaynaklarına doğrudan erişebilecek yetkilere sahiptir.

Örneğin:

- Bellek yönetimi.
- İşlemci zamanlayıcısı.
- Dosya sistemi sürücüleri.
- Ağ altyapısı.
- Donanım sürücüleri.

### User Space

User Space, kullanıcı uygulamalarının ve sistem servislerinin çalıştığı alandır.

Bu alandaki programlar donanım kaynaklarına doğrudan erişmek yerine çekirdeğin sunduğu sistem çağrıları (System Calls) üzerinden işlem gerçekleştirir.

Örneğin:

- Bash
- systemd
- SSH
- Web sunucuları
- Masaüstü uygulamaları
- Kullanıcı programları

### Kernel Space ve User Space Karşılaştırması

| Özellik | Kernel Space | User Space |
|---|---|---|
| Çalışma yetkisi | Ayrıcalıklı | Sınırlı |
| Donanıma erişim | Çekirdek mekanizmaları üzerinden doğrudan yönetim | Sistem çağrıları üzerinden |
| Bellek alanı | Çekirdek belleği | Süreçlere ait kullanıcı belleği |
| Çalışan bileşenler | Kernel, kernel modülleri | Uygulamalar ve servisler |
| Hata etkisi | Sistem kararlılığını ciddi şekilde etkileyebilir | Genellikle ilgili süreçle sınırlıdır |

İki alan arasındaki iletişim System Call (Sistem Çağrısı) mekanizmasıyla sağlanır.

Örneğin bir uygulama dosya okumak istediğinde:

1. Uygulama `read()` sistem çağrısını gerçekleştirir.
2. İşlemci gerekli geçişi yaparak çekirdek alanına geçer.
3. Kernel, ilgili dosya tanımlayıcısını ve erişim izinlerini kontrol eder.
4. Dosya sisteminden gerekli veriler alınır.
5. Sonuç kullanıcı alanındaki uygulamaya döndürülür.

Bu mekanizma sayesinde kullanıcı uygulamaları donanımın yönetim ayrıntılarını bilmek zorunda kalmadan sistem kaynaklarını kullanabilir.

## 8. Kernel Hata Ayıklama ve Sistem İnceleme

Linux çekirdeği, başlangıç sırasında gerçekleştirdiği işlemlere ilişkin çeşitli mesajlar üretir.

Bu mesajlar, donanımın algılanması, sürücülerin yüklenmesi, bellek yönetimi ve diğer çekirdek işlemlerinin incelenmesi için kullanılabilir.

### 8.1. dmesg

`dmesg`, çekirdek tarafından üretilen mesajların halka arabelleğinden (ring buffer) okunmasını sağlar.

Temel kullanım:

```bash
dmesg
```

Çıktıyı sayfalı görüntülemek için:

```bash
dmesg | less
```

Donanım ve bellek mesajlarını filtrelemek için:

```bash
dmesg | grep -i -E 'memory|cpu|acpi'
```

Hata mesajlarını görüntülemek için:

```bash
dmesg --level=err,warn
```

Çekirdek mesajlarının zaman bilgileriyle görüntülenmesi için:

```bash
dmesg -T
```

Not: `dmesg -T` tarafından gösterilen zamanlar yaklaşık takvim zamanlarıdır. Özellikle sistemin çok erken açılış aşamalarında zaman eşitlemesi henüz gerçekleşmemiş olabilir.

### 8.2. /proc/cpuinfo

Çekirdeğin işlemci hakkında topladığı bilgileri görüntüler.

```bash
cat /proc/cpuinfo
```

Bu dosyada:

- İşlemci modeli.
- İşlemci ailesi.
- Çekirdek sayısı.
- İşlemci özellikleri.
- Desteklenen komut setleri.

gibi bilgiler bulunabilir.

### 8.3. /proc/meminfo

Bellek yönetimiyle ilgili bilgileri gösterir.

```bash
cat /proc/meminfo
```

Önemli alanlardan bazıları:

| Alan | Açıklama |
|---|---|
| MemTotal | Kullanılabilir toplam fiziksel bellek |
| MemFree | Tamamen boş fiziksel bellek |
| MemAvailable | Yeni uygulamalar için tahmini kullanılabilir bellek |
| Buffers | Blok aygıtı tampon belleği |
| Cached | Dosya önbelleği için kullanılan bellek |
| SwapTotal | Toplam takas alanı |
| SwapFree | Boş takas alanı |

### 8.4. /proc/cmdline

Çekirdeğe önyükleyici tarafından iletilen başlangıç parametrelerini görüntüler.

```bash
cat /proc/cmdline
```

### 8.5. journalctl

systemd kullanılan dağıtımlarda çekirdek mesajları sistem günlükleri üzerinden de incelenebilir.

Mevcut açılışın çekirdek mesajları:

```bash
journalctl -k -b
```

Önceki açılışın çekirdek mesajları:

```bash
journalctl -k -b -1
```

### 8.6. lsmod ve modinfo

Çekirdeğe yüklenmiş modülleri görüntülemek için:

```bash
lsmod
```

Bir modül hakkında ayrıntılı bilgi almak için:

```bash
modinfo e1000e
```

Buradaki `e1000e`, Intel Ethernet denetleyicilerinde kullanılan sürücülerden biridir. Sisteminizde farklı bir sürücü bulunabilir.

## 9. Linux Kernel Başlangıç Sürecinin Genel Akış Şeması

Şimdiye kadar incelediğimiz işlemleri bir araya getirdiğimizde çekirdeğin başlangıç süreci genel olarak şu şekilde ilerler:

```text
        BOOTLOADER
             |
             v
   Kernel (vmlinuz) belleğe yüklenir
             |
             v
       Boot Protocol
             |
             v
   Mimariye özgü başlangıç kodu
             |
             v
     Decompressor çalışır
             |
             v
   Sıkıştırılmış kernel açılır
             |
             v
   Mimariye özgü kernel kodu
             |
             v
       start_kernel()
             |
             v
    Temel alt sistemler hazırlanır
             |
             v
      Scheduler / Memory
       IRQ / VFS / vb.
             |
             v
         rest_init()
             |
             v
     İlk kernel thread'leri
       /              \
      v                v
  PID 1             kthreadd
      |
      v
  kernel_init
      |
      v
  Initramfs varsa /init
      |
      v
  Gerçek root filesystem
      |
      v
  Gerçek init programı
      |
      v
  systemd / OpenRC / SysVinit
      |
      v
  Sistem servisleri
      |
      v
  Kullanıcı oturumu
```

**Not:** Bu akış şeması genel bir Linux başlangıç modelidir. Initramfs bulunmayan sistemlerde gerçek kök dosya sistemine geçiş ve init programının başlatılması farklı şekilde gerçekleşebilir.

## 10. Özet

Linux çekirdeği, önyükleyicinin kontrolü devretmesiyle birlikte çalışmaya başlar.

İlk olarak mimariye özgü başlangıç kodları çalıştırılır, gerekli işlemci ve bellek hazırlıkları gerçekleştirilir ve sıkıştırılmış çekirdek imajı açılır.

Ardından `start_kernel()` fonksiyonu çalışarak bellek yönetimi, süreç zamanlayıcısı, kesme altyapısı ve sanal dosya sistemi gibi temel alt sistemleri hazırlar.

Çekirdek başlangıç işlemlerinin devamında PID 1 görevini üstlenecek ilk kullanıcı alanı süreci hazırlanır. Initramfs kullanılıyorsa önce bu ortamın başlangıç programı çalıştırılır ve gerçek kök dosya sistemine geçiş gerçekleştirilir.

Son olarak gerçek init sistemi devreye girerek servisleri başlatır ve işletim sistemini kullanıcı etkileşimine hazır hâle getirir.

---

*Not: Linux çekirdeğinin başlangıç mekanizmaları işlemci mimarisine, çekirdek sürümüne, firmware türüne ve derleme yapılandırmasına göre farklılık gösterebilir. Bu bölümdeki örnekler ağırlıklı olarak x86-64 tabanlı sistemler üzerinden açıklanmıştır.*