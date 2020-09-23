-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 23 Eyl 2020, 22:38:02
-- Sunucu sürümü: 10.4.13-MariaDB
-- PHP Sürümü: 7.4.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `coronablog`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `articles`
--

CREATE TABLE `articles` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `author` text NOT NULL,
  `content` text NOT NULL,
  `created_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `keywords` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `articles`
--

INSERT INTO `articles` (`id`, `title`, `author`, `content`, `created_date`, `keywords`) VALUES
(2, '    Load Balancing Nedir?', 'yusuf', '<p><strong>Konu İ&ccedil;eriği</strong><br />\r\n<br />\r\n<strong>➤</strong>&nbsp;Load Balancing Nedir?<br />\r\n<br />\r\n<strong>➤</strong>&nbsp;Load Balancing Nasıl &Ccedil;alışır?<br />\r\n<br />\r\n<strong>➤</strong>&nbsp;Load Balancing Algoritmaları<br />\r\n<br />\r\n<strong>➤</strong>&nbsp;Load Balancing Kullanmanın &Ouml;nemi<br />\r\n<br />\r\n<br />\r\n<br />\r\n<strong>Load Balancing Nedir?</strong><br />\r\n<br />\r\nY&uuml;k dengeleme yani &lsquo;load balancing&rsquo; en genel tanımıyla gelen ağ trafiğini sunucular arasında paylaştırma işlemidir. Artan trafiğin karşılanabilmesi i&ccedil;in ger&ccedil;ekleştirilen paylaştırma işlemi isteğe g&ouml;re eşit olarak yapılabilir ya da belirli kurallar &ccedil;er&ccedil;evesinde ger&ccedil;ekleştirilebilir. Sunucu kapandığında y&uuml;k dengeleyici trafiği &ccedil;evrimi&ccedil;i olan sunuculara y&ouml;nlendiriyor. Uygulama ve aynı zamanda veritabanı sunucuları arasında dengelemeyi sağlayan sistemler ise &lsquo;load balancer&rsquo; olarak adlandırılıyor.<br />\r\n<br />\r\nLoad balancing &ouml;zelliğinin kullanılmaması durumunda tahmin edilebileceği gibi tek bir sunucuya bağlanılır. Bu sunucu &uuml;zerinde herhangi bir sorun olması ise internet sitesine erişimi sıkıntıya sokar. Ayrıca &ccedil;ok sayıda kullanıcının internet sitesine erişmek istemesi durumunda da sorun yaşanabilir. &Ccedil;&uuml;nk&uuml; bu durumda sayfaların y&uuml;klenme s&uuml;relerinde yavaşlama meydana gelir hatta siteye erişim bile kesilebilir. Bu nedenle load balancing &ouml;zelliğinin mutlaka kullanılması gerekir.<br />\r\n<br />\r\nLoad balancerler ise 4 trafik t&uuml;r&uuml; i&ccedil;in dengeleme kuralları oluşturabiliyor. Bunlar;<br />\r\n<br />\r\n<strong>&raquo;</strong>HTTP<br />\r\n<strong>&raquo;</strong>HTTPS<br />\r\n<strong>&raquo;</strong>TCP<br />\r\n<strong>&raquo;</strong>UDP<br />\r\n&nbsp;</p>\r\n\r\n<table cellspacing=\"0\" style=\"border-collapse:collapse; width:600px\">\r\n	<tbody>\r\n		<tr>\r\n			<td style=\"width:20px\"><a href=\"https://i.resimyukle.xyz/SMJU9G.png\"><img alt=\"\" src=\"https://www.turkhackteam.org/images/statusicon/wol_error.gif\" style=\"height:16px; width:16px\" /></a></td>\r\n			<td><a href=\"https://i.resimyukle.xyz/SMJU9G.png\">Bu resim yeniden boyutlandırıldı, tam halini g&ouml;rmek i&ccedil;in tıklayınız.</a></td>\r\n		</tr>\r\n	</tbody>\r\n</table>\r\n\r\n<p><a href=\"https://i.resimyukle.xyz/SMJU9G.png\"><img src=\"https://i.resimyukle.xyz/SMJU9G.png\" style=\"width:600px\" /></a><br />\r\n<br />\r\n<br />\r\n<strong>Load Balancing Nasıl &Ccedil;alışır?</strong><br />\r\n<br />\r\nLoad balancer &ccedil;alışma prensibi aslında sanıldığı kadar kompleks bir yapıya sahip değildir. İsteği sunucuya iletmesi toplamda iki aşamadan oluşan bir prensip ile ger&ccedil;ekleşiyor. İlk olarak sunucuların isteğe uygun bi&ccedil;imde yanıt verebileceğinin teyidi sağlanıyor ve sonrasında sunucular arasından se&ccedil;im yapılması i&ccedil;in daha &ouml;nce belirlenmiş olan kurallar ile iletim tamamlanıyor.<br />\r\n<br />\r\n<strong>Uygunluk Kontrolleri</strong><br />\r\n<br />\r\nHealth checks yani uygunluk kontrolleri &ouml;nemli bir aşamadır ve bu esnada load balancingin uygulandığı sistemlerde ağ trafiği sadece performans bakımından ideal olan sunuculara iletiliyor. Kontrolden ge&ccedil;emeyen sunucuların ise havuzdan kaldırılması sağlanıyor ve bu sunucuya trafik g&ouml;nderilmiyor.<br />\r\n<br />\r\n<a href=\"https://i.resimyukle.xyz/9yQ7c3.gif\"><img src=\"https://i.resimyukle.xyz/9yQ7c3.gif\" /></a><br />\r\n<br />\r\n<br />\r\n<strong>Load Balancing Algoritmaları</strong><br />\r\n<br />\r\nY&uuml;k dengeleme algoritmalarının trafiğin hangi backend sunucusuna iletileceğini belirlediğini s&ouml;yleyebiliriz. Bu algoritmaların her birinin farklı bir faydası bulunuyor. Dengeleme y&ouml;ntemi ise sistemin gereksinimlerine g&ouml;re değişiyor.<br />\r\n<br />\r\n<strong>Round Robin</strong><br />\r\n<br />\r\nGelen istekleri sunucu grubuna dağıtıyor ve mevcut sunucular arasından ilk olarak ilk sırada bulunanı kullanıyor. Sunucu se&ccedil;imleri listedeki sıraya g&ouml;re devam eder.<br />\r\n<br />\r\n<strong>Least Connections</strong><br />\r\n<br />\r\nY&uuml;k g&ouml;nderiminde en az bağlantıya sahip olan sunucuyu dikkate alıyor ve bu se&ccedil;enek trafiğin uzun ortamlarla sonu&ccedil;landığı durumlarda tavsiye ediliyor.<br />\r\n<br />\r\n<strong>Source (IP Hash)</strong><br />\r\n<br />\r\nLoad balancing istemcinin IP adresini ve isteği hangi sunucunun alacağını belirlemeyi sağlar. Bu se&ccedil;enek kapsamında kullanıcının s&uuml;rekli aynı sunucuya bağlanması m&uuml;mk&uuml;n oluyor.<br />\r\n<br />\r\n<a href=\"https://i.resimyukle.xyz/8PA346.png\"><img src=\"https://i.resimyukle.xyz/8PA346.png\" /></a><br />\r\n<br />\r\n<br />\r\n<strong>Load Balancing Kullanmanın &Ouml;nemi</strong><br />\r\n<br />\r\nİnternet sitelerinde sunucu s&uuml;rekliliği ve erişilebilirlik elbette en &ouml;nemli unsurlardır ve bunu sağlamak da load balancing ile m&uuml;mk&uuml;n olabiliyor. Zira bu fakt&ouml;r tek başında load balancing &ouml;nemini ortaya koyuyor. Sitelerde kimi zaman trafik artışları olabilir ve bu durumu da her daim g&ouml;z &ouml;n&uuml;nde bulundurmak gerekiyor. Erişim kesintilerinin yaşanmaması sayesinde kullanıcı deneyimleri de gelişir. Kullanıcıların en uygun olan veri tabanı kaynaklarına y&ouml;nlendiriliyor ve dolayısıyla veritabanı optimizasyonu da sağlanmış oluyor. Bu durum &lsquo;single point of failure&rsquo; riskini de yok ediyor.<br />\r\n<br />\r\n<a href=\"https://i.resimyukle.xyz/5dA24M.png\"><img src=\"https://i.resimyukle.xyz/5dA24M.png\" /></a><br />\r\n<br />\r\n<br />\r\n<a href=\"https://i.resimyukle.xyz/RGQJLC.gif\"><img src=\"https://i.resimyukle.xyz/RGQJLC.gif\" /></a><br />\r\n//Alıntıdır<br />\r\n<br />\r\n<br />\r\nOkuduğunuz İ&ccedil;in Teşekk&uuml;r Ederim.<br />\r\nEsenlikle Kalın..<br />\r\n<br />\r\n<strong>Saygılarımla</strong><img alt=\"\" src=\"https://www.turkhackteam.org/images/smilies/smiles2019/Smiley1021.png\" /></p>\r\n', '2020-08-07 18:37:12', '    Load Balancing Nedir? Load Balancing Nasıl Çalışır?');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `contact`
--

CREATE TABLE `contact` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `surname` varchar(100) NOT NULL,
  `message` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL,
  `uname` char(50) NOT NULL,
  `pwd` text NOT NULL,
  `status` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `user`
--

INSERT INTO `user` (`id`, `name`, `email`, `uname`, `pwd`, `status`) VALUES
(14, 'Corona Blog', 'yusufcandogru120@gmail.com', 'admin', '$5$rounds=535000$AeEdzY6y67R3PAvd$qiZyVHMUnmJmuL4P3O9Yn3ZXjs/KNIATHmgVh1YeHv9', 1);

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`,`uname`),
  ADD UNIQUE KEY `uname` (`uname`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Tablo için AUTO_INCREMENT değeri `contact`
--
ALTER TABLE `contact`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Tablo için AUTO_INCREMENT değeri `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
