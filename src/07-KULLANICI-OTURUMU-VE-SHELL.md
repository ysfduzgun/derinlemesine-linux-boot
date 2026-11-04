# Kullanıcı Oturumu ve Shell
Linux ve Unix benzeri işletim sistemlerinde `init` (PID 1) sistemi donanımı ve temel servisleri hazır hale getirdikten sonra, kullanıcının sistemle etkileşime girebilmesi için bir giriş arayüzü başlatır.
Bu arayüz grafiksel (Display Manager) veya metin tabanlı (getty) olabilir.

## Giriş Ekranı ve Oturum Başlatma
Giriş ekranları, kullanıcının sisteme güvenli bir şekilde erişmesini sağlar.
Kullanıcı adı ve parola gibi kimlik bilgilerini alarak arka planda **PAM (Pluggable Authentication Modules)** kullanarak doğrulama yapar.
Doğrulama başarılı olursa kullanıcı oturumu (session) başlatılır.

### Grafiksel Giriş Yöneticileri (Display Managers)

Masaüstü ortamlarına (GNOME, KDE, XFCE vb.) geçiş yapmak için kullanılır.

| Adı | Araç Seti | Masaüstü | Açıklama |
|-----|-----------|----------|----------|
| GDM (GNOME Display Manager) | Gtk | GNOME | Gnome ile tam uyumludur |
| SDDM (Simple Desktop Display Manager) | Qt | KDE Plasma, LXQt | Qml tabanlı özelleştirilebilir arayüze sahiptir |
| LightDM | Gtk / Qt | Xfce, Mate, Lxde, Cinnamon | Basit yapılı ve hafiftir. Farklı arayüzler (greeter) ile kullanılabilir |

### Metin Tabanlı Giriş Yöneticileri (getty / TTY)

Grafik arayüzü olmayan ortamlarda veya kullanıcı grafik ekranı kullanmak istemediği durumlarda oturum açmak için kullanılır.
Çalışmak için bir TTY (Teletypewriter) ortamına ihtiyaç duyarlar. Bazı getty araçları: **agetty**, **mingetty**, **busybox getty**

Getty genellikle init sistemi tarafından başlatılır.

Getty elle çalıştırmak için aşağıdaki gibi komut kullanılabilir:
```sh
/sbin/agetty --noclear 38400 tty1 linux
```

* **38400** haberleşme hızını belirtir ve genellikle standart değer budur.
* **tty1** 1. tty ekranı üzerinde oturum ekranı oluşturulacağı anlamına gelir.
* **--noclear** başlanmadan önce ekranı temizlemeyeceği anlamına gelir. Bu parametre genellikle yalnızca tty1 için kullanılır.
* **linux** terminal türünü belirtir. (linux terminal ekranı için linux, seri haberleşme için vt100, terminal emulatörü için xterm veya xterm-256color)

### Uzaktan Bağlantı Yöntemleri

Sisteme ağ üzerinden uzaktan bağlanmak için kullanılır.
*   **SSH (Secure Shell):** Ağ üzerindeki başka bir bilgisayara güvenli ve şifreli bir şekilde bağlanmayı sağlayan endüstri standardı protokoldür. Varsayılan olarak 22. portu kullanır.
*   **Telnet:** SSH'ın eski ve şifresiz versiyonudur. Verileri açık metin (cleartext) olarak ilettiği için güvenlik açığı oluşturur ve modern sistemlerde yerini tamamen SSH'a bırakmıştır.


## Kabuk (Shell)

Kimlik doğrulama işlemi başarıyla tamamlandıktan sonra, sistem kullanıcının `/etc/passwd` dosyasında tanımlanmış olan varsayılan **Kabuk (Shell)** programını başlatır.

| Adı | Açıklama |
|-----|----------|
| ash | Busybox tarafından sağlanan POSIX standartlarına uyumlu kabuktur.|
| dash (Debian Almquist Shell) | POSIX standartlarına sıkı sıkıya bağlı, son derece hafif, hızlı ve minimum kaynak tüketen bir kabuktur.|
| bash (Bourne Again Shell) | Linux dağıtımlarının çoğunda varsayılan olarak gelen, oldukça gelişmiş ve popüler bir kabuktur.|
| zsh (Z Shell) | Eklenti desteği, gelişmiş otomatik tamamlama ve tema seçenekleriyle (örn: Oh My Zsh) özellikle yazılımcılar arasında popülerdir.|
| fish (Friendly Interactive Shell) | Yapılandırma gerektirmeksizin kutudan çıktığı gibi sözdizimi vurgulaması ve akıllı öneriler sunan kullanıcı dostu bir kabuktur.|

**Not:** Sistem varsayılan olarak `/bin/sh` komutunu kabuk olarak kabul eder. Bu dosyaya varsayılan sistem kabuğu linklenir. (Örneğin debian için /bin/dash, archlinux için /bin/bash, alpine için /bin/busybox)
