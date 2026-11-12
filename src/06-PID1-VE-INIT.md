# PID 1 ve Init Sistemi

Initramfs aşamasında gerçek kök dosya sistemine geçildikten sonra çekirdek, sistemin normal açılışını devam ettirecek olan init programını çalıştırır [22].

Varsayılan olarak kullanılan program genellikle `/sbin/init` yolundadır. Ancak bu yol çekirdek komut satırındaki `init=` parametresiyle değiştirilebilir.

Init programı, kullanıcı alanında başlatılan ilk süreçtir ve **PID 1** numarasına sahiptir [22].

PID 1'in temel görevleri şunlardır:

- Sistemin açılış işlemlerini gerçekleştirmek.
- Gerekli servisleri ve arka plan süreçlerini başlatmak.
- Servislerin durumlarını yönetmek ve gerektiğinde yeniden başlatmak.
- Yeni kullanıcı oturumları için gerekli süreçleri oluşturmak.
- Sistemin kapatılması veya yeniden başlatılması sırasında gerekli işlemleri yürütmek.
- Sahipsiz kalan çocuk süreçleri devralmak ve sonlanan süreçleri temizlemek [27].

Burada önemli bir ayrım vardır: PID 1 bir süreçtir; init sistemi ise bu sürecin yürüttüğü program ve onun sağladığı sistem yönetim mekanizmalarının bütünüdür.

## PID 1'in çalışma mantığı

Linux sistemlerinde süreçler bir ebeveyn-çocuk ilişkisi içerisinde çalışır. Bir süreç sonlandığında, ebeveyn sürecinin bu durumu takip ederek ilgili süreci toplaması gerekir.

Normal bir süreç sonlandığında ebeveyn süreci tarafından beklenmezse zombie (zombi) durumunda kalabilir.

PID 1, ebeveyni sonlanmış süreçlerin devralınmasında özel bir role sahiptir. Bu nedenle init sisteminin yalnızca servisleri başlatması yeterli değildir; süreç yaşam döngüsünü de doğru yönetmesi gerekir.

### PID 1 neden önemlidir?

PID 1, çekirdek tarafından özel olarak ele alınır. Normal süreçlerden farklı olarak sistemin temel kullanıcı alanı süreçlerinin devamlılığında kritik rol oynar.

PID 1 beklenmedik şekilde sonlanırsa çekirdek `Attempted to kill init` hatasıyla kernel panic oluşturur [22].

Örneğin:

```text
Kernel panic - not syncing: Attempted to kill init!
```

Bu nedenle PID 1 olarak çalışan programın güvenilir olması gerekir.

PID ad alanlarında da ilk süreç PID 1 olur. Bu sürecin sonlanması, o ad alandaki diğer süreçlerin çekirdek tarafından sonlandırılmasına yol açar [28].

### PID 1 değiştirilebilir mi?

PID 1'in çalıştırdığı program değiştirilebilir. Ancak bu işlem yeni bir PID 1 oluşturmak anlamına gelmez.

Örneğin initramfs aşamasında:

```sh
exec switch_root /root /sbin/init
```

komutu çalıştırıldığında mevcut süreç, gerçek kök dosya sistemindeki init programını çalıştıracak şekilde değiştirilir.

Burada `exec` mevcut sürecin program görüntüsünü değiştirir; PID numarası korunur [24].

Dolayısıyla:

- PID 1 numarası korunur.
- Eski initramfs başlangıç programı yerini yeni programa bırakır.
- Gerçek sistemin init programı PID 1 olarak çalışmaya devam eder.

## Init sistemleri

Linux dağıtımlarında farklı init sistemleri kullanılabilir. Bunların temel amacı sistem açılışını yönetmek ve kullanıcı alanındaki servislerin çalışmasını sağlamaktır.

Yaygın init sistemleri:

- systemd
- SysVinit
- OpenRC
- s6
- runit
- BusyBox init

Bu yazıda SysVinit, systemd, OpenRC ve BusyBox init üzerinde duracağız.

### Genel karşılaştırma

| Özellik | systemd | SysVinit + SysV-rc | OpenRC | BusyBox init |
|---|---|---|---|---|
| Yapılandırma | Unit dosyaları [43] | Runlevel ve başlangıç betikleri ([44], [45]) | Servis betikleri ([46], [47]) | `inittab` ve betikler ([38], [48]) |
| Bağımlılık yönetimi | Unit bağımlılıkları [43] | Runlevel ve servis betikleri üzerinden ([44], [45]) | Servis bağımlılıkları ([46], [47]) | Yerleşik bağımlılık çözücüsü bulunmaz [48] |

Not: SysVinit, OpenRC ve BusyBox init aynı kapsamda özellik sunmaz. Özellikle servis yönetimi, bağımlılık çözümü ve süreç denetimi açısından aralarında önemli farklar bulunur. Ayrıca OpenRC'de paralel başlatma isteğe bağlıdır.

## SysVinit

SysVinit (System V init), Unix sistemlerinden gelen geleneksel init yaklaşımını Linux üzerinde uygulayan init sistemidir ([44], [45]).
Servislerin başlatılması ve durdurulması için genellikle shell betikleri kullanılır. Sistem açılışında hangi servislerin çalıştırılacağı runlevel adı verilen çalışma seviyeleriyle belirlenir.

### Runlevel

Runlevel, sistemin hangi çalışma durumunda olduğunu ve bu durumda hangi servislerin çalıştırılacağını tanımlar.

Geleneksel SysV runlevel yapısı şöyledir:

| Runlevel | Açıklama |
|---|---|
| 0 | Sistemi kapatma (Halt). |
| 1 | Tek kullanıcılı bakım ve kurtarma modu. |
| S / s | Açılış sırasında kullanılan tek kullanıcılı başlangıç seviyesi. |
| 2 | Çok kullanıcılı mod. |
| 3 | Çok kullanıcılı, grafik arayüzsüz mod. |
| 4 | Kullanıcı tarafından özelleştirilebilir seviye. |
| 5 | Genellikle grafik arayüzlü çok kullanıcılı mod. |
| 6 | Sistemi yeniden başlatma (Reboot). |

Runlevel'ların anlamı dağıtıma göre değişebilir. Örneğin Debian'ın geleneksel SysV yapılandırmasında 2, 3, 4 ve 5 numaralı seviyeler varsayılan olarak aynı servis grubunu çalıştırır [44]. Bu nedenle runlevel 2'nin ağ desteği olmadığı şeklinde genel bir kural bulunmaz.

### Servis betikleri

SysVinit kullanılan sistemlerde servislerin başlangıç betikleri genellikle:

```text
/etc/init.d/
```

dizini altında bulunur.

Örneğin:

```text
/etc/init.d/
├── networking
├── ssh
├── cron
└── nginx
```

Bu betikler genellikle `start`, `stop`, `restart` ve `status` gibi işlemleri destekler.

### Runlevel dizinleri ve sembolik bağlantılar

Hangi servisin hangi runlevel'da çalışacağı aşağıdaki dizinlerde bulunan sembolik bağlantılar aracılığıyla belirlenir:

```text
/etc/rc0.d/
/etc/rc1.d/
/etc/rc2.d/
/etc/rc3.d/
/etc/rc4.d/
/etc/rc5.d/
/etc/rc6.d/
```

Bu dizinlerdeki bağlantılar, asıl servis betiklerini `/etc/init.d/` dizininden gösterir.

Bağlantı isimlerinde kullanılan harfler servis işlemini belirtir:

- **S (Start):** İlgili runlevel'a girildiğinde servisin başlatılmasını sağlar.
- **K (Kill):** İlgili runlevel'a girildiğinde servisin durdurulmasını sağlar.

Örnek:

```text
/etc/rc3.d/
├── S20ssh -> ../init.d/ssh
├── S30cron -> ../init.d/cron
└── K20nginx -> ../init.d/nginx
```

Bağlantı isimlerindeki sayılar, betiklerin çalıştırılma sırasını belirler. Küçük numaralı betikler önce çalıştırılır.

Sistem bir runlevel'a geçerken ilgili dizindeki `K` betikleri `stop`, `S` betikleri ise `start` parametresiyle çalıştırılır.

### Servis yönetimi

SysVinit kullanılan sistemlerde servisleri yönetmek için dağıtıma göre farklı yardımcı komutlar bulunur.

Debian gibi sistemlerde:

```sh
# Servisi başlat
service nginx start

# Servisi durdur
service nginx stop

# Servisi yeniden başlat
service nginx restart

# Servisin açılışta çalışmasını etkinleştir
update-rc.d nginx defaults

# Servisin açılışta çalışmasını devre dışı bırak
update-rc.d nginx disable
```

Burada `service` ve `update-rc.d` komutları SysVinit'in kendisi değil, servis betiklerini ve açılış bağlantılarını yönetmek için kullanılan yardımcı araçlardır.

## systemd

systemd, Linux dağıtımlarında yaygın olarak kullanılan kapsamlı bir init ve sistem yönetim altyapısıdır ([5], [43]).
Debian, Ubuntu, Arch Linux ve Fedora gibi birçok dağıtımda varsayılan olarak kullanılır.

systemd yalnızca servisleri başlatmakla kalmaz; sistem açılışını, servis bağımlılıklarını, zamanlanmış görevleri, dosya sistemi bağlama işlemlerini, oturumları ve kaynak yönetimini de üstlenebilir.

### Unit yapısı

systemd, yönetim işlemlerini Unit adı verilen yapılandırma birimleri üzerinden gerçekleştirir.

Unit dosyaları genellikle INI benzeri bir yapıdadır. Her birim belirli bir sistem kaynağını veya işlemi temsil eder.

Başlıca Unit türleri:

| Uzantı | Açıklama |
|---|---|
| .service | Servisleri ve arka plan süreçlerini yönetir. |
| .target | Birden fazla Unit'i gruplar ve belirli sistem durumlarını tanımlar. |
| .mount | Dosya sistemi bağlama işlemlerini yönetir. |
| .automount | İhtiyaç duyulduğunda dosya sistemlerinin otomatik bağlanmasını sağlar. |
| .timer | Belirli zamanlarda veya takvim kurallarına göre servisleri tetikler. |
| .socket | Ağ soketleri veya yerel IPC soketleri üzerinden servis etkinleştirmeyi sağlar. |
| .path | Dosya ve dizinlerdeki değişiklikleri izleyerek servisleri tetikler. |
| .device | Çekirdek tarafından tanınan donanım aygıtlarını temsil eder. |
| .slice | Süreçleri cgroups üzerinden kaynak yönetimi gruplarına ayırır. |
| .swap | Swap dosyası veya bölümünün etkinleştirilmesini yönetir. |
| .scope | systemd dışında başlatılmış süreç gruplarını takip eder. |

### Target yapısı

Target birimleri, sistemin belirli çalışma durumlarını temsil eder. Geleneksel SysVinit runlevel yapısına benzer bir işlev görürler.

Örneğin:

| Target | Açıklama |
|---|---|
| poweroff.target | Sistemi kapatma. |
| rescue.target | Kurtarma ve bakım modu. |
| multi-user.target | Grafik arayüzsüz çok kullanıcılı çalışma modu. |
| graphical.target | Grafik arayüzlü çok kullanıcılı çalışma modu. |
| reboot.target | Sistemi yeniden başlatma. |
| emergency.target | En temel kurtarma ortamı. |

Örneğin:

```sh
# Varsayılan açılış hedefini görüntüle
systemctl get-default

# Varsayılan hedefi grafik arayüz olarak ayarla
systemctl set-default graphical.target

# Çok kullanıcılı moda geç
systemctl isolate multi-user.target
```

### Servis bağımlılıkları

systemd, servisler arasındaki bağımlılıkları ve başlatma sırasını Unit dosyaları üzerinden yönetir.

Örneğin bir servis başlatılmadan önce ağ servisinin hazır olması gerekiyorsa ilgili bağımlılık tanımlanabilir.

Unit dosyasında:

```ini
[Unit]
Description=Example Service
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=/usr/local/bin/example

[Install]
WantedBy=multi-user.target
```

Burada:

- `Wants=`: İlgili birimin de etkinleştirilmesini ister; ancak onun başarısız olması bu servisin mutlaka başarısız olacağı anlamına gelmez.
- `After=`: Başlatma sırasını belirler. Tek başına ilgili servisin başlatılmasını sağlamaz.
- `WantedBy=`: Servisin hangi hedef üzerinden etkinleştirilebileceğini belirtir.

Daha güçlü bir bağımlılık gerektiğinde `Requires=` gibi direktifler kullanılabilir.

Bu yapı sayesinde systemd, bağımlılıkları dikkate alarak birden fazla servisi paralel başlatabilir.

### Socket Activation

systemd'nin önemli özelliklerinden biri Socket Activation mekanizmasıdır.

Bu mekanizmada bir servis doğrudan açılışta başlatılmak zorunda değildir. Önce ilgili soket dinlemeye alınır. Sokete bağlantı geldiğinde systemd bağlı olduğu servisi başlatabilir.

Örneğin:

```text
          İstemci
             |
             v
      TCP bağlantısı
             |
             v
       socket unit
             |
             v
       service unit
             |
             v
        Uygulama
```

Bu yöntem, sürekli çalışması gerekmeyen servislerde kaynak kullanımını azaltabilir.

### Servis yönetimi

systemd servisleri `systemctl` komutu üzerinden yönetilir.

```sh
# Servisi başlat
systemctl start nginx

# Servisi durdur
systemctl stop nginx

# Servisi yeniden başlat
systemctl restart nginx

# Servis durumunu görüntüle
systemctl status nginx

# Servisi açılışta etkinleştir
systemctl enable nginx

# Servisi açılışta devre dışı bırak
systemctl disable nginx

# Servis günlüklerini görüntüle
journalctl -u nginx
```

### SysVinit uyumluluğu

systemd, uzun süre SysVinit servis betikleriyle geriye dönük uyumluluk sağlamıştır. Bu sayede eski `/etc/init.d/` betiklerinin bir kısmı systemd tarafından çalıştırılabilmiştir.

Ancak bu uyumluluk sürüme ve dağıtımın derleme yapılandırmasına bağlıdır. systemd 260 sürümünden itibaren SysV uyumluluk desteği kaldırılmıştır [49]. Dolayısıyla güncel sistemlerde SysV betiklerinin systemd altında çalışacağını varsaymak doğru değildir.

## OpenRC

OpenRC, modüler yapıda, shell betikleri tabanlı servis yönetimi sağlayan bir init sistemidir ([46], [47]).
Gentoo ve Alpine Linux gibi dağıtımlarda kullanılabilir.

OpenRC, geleneksel SysV yaklaşımının basitliğini korurken servis bağımlılıklarını çözme, runlevel yönetimi ve isteğe bağlı paralel başlatma gibi özellikler sunar.

OpenRC'nin önemli bir farkı, systemd gibi sürekli çalışan bir servis yöneticisi olmamasıdır. Genellikle PID 1 tarafından açılış sırasında çağrılır, servisleri başlatır ve görevini tamamladıktan sonra sonlanır.

### Runlevel

OpenRC'de çalışma seviyeleri sayılar yerine isimlerle tanımlanır.

| Runlevel | Açıklama |
|---|---|
| sysinit | Sistem için en temel başlangıç işlemlerini gerçekleştirir. |
| boot | Açılış sırasında gerekli temel servisleri başlatır. |
| default | Normal sistem çalışma seviyesidir. |
| nonetwork | Ağ servislerinin bulunmadığı veya kullanılmadığı yerel çalışma seviyesi. |
| single | Tek kullanıcılı bakım modu. |
| shutdown | Sistem kapanırken servislerin durdurulması için kullanılır. |

OpenRC'nin tipik açılış sırası:

```text
      sysinit
         |
         v
        boot
         |
         v
       default
         |
         v
   Normal sistem
```

### Servis betikleri

OpenRC servis betikleri genellikle:

```text
/etc/init.d/
```

dizini altında tutulur.

Örnek:

```sh
#!/sbin/openrc-run

description="Example Service"

depend() {
    need net
    use dns
}

start() {
    ebegin "Starting example service"
    start-stop-daemon --start --exec /usr/local/bin/example
    eend $?
}

stop() {
    ebegin "Stopping example service"
    start-stop-daemon --stop --exec /usr/local/bin/example
    eend $?
}
```

OpenRC betikleri bağımlılıklarını `depend()` fonksiyonu içerisinde tanımlar.

Kullanılabilecek bazı bağımlılık ifadeleri:

- `need`: Zorunlu bağımlılık.
- `use`: İlgili servis mevcut runlevel'da bulunuyorsa başlatılmasını ister.
- `want`: İsteğe bağlı olarak ilgili servisin başlatılmasını ister.
- `before`: İlgili servisten önce çalışılması gerektiğini belirtir.
- `after`: İlgili servisten sonra çalışılması gerektiğini belirtir.

### Servislerin etkinleştirilmesi

OpenRC'de servislerin hangi runlevel içerisinde çalışacağı `/etc/runlevels/` dizinindeki sembolik bağlantılarla belirlenir.

Örnek:

```text
/etc/runlevels/
├── boot/
├── default/
└── sysinit/
```

Bir servisi varsayılan runlevel'a eklemek için:

```sh
rc-update add nginx default
```

Servisi runlevel'dan kaldırmak için:

```sh
rc-update del nginx default
```

Bu komutlar servisin otomatik başlatılma yapılandırmasını değiştirir. Servisi o anda başlatmak için ayrıca `rc-service` kullanılabilir.

### Paralel başlatma

OpenRC, bağımlılık grafiğini kullanarak servislerin hangi sırayla başlatılacağını belirler.

Birbirine bağımlı olmayan servisler paralel çalıştırılabilir. Ancak paralel başlatma varsayılan olarak etkin değildir; `/etc/rc.conf` içerisinde:

```sh
rc_parallel="YES"
```

şeklinde yapılandırılabilir.

### Servis yönetimi

```sh
# Servisi başlat
rc-service nginx start

# Servisi durdur
rc-service nginx stop

# Servisi yeniden başlat
rc-service nginx restart

# Servis durumunu görüntüle
rc-service nginx status

# Aktif runlevel ve servisleri görüntüle
rc-status
```

OpenRC, servislerin açılışta otomatik çalışmasını ve bağımlılıklarını yönetir. Ancak sürekli çalışan bir servis gözetmeni değildir. Süreçlerin sürekli denetlenmesi ve çöken servislerin otomatik yeniden başlatılması gerektiğinde ek araçlardan yararlanılabilir.

## BusyBox init

BusyBox init, BusyBox paketinin içerisinde bulunan küçük ve temel özelliklere sahip bir init uygulamasıdır ([38], [48]).
Özellikle gömülü sistemlerde, kurtarma ortamlarında ve düşük kaynak tüketiminin önemli olduğu sistemlerde tercih edilir.

SysVinit'e benzer bir `inittab` yapılandırma dosyası kullanır. Ancak geleneksel runlevel mekanizmasını desteklemez.

### inittab

BusyBox init'in temel yapılandırma dosyası:

```text
/etc/inittab
```

dosyasıdır.

Dosyanın satır yapısı şöyledir:

```text
<id>:<runlevels>:<action>:<process>
```

Buradaki alanlar:

- `id`: Sürecin kullanılacağı terminali belirtir.
- `runlevels`: BusyBox init tarafından dikkate alınmaz.
- `action`: Komutun hangi durumda çalıştırılacağını belirtir.
- `process`: Çalıştırılacak komutu veya betiği belirtir.

BusyBox init tarafından desteklenen bazı action türleri:

| Action | Açıklama |
|---|---|
| sysinit | Başlangıç işlemlerini gerçekleştirir ve tamamlanmasını bekler. |
| wait | Komutu çalıştırır ve tamamlanmasını bekler. |
| once | Komutu bir kez çalıştırır, tamamlanmasını beklemez. |
| respawn | Süreç sonlanırsa yeniden başlatır. |
| askfirst | Kullanıcıdan Enter tuşuna basmasını bekleyerek süreci başlatır. |
| ctrlaltdel | Ctrl + Alt + Del tuşlarına basıldığında çalıştırılır. |
| shutdown | Kapanış işlemleri sırasında çalıştırılır. |
| restart | Init sürecinin yeniden başlatılması veya başka bir programla değiştirilmesi için kullanılır. |

Örnek bir `/etc/inittab`:

```text
# Açılış betiği
::sysinit:/etc/init.d/rcS

# Kullanıcı girişi için terminal
tty1::respawn:/sbin/getty 38400 tty1

# Ctrl + Alt + Del
::ctrlaltdel:/sbin/reboot

# Kapanış işlemleri
::shutdown:/bin/umount -a -r
```

BusyBox init'in önemli özelliklerinden biri, `inittab` dosyası bulunmadığında da çalışabilmesidir.

Bu durumda kendi varsayılan davranışını kullanır. Varsayılan davranış içerisinde genellikle:

```text
::sysinit:/etc/init.d/rcS
::askfirst:/bin/sh
```

gibi işlemler bulunur.

Dolayısıyla `inittab` bulunmadığında `/etc/init.d/rcS` başlangıç betiği varsayılan olarak çalıştırılır.

### BusyBox init ile OpenRC kullanımı

BusyBox init, OpenRC ile birlikte kullanılabilir. Bu yapıda BusyBox init PID 1 olarak çalışırken OpenRC açılış işlemlerini ve servis yönetimini gerçekleştirir.

Örnek yapılandırma:

```text
# OpenRC başlangıç aşamaları
::sysinit:/sbin/openrc sysinit
::wait:/sbin/openrc boot
::wait:/sbin/openrc default

# Ctrl + Alt + Del
::ctrlaltdel:/sbin/openrc reboot

# Kapanış
::shutdown:/sbin/openrc shutdown

# Terminal oturumu
tty1::respawn:/sbin/getty 38400 tty1
```

Burada BusyBox init, belirtilen işlemleri sırasıyla çalıştırır. OpenRC ise servis bağımlılıklarını ve runlevel yapılandırmasını değerlendirir.

Bu örnek, BusyBox init'in tek başına sunmadığı servis yönetimi özelliklerinin başka bir araçla tamamlanabileceğini gösterir.

## Özel init oluşturulması

Bir Linux sisteminde systemd, SysVinit veya OpenRC gibi hazır bir init sistemi kullanmak zorunlu değildir. İstenirse PID 1 olarak çalışacak özel bir program veya betik hazırlanabilir.

Örneğin çok basit bir sistemde:

- Gerekli dosya sistemleri bağlanabilir.
- Donanım aygıtları hazırlanabilir.
- Gerekli servisler başlatılabilir.
- Terminal oturumları açılabilir.
- Kapanış işlemleri yönetilebilir.

Ancak bu yaklaşımın bazı önemli sorumlulukları vardır.

Özel init programının:

- Çocuk süreçleri takip etmesi ve zombie süreçleri temizlemesi.
- Servislerin çökmesini tespit etmesi ve gerekiyorsa yeniden başlatması.
- SIGTERM, SIGINT ve diğer sinyalleri doğru yönetmesi.
- Sistem kapatılırken servisleri uygun sırayla durdurması.
- Dosya sistemlerinin güvenli şekilde ayrılmasını sağlaması.
- Gerekli servis bağımlılıklarını ve başlangıç sırasını yönetmesi gerekir.

Bu özellikler olmadan yalnızca birkaç servisi arka planda başlatan bir betik, tam teşekküllü bir servis yöneticisi sayılmaz.

### Basit özel init örneği

Aşağıdaki örnek yalnızca PID 1 olarak çalışacak basit bir başlangıç betiğinin temel fikrini gösterir. Üretim sistemlerinde kullanılabilecek güvenli ve eksiksiz bir init uygulaması değildir.

```sh
#!/bin/sh

# Çalıştırılabilir dosyaların aranacağı yollar.
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Gerekli çalışma dizinleri.
mkdir -p /run /tmp

# Kök dosya sistemini yazılabilir bağla.
mount -o remount,rw /

# fstab içerisindeki dosya sistemlerini bağla.
mount -a

# Hostname ayarla.
hostname "$(cat /etc/hostname)"

# Gerekli servisleri başlat.
# Örnek olarak burada özel servis başlatma komutları bulunabilir.

# PID 1 olarak çalışan programın sonlanmasını önle.
# Bu yalnızca örnek amaçlıdır; gerçek bir init yerine geçmez.
exec /bin/sh
```

Bu örnekte servis yönetimi, süreç denetimi ve güvenli kapatma işlemleri özellikle uygulanmamıştır.

Örneğin:

```sh
exec sleep infinity
```

kullanarak PID 1'in sonlanmasını önlemek mümkündür. Ancak bu, çalışan bir init sistemi oluşturmaz. Böyle bir süreç servisleri yönetmez, kapanış işlemlerini gerçekleştirmez ve servislerin durumunu takip etmez.

Ayrıca systemd-logind gibi bileşenler systemd'nin sunduğu diğer altyapılarla yakından ilişkilidir. Bu nedenle systemd bileşenlerini başka bir init altında doğrudan çalıştırmak her zaman mümkün değildir. Alternatif olarak elogind gibi bağımsız çözümler kullanılabilir.

## Açılış sürecinin genel görünümü

Önceki bölümlerde anlattığımız açılış sürecini PID 1 aşamasıyla birlikte özetlersek:

```text
              BIOS / UEFI
                   |
                   v
                Bootloader
                   |
                   v
                Linux Kernel
                   |
                   v
                Initramfs
                   |
                   v
         Gerçek kök dosya sistemi
                   |
                   v
             switch_root
                   |
                   v
             Asıl PID 1
                   |
          +--------+--------+
          |        |        |
          v        v        v
       Servisler  TTY    Mount işlemleri
          |        |        |
          +--------+--------+
                   |
                   v
             Kullanıma hazır
                Linux
```

PID 1 servisleri başlattıktan sonra kullanıcıya bir terminal oturumu sunulabilir. Sıradaki bölümde TTY ve getty'nin terminali nasıl hazırladığını, shell'in de kullanıcı komutlarını nasıl çalıştırdığını izleyeceğiz.
