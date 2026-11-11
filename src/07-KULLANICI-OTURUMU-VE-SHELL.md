# Kullanıcı Terminali ve Shell

Linux ve Unix benzeri işletim sistemlerinde kernel ve init sistemi temel çalışma ortamını hazırladıktan sonra kullanıcıların sistemle komut satırı üzerinden etkileşim kurabilmesi için terminal süreçleri başlatılır.

Bu amaçla kullanılan temel bileşenler TTY, sanal konsollar, getty ve shell'dir.

Terminal, kullanıcının komut girdiği ve programların çıktılarını görüntülediği arayüzü ifade eder. Shell ise bu terminal üzerinden girilen komutları yorumlayan ve çalıştıran programdır.

Bu bölümde Linux'un terminal altyapısı, sanal konsollar, getty ve shell çalışma mantığı ele alınacaktır.

## TTY ve Sanal Konsollar

TTY (Teletypewriter), kullanıcı ile işletim sistemi arasında metin tabanlı etkileşim sağlayan terminal arayüzünü ifade eder.

İlk Unix sistemlerinde TTY kavramı fiziksel terminal cihazlarından gelmektedir. Günümüzde Linux, fiziksel terminallerin yanı sıra sanal konsollar ve yazılım tabanlı terminaller de destekler.

### Linux sanal konsolları

Linux, grafik arayüz kullanılmadan da birden fazla sanal konsol sunabilir.

Bu konsollar genellikle `tty1`, `tty2`, `tty3` gibi isimlerle ifade edilir.

Örneğin:

```text
/dev/tty1
/dev/tty2
/dev/tty3
/dev/tty4
```

Her sanal konsol bağımsız bir metin tabanlı çalışma ortamı sağlar. Kullanıcılar klavyeden Ctrl + Alt + F1, Ctrl + Alt + F2 gibi tuş kombinasyonlarıyla konsollar arasında geçiş yapabilir.

Kullanılan sistemin yapılandırmasına göre aktif konsol numaraları ve geçiş tuşları değişebilir.

Sanal konsolları görüntülemek için:

```sh
# Mevcut terminali görüntüle
tty

# TTY aygıtlarını listele
ls -l /dev/tty*

# Aktif sanal konsolu görüntüle
fgconsole
```

### TTY ve PTY farkı

Linux'ta terminal altyapısı yalnızca fiziksel veya sanal konsollardan ibaret değildir. Yazılım tarafından oluşturulan sözde terminaller de bulunur.

PTY (Pseudo Terminal), bir programın terminal aygıtı gibi davranabilmesini sağlayan mekanizmadır.

PTY iki uçtan oluşur:

- **Master:** Terminali oluşturan uygulamanın veya terminal sunucusunun kullandığı uç.
- **Slave:** Shell veya terminal üzerinde çalışan uygulamaların bağlandığı uç.

Örneğin SSH bağlantıları, terminal emülatörleri ve tmux gibi terminal çoklayıcıları PTY kullanabilir.

```text
       Terminal uygulaması
               |
               v
          PTY Master
               |
               v
          PTY Slave
               |
               v
          Shell / Komutlar
```

PTY aygıtları genellikle `/dev/pts/` altında bulunur.

```sh
# Oluşturulmuş PTY aygıtlarını listele
ls -l /dev/pts/

# Mevcut terminalin türünü görüntüle
tty
```

Örneğin:

```text
/dev/pts/0
/dev/pts/1
/dev/pts/2
```

Bu aygıtlar, grafik terminal emülatörleri ve SSH oturumları gibi yazılım tabanlı terminal bağlantılarında kullanılabilir.

## Getty

Getty, bir terminal üzerinde metin tabanlı çalışma ortamını hazırlayan ve terminali kullanıcı etkileşimine hazır hale getiren programdır.

Genellikle init sistemi tarafından başlatılır ve ilgili TTY üzerinde çalışır.

Getty'nin temel görevleri:

- Terminal aygıtını açmak.
- Terminalin haberleşme ve çalışma ayarlarını yapmak.
- Terminalin kullanılabilir durumda olmasını sağlamak.
- İlgili terminal üzerinde sonraki programın çalıştırılmasını sağlamak.

Linux sistemlerinde yaygın olarak kullanılan getty uygulamaları:

| Araç | Açıklama |
|---|---|
| agetty | util-linux paketinin sağladığı yaygın getty uygulaması. |
| mingetty | Minimal sistemlerde kullanılan getty uygulaması. |
| BusyBox getty | BusyBox içerisinde bulunan getty uygulaması. |

### Getty çalıştırma örneği

```sh
/sbin/agetty --noclear 38400 tty1 linux
```

Komutun parametreleri:

| Parametre | Açıklama |
|---|---|
| --noclear | Terminal ekranının temizlenmesini engeller. |
| 38400 | Seri bağlantılar için baud hızını belirtir. |
| tty1 | Kullanılacak terminal aygıtını belirtir. |
| linux | Terminal türünü belirtir. |

38400 değeri özellikle seri terminal bağlantılarında kullanılan bir haberleşme hızıdır. Yerel sanal konsollarda bu parametre fiziksel bir seri bağlantı hızı anlamına gelmez.

Terminal türü ise `TERM` ortam değişkeninin değerini belirler. Örneğin:

- `linux`: Linux sanal konsolu.
- `vt100`: VT100 uyumlu terminal.
- `xterm`: X terminal emülatörü.
- `xterm-256color`: 256 renk destekli xterm uyumlu terminal.

### Getty'nin init sistemi tarafından yönetilmesi

Getty süreçleri genellikle init sistemi tarafından yönetilir.

BusyBox init kullanılan bir sistemde `/etc/inittab` içerisinde:

```text
tty1::respawn:/sbin/getty 38400 tty1
tty2::respawn:/sbin/getty 38400 tty2
```

şeklinde tanımlanabilir.

Buradaki `respawn` ifadesi, getty süreci sonlandığında init tarafından yeniden başlatılmasını sağlar.

systemd kullanılan sistemlerde ise sanal konsollar genellikle `getty@.service` şablon birimi üzerinden yönetilir.

```sh
# tty1 getty durumunu görüntüle
systemctl status getty@tty1.service

# tty2 getty servisini başlat
systemctl start getty@tty2.service

# tty2 getty servisini durdur
systemctl stop getty@tty2.service
```

## Shell (Kabuk)

Shell, kullanıcı ile işletim sistemi arasında komut satırı üzerinden etkileşim sağlayan programdır.

Kullanıcının girdiği komutları yorumlar, gerekli programları çalıştırır ve sonuçları terminal üzerinden görüntüler.

Shell üzerinden:

- Dosya ve dizin işlemleri gerçekleştirilebilir.
- Sistem komutları çalıştırılabilir.
- Programlar başlatılabilir.
- Ortam değişkenleri yönetilebilir.
- Komutlar birbirine bağlanabilir.
- Shell betikleri çalıştırılabilir.

Shell, kernel'in kendisi değildir. Kullanıcı alanında çalışan bir programdır ve ihtiyaç duyduğu işlemler için sistem çağrıları üzerinden kernel ile iletişim kurar.

### Yaygın shell türleri

Linux sistemlerinde farklı özelliklere sahip birçok shell uygulaması bulunur.

| Shell | Açıklama |
|---|---|
| sh | Geleneksel Unix shell arayüzünü ifade eder. Genellikle POSIX uyumlu bir shell uygulamasına sembolik bağlantıdır. |
| ash | Hafif ve POSIX uyumlu bir shell uygulamasıdır. BusyBox içerisinde de bulunur. |
| dash | Debian Almquist Shell. Hafif, hızlı ve POSIX uyumlu bir shell uygulamasıdır. |
| bash | Bourne Again Shell. Gelişmiş betik özellikleri ve yaygın kullanımıyla bilinir. |
| zsh | Gelişmiş otomatik tamamlama, özelleştirme ve etkileşimli kullanım özellikleri sunar. |
| fish | Sözdizimi vurgulaması, otomatik öneriler ve kullanıcı dostu etkileşimli özellikleriyle öne çıkar. |

### /bin/sh ve diğer shell'ler

Linux sistemlerinde `/bin/sh`, geleneksel Unix shell arayüzünü temsil eder.

Ancak bu dosya her zaman bağımsız bir shell uygulaması değildir. Genellikle sistemin tercih ettiği POSIX uyumlu shell uygulamasına yönlendirilmiş sembolik bağlantıdır.

Örneğin:

| Dağıtım | /bin/sh bağlantısı |
|---|---|
| Debian | Genellikle /bin/dash |
| Arch Linux | Genellikle /bin/bash |
| Alpine Linux | Genellikle /bin/busybox |

Burada önemli bir ayrım vardır: `/bin/sh` ile kullanıcıların etkileşimli olarak kullandığı varsayılan shell aynı olmak zorunda değildir.

Örneğin Debian sisteminde:

```text
/bin/sh  -> /bin/dash
/bin/bash
/bin/zsh
```

şeklinde bir yapı bulunabilir.

Bir kullanıcı Bash kullanırken sistem betikleri `/bin/sh` üzerinden Dash ile çalıştırılabilir.

Bu nedenle POSIX uyumlu shell betikleri yazılırken Bash'e özel özelliklerin kullanılmamasına dikkat edilmelidir.

### Shell'in çalışma biçimleri

Shell'ler farklı çalışma biçimlerinde kullanılabilir.

| Tür | Açıklama |
|---|---|
| Interactive shell | Kullanıcıdan komut alır ve sonuçları terminale yazdırır. |
| Non-interactive shell | Genellikle bir betik veya komut çalıştırmak için kullanılır. |
| Login shell | Kullanıcının oturum başlangıcında başlatılan shell'dir. |
| Non-login shell | Mevcut bir oturum içerisinden başlatılan yeni shell'dir. |

Bu çalışma biçimleri shell'in hangi yapılandırma dosyalarını okuyacağını ve ortamını nasıl hazırlayacağını etkiler.

### Shell yapılandırma dosyaları

Shell'ler başlangıç sırasında belirli yapılandırma dosyalarını okuyabilir. Bu dosyalarda ortam değişkenleri, komut takma adları ve kullanıcı tercihleri tanımlanabilir.

Bash için yaygın yapılandırma dosyaları:

| Dosya | Açıklama |
|---|---|
| /etc/profile | Sistem genelindeki login shell ayarları. |
| ~/.bash_profile | Kullanıcıya özel Bash login shell ayarları. |
| ~/.bash_login | Bash tarafından alternatif login yapılandırması olarak kullanılabilir. |
| ~/.profile | Kullanıcıya özel genel login ayarları. |
| ~/.bashrc | Etkileşimli Bash shell ayarları. |
| /etc/bash.bashrc | Debian gibi dağıtımlarda sistem genelindeki etkileşimli Bash ayarları. |

Bash'in login ve non-login çalışma biçimlerine göre okuduğu dosyalar farklıdır.

Örneğin etkileşimli non-login Bash genellikle `~/.bashrc` dosyasını okur. Login Bash ise öncelikle `~/.bash_profile`, `~/.bash_login` veya `~/.profile` dosyalarından uygun olanı değerlendirir.

Diğer shell uygulamalarının yapılandırma dosyaları ve yükleme sıraları farklı olabilir.

### Shell bilgilerini görüntüleme

```sh
# Kullanıcının shell bilgisini görüntüle
getent passwd "$USER"

# Mevcut terminal aygıtını görüntüle
tty

# Çalışan shell'in çalıştırılabilir dosyasını görüntüle
readlink -f /proc/$$/exe

# Terminal türünü görüntüle
echo "$TERM"

# Shell ortam değişkenini görüntüle
echo "$SHELL"

# Kullanılabilir shell listesini görüntüle
cat /etc/shells
```

Burada `$SHELL` değişkeni genellikle kullanıcının varsayılan shell'ini gösterir. O anda çalışan shell'i belirlemek için tek başına yeterli değildir.

## SSH ve Uzaktan Terminal Erişimi

SSH (Secure Shell), ağ üzerinden başka bir Linux veya Unix sistemine güvenli şekilde bağlanmayı sağlayan protokoldür.

SSH sayesinde uzak sistemde terminal oturumu açılabilir ve komut satırı üzerinden işlemler gerçekleştirilebilir.

Varsayılan SSH portu TCP 22'dir.

Örnek bağlantı:

```sh
ssh kullanici@192.168.1.10
```

SSH bağlantısı sırasında etkileşimli terminal talep edilirse sunucu tarafında genellikle bir PTY oluşturulur. Uzak sistemde kullanıcının shell programı bu terminal üzerinden çalıştırılır.

PTY olmadan da SSH üzerinden komut çalıştırmak mümkündür:

```sh
ssh kullanici@192.168.1.10 "uname -a"
```

Bu örnekte uzak sistemde komut çalıştırılır; ancak etkileşimli bir terminal oturumu oluşturulmaz.

SSH bağlantısında PTY tahsisini zorlamak için:

```sh
ssh -t kullanici@192.168.1.10
```

komutu kullanılabilir.

Bu özellik özellikle uzak sistemlerde interaktif terminal gerektiren programların çalıştırılmasında önemlidir.

## Genel Akış

Linux sisteminde terminalden shell'e kadar gerçekleşen süreç genel olarak şu şekildedir:

```text
          Linux Kernel
                |
                v
            Init (PID 1)
                |
                v
         Sanal Konsol (TTY)
                |
                v
              Getty
                |
                v
         Terminal hazır hale gelir
                |
                v
           Shell başlatılır
                |
                v
        Komutlar yorumlanır
                |
                v
         Programlar çalışır
                |
                v
       Kernel ile iletişim
```

Bu yapı sayesinde Linux, grafik arayüz olmadan da tamamen terminal üzerinden yönetilebilir. Sunucular, gömülü sistemler ve minimal Linux dağıtımları için TTY ve shell altyapısı temel kullanıcı etkileşim yöntemlerinden biridir.

Böylece firmware'in donanımı başlatmasıyla başlayan akış, kullanıcının komut çalıştırabildiği shell oturumuna ulaşır. Bu, çalışmada izlediğimiz önyükleme zincirinin son halkasıdır.
