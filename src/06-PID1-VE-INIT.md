# PID1 ve Init sistemi
Initramfs kurulu olan sisteme geçiş yaptıktan sonra çekirdek parametresinde belirtilen init dosyasını (varsayılan /sbin/init) çalıştırır.
Bu init artık sistem çalıştığı sürece kapatılmaz veya başka bir sürece devredilmez.
Init sisteminin görevi sistem için gereken servisleri başlatmak, kullanıcıdan gelen komuta göre yönetmek ve gerektiğinde sistemi kapatmak veya yeniden başlatmaktır.

Populer init sistemleri: systemd, sysv-init, openrc, s6, runit, busybox init ...

Bu yazıda sysv-init,  systemd, openrc  ve busybox init üzerine değineceğiz. Başlıca aşağıdaki gibi kıyaslanabilir.

| Servis yöneticisi | Paralel Başlatma |  Hafiflik | Bağımlılık Yönetimi | Servis dosyası | Kullanım amacı |
|-------------------|------------------|----------|---------------------|----------------|----------------|
| systemd           | Var              | Karmaşık | Var                 | Unit dosyaları | Genel amaçlı   |
| sysv-init         | -                | Orta     | -                   | Shell script   | Eski / Geleneksel dağıtımlar|
| openrc            | Var              | Hafif    | Var                 | Shell script   | Genel amaçlı   |
| busybox init      | -                | Minimal  | -                   | -              | Gömülü sistemler / Düşük boyutlu sistemler |


## Sysv-init
Köklü ve uzun yıllardır kullanılan bir init sistemidir.

Runlevel adı verilen çalışma düzeylerine sahiptir.

| Runlevel   |  Açıklama |
|----|---|
|0 | Sistemi kapatma (Halt).|
|1 / S | Tek kullanıcılı mod (Single-user mode). Genelde kurtarma ve bakım işlemleri için kullanılır, ağ servisleri kapalıdır.|
|2 | Çok kullanıcılı mod (Multi-user mode), ancak ağ desteği (NFS vb.) yoktur.|
|3 | Grafik arayüzsüz (CLI) tam çok kullanıcılı mod. Sunucularda varsayılan moddur.|
|4 | Kullanıcıya özel tanımlanabilir boş seviye (Genelde kullanılmaz).|
|5 | Grafik arayüzlü (GUI) masaüstü modu. Masaüstü Linux dağıtımlarında varsayılan moddur.|
|6 | Sistemi yeniden başlatma (Reboot).|

* Ana Betik Deposu: Tüm servislerin başlatma, durdurma ve yeniden başlatma komutlarını içeren ana betikler /etc/init.d/ dizini altında tutulur.
* Seviye Dizinleri: Her runlevel için ayrı bir dizin bulunur: /etc/rc0.d/, /etc/rc1.d/, /etc/rc3.d/ vb.
* Sembolik Linkler (K ve S Harfleri): Bu rcX.d dizinlerinin içinde, /etc/init.d/ altındaki asıl betiklere yönlendirilmiş sembolik bağlar (symlink) yer alır. Bu bağların isimleri çok önemlidir:
	* S (Start): Sistem o runlevel'a girdiğinde bu servisin başlatılacağını gösterir (Örn: S20nginx).
	* K (Kill): Sistem o runlevel'a girdiğinde veya çıkış yaparken bu servisin durdurulacağını gösterir (Örn: K20nginx).

Sysv-init servislerini yönetmek için `service` ve `update-rc.d` komutları kullanılır.


## Systemd
Debian, Archlinux ve Fedora gibi dağıtımlarda varsayılan olarak kullanılan init sistemidir.
Sysv-init yerine geçmesi amacı ile geliştirilmeye başlanmıştır. Sysv-init servisleri ile uyumludur.
Servisleri paralel olarak başlatabilir ve servisler arası bağımlılık çözebilir.

Systemd, yönetim işlemlerini Unit (Birim) adı verilen yapılandırma dosyalarıyla gerçekleştirir. Çeşitli türleri bulunur:

| uzantı | Açıklama |
|------|-----|
| .service | Arka planda çalışan servisleri (daemon) başlatır ve durdurur (Örn: nginx.service).|
|.target | Sistem durumlarını gruplar (SysVinit'teki runlevel mantığı). Örneğin, multi-user.target grafik arayüzsüz çok kullanıcılı modu, graphical.target ise masaüstü ortamını ifade eder.|
|.mount / .automount | Dosya sistemlerinin bağlanma noktalarını yönetir.|
|.timer | Cron işleri gibi, belirli zamanlarda veya olaylarda servislerin tetiklenmesini sağlar.|
|.socket | Ağ soketlerini veya IPC (süreçler arası iletişim) kanallarını yönetir. İlgili porta bir istek geldiğinde, bağlı olduğu .service dosyasını otomatik olarak tetikler (Socket Activation).|
|.path | Belirli bir dosya veya dizindeki değişiklikleri (izleme/izleme) takip eder. Dosyada bir değişiklik olduğunda bir servisi tetiklemek için kullanılır.|
|.device | Çekirdek (Kernel) tarafından tanınan bir donanım aygıtını systemd birimi haline getirir. Donanım tabanlı bağımlılıklar oluşturmak için idealdir.|
|.slice | Kaynak yönetimini (CPU, bellek, I/O) gruplamak için kullanılır. Süreçlerin ne kadar sistem kaynağı tüketeceğini sınırlandırmak için cgroups mimarisinden yararlanır.|

Systemd servislerini yönetmek için `systemctl` komutu kullanılır.

## OpenRC

OpenRC kabuk betiği (shell script) tabanlı, modüler bir init sistemidir.
Gentoo ve Alpine Linux gibi dağıtımlarında varsayılan olarak kullanılan init sistemidir.
Sysv-init gibi geleneksel sistemlerin hafifliğini korurken, bağımlılık takibi gibi modern özellikleri sunar.

OpenRC'de sistem durumları Runlevel mantığıyla yönetilir ancak numaralar yerine isimlendirilmiş seviyeler kullanılır:

| Runlevel | Açıklama |
|------|-----|
| boot | Sistem açılırken temel servisleri (dosya sistemlerinin bağlanması, donanım tespiti vb.) başlatır.|
| default | Açılıştan sonra sistemin normal çalışma modudur. Çoğu ağ servisi ve kullanıcı uygulaması burada çalışır.|
| nonetwork | Ağ servislerinin devre dışı bırakıldığı, yerel modda çalışma seviyesidir.|
| single | Tek kullanıcılı (root) kurtarma ve bakım modudur.|
| shutdown | Sistemi güvenli bir şekilde kapatmak için tüm servisleri durdurur.|

* Ana Betik Deposu: Sysv-init ile aynı şekilde /etc/init.d içerisinde bulunur.
* Seviye Dizinleri ve Yapılandırma: Servislerin hangi runlevel'da çalışacağı /etc/runlevels/ dizini altındaki klasörlerde (boot, default vb.) sembolik linkler (symlink) aracılığıyla belirlenir.
* Openrc Systemd ile benzer şekilde servis bağımlılığı çözme ve paralel servis başlatma özelliğine sahiptir.

Openrc servislerini yönetmek için `rc-update` ve `rc-service` komutları kullanılır.


## Busybox init
Sysv-init ile benzerdir fakat runlevel mantığı bulunmaz. Yalnızca */etc/inittab* yapılandırma dosyası bulunur.
Bu dosya bulunmadığı durumda `/etc/init.d/rcS` dosyası kullanılır.

* **Not:** Busybox init bazı durumlarda openrc veya sysv-init ile karışık kullanılabilir. Örneğin:

```
# Açılış yapılandırması
::sysinit:/sbin/openrc sysinit
::wait:/sbin/openrc boot
::wait:/sbin/openrc default
::ctrlaltdel:/sbin/openrc reboot
::shutdown:/sbin/openrc shutdown
# Tty1 üzerinde giriş oluşturmak için.
tty1::respawn:/sbin/getty 38400 tty1
```

# Özel init
Bir servis yöneticisi kullanmak yerine kendi init dosyamızı oluşturabiliriz. Örneğin:
```sh
## Başlangıç
# Çevresel değişken ayarı
export PATH=/bin:/sbin:/usr/bin:/usr/sbin
source /etc/profile
## Disk bağlama
# Kök dizini yazılabilir yap
mount -o remount,rw /
# fstab içerisindeki diskleri bağla
mount -a
## Devd
# systemd-udevd başlatma
/lib/systemd/systemd-udevd --daemon &
# Modülleri yükleme
udevadm trigger -c add
udevadm settle
## Açılış ayarları
# hostname ayarlama
hostname $(cat /etc/hostname)
## Servisleri başlatma
# Dbus
mkdir -p /run/dbus/
dbus-daemon --system --nofork &
# Network Manager
NetworkManager &
# Logind (systemd-logind)
/lib/systemd/systemd-logind &
# Lightdm
lightdm &
### PID1 kapanmaması için
exec sleep inf
```

* **Not:** Yukarıdaki init servis yönetimi (örneğin servisi yeniden başlatma, durdurma, etkinleştirme, devre dışı bırakma) özelliğine sahip olmadığı için servis yöneticisi olarak kabul edilmez.

* **Not:** PID1 (init) kapandığı durumda çekirdek çöker (kernel panic: kill init).